"""Atomic file writes that reject symlink destinations and parents."""
import os
import stat
import tempfile
from contextlib import contextmanager
from pathlib import Path


class SafeWriteError(ValueError):
    """The requested output path is not a safe regular-file destination."""


def _is_reparse_point(info):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(info, "st_file_attributes", 0) & flag)


def _reject_symlink_components(directory):
    current = Path(directory)
    while True:
        try:
            info = current.lstat()
        except OSError as error:
            raise SafeWriteError("El directorio de salida no está disponible.") from error
        if stat.S_ISLNK(info.st_mode) or _is_reparse_point(info):
            raise SafeWriteError("No se permiten symlinks ni puntos de reanálisis en la ruta.")
        if current.parent == current:
            return
        current = current.parent


def _validate_destination(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return
    except OSError as error:
        raise SafeWriteError("No se pudo inspeccionar el destino de escritura.") from error
    if (
        stat.S_ISLNK(info.st_mode)
        or _is_reparse_point(info)
        or not stat.S_ISREG(info.st_mode)
    ):
        raise SafeWriteError("El destino debe ser un archivo regular, nunca un symlink.")



def ensure_private_directory(path, *, create=True):
    """Create or validate a directory that is private to the current POSIX user."""
    destination = Path(os.path.abspath(os.fspath(path)))
    if create:
        missing = []
        current = destination
        while not current.exists() and not current.is_symlink():
            missing.append(current)
            current = current.parent
        _reject_symlink_components(current)
        if not current.is_dir():
            raise SafeWriteError("Un componente de la ruta no es un directorio.")
        for directory in reversed(missing):
            try:
                directory.mkdir(mode=0o700)
            except FileExistsError:
                pass
            _reject_symlink_components(directory)
            if not directory.is_dir():
                raise SafeWriteError("Un componente de la ruta no es un directorio.")
    _reject_symlink_components(destination)
    if not destination.is_dir():
        raise SafeWriteError("El destino debe ser un directorio existente.")
    if os.name == "posix":
        try:
            effective_uid = os.geteuid()
            parent_info = destination.parent.stat()
            directory_info = destination.stat(follow_symlinks=False)
            if directory_info.st_uid != effective_uid:
                raise SafeWriteError(
                    "El directorio privado debe pertenecer al usuario efectivo del proceso."
                )
            parent_mode = stat.S_IMODE(parent_info.st_mode)
            parent_is_trusted = parent_info.st_uid in {0, effective_uid}
            parent_is_root_sticky = (
                parent_info.st_uid == 0
                and bool(parent_info.st_mode & stat.S_ISVTX)
            )
            if (
                not parent_is_trusted
                or (parent_mode & 0o022 and not parent_is_root_sticky)
            ):
                raise SafeWriteError(
                    "El directorio padre debe pertenecer a root o al usuario efectivo y "
                    "no ser escribible por grupo u otros, salvo un padre sticky propiedad de root."
                )
            os.chmod(destination, 0o700, follow_symlinks=False)
            mode = stat.S_IMODE(destination.stat(follow_symlinks=False).st_mode)
        except SafeWriteError:
            raise
        except (OSError, NotImplementedError) as error:
            raise SafeWriteError("No se pudieron restringir los permisos del directorio.") from error
        if mode & 0o077:
            raise SafeWriteError("El directorio debe ser privado (permisos 0700).")
    return destination



@contextmanager
def open_private_file(path, mode="r", *, encoding="utf-8"):
    """Open a private regular file without following links or accepting hard links."""
    if mode not in {"r", "rb", "a", "a+"}:
        raise SafeWriteError("El modo de apertura privada no está permitido.")
    destination = Path(os.path.abspath(os.fspath(path)))
    ensure_private_directory(destination.parent, create=mode.startswith("a"))
    before = None
    try:
        before = destination.lstat()
        if stat.S_ISLNK(before.st_mode) or _is_reparse_point(before):
            raise SafeWriteError("No se permiten enlaces en archivos privados.")
    except FileNotFoundError:
        if not mode.startswith("a"):
            raise SafeWriteError("El archivo privado no existe.")

    flags = getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    if mode in {"r", "rb"}:
        flags |= os.O_RDONLY
    elif mode == "a":
        flags |= os.O_WRONLY | os.O_APPEND | os.O_CREAT
    else:
        flags |= os.O_RDWR | os.O_APPEND | os.O_CREAT

    descriptor = None
    stream = None
    try:
        descriptor = os.open(destination, flags, 0o600)
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise SafeWriteError("El archivo privado debe ser regular.")
        if os.name == "posix":
            if opened.st_uid != os.geteuid():
                raise SafeWriteError(
                    "El archivo privado debe pertenecer al usuario efectivo del proceso."
                )
            if opened.st_nlink != 1:
                raise SafeWriteError("No se permiten enlaces duros en archivos privados.")
            if stat.S_IMODE(opened.st_mode) & 0o077:
                os.fchmod(descriptor, 0o600)

        after = destination.lstat()
        if (
            stat.S_ISLNK(after.st_mode)
            or _is_reparse_point(after)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
            or (
                before is not None
                and (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            )
        ):
            raise SafeWriteError("El archivo privado cambió durante su apertura.")

        if mode == "rb":
            stream = os.fdopen(descriptor, mode)
        else:
            stream = os.fdopen(descriptor, mode, encoding=encoding, newline="")
        descriptor = None
        try:
            yield stream
            if mode.startswith("a"):
                stream.flush()
                os.fsync(stream.fileno())
            final_info = os.fstat(stream.fileno())
            path_info = destination.lstat()
            if (
                stat.S_ISLNK(path_info.st_mode)
                or _is_reparse_point(path_info)
                or (final_info.st_dev, final_info.st_ino) !=
                   (path_info.st_dev, path_info.st_ino)
            ):
                raise SafeWriteError("El archivo privado cambió durante su uso.")
            if os.name == "posix" and (
                final_info.st_uid != os.geteuid() or final_info.st_nlink != 1
            ):
                raise SafeWriteError("La propiedad o los enlaces del archivo privado cambiaron.")
        finally:
            stream.close()
    except SafeWriteError:
        raise
    except OSError as error:
        raise SafeWriteError("No se pudo abrir o actualizar el archivo privado.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)



def atomic_write_text(path, text, *, encoding="utf-8", mode=0o600, create_parents=False):
    """Write text through a private temporary file and atomically replace a regular file."""
    if not isinstance(text, str):
        raise SafeWriteError("El contenido debe ser texto.")
    if isinstance(mode, bool) or not isinstance(mode, int) or not 0 <= mode <= 0o777:
        raise SafeWriteError("El modo de archivo solicitado es inválido.")

    destination = Path(os.path.abspath(os.fspath(path)))
    parent = destination.parent
    if create_parents:
        missing = []
        current = parent
        while not current.exists() and not current.is_symlink():
            missing.append(current)
            current = current.parent
        _reject_symlink_components(current)
        if not current.is_dir():
            raise SafeWriteError("Un componente de la ruta de salida no es un directorio.")
        for directory in reversed(missing):
            try:
                directory.mkdir()
            except FileExistsError:
                pass
            _reject_symlink_components(directory)
            if not directory.is_dir():
                raise SafeWriteError("Un componente de la ruta de salida no es un directorio.")
    elif not parent.is_dir():
        raise SafeWriteError("El directorio padre del destino no existe.")
    _reject_symlink_components(parent)
    _validate_destination(destination)

    descriptor = None
    temporary_path = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=str(parent)
        )
        temporary_path = Path(temporary_name)
        if os.name == "posix":
            os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding=encoding, newline="") as stream:
            descriptor = None
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        _reject_symlink_components(parent)
        _validate_destination(destination)
        os.replace(temporary_path, destination)
        temporary_path = None
    except SafeWriteError:
        raise
    except (OSError, UnicodeError) as error:
        raise SafeWriteError("No se pudo escribir el archivo de forma atómica.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
