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
    """Validate every directory component against links and untrusted writers."""
    current = Path(directory)
    while True:
        try:
            info = current.lstat()
        except OSError as error:
            raise SafeWriteError("El directorio de salida no está disponible.") from error
        if (
            stat.S_ISLNK(info.st_mode)
            or _is_reparse_point(info)
            or not stat.S_ISDIR(info.st_mode)
        ):
            raise SafeWriteError(
                "La ruta de salida solo puede contener directorios reales, sin enlaces."
            )
        if os.name == "posix":
            effective_uid = os.geteuid()
            mode = stat.S_IMODE(info.st_mode)
            trusted_owner = info.st_uid in {0, effective_uid}
            root_sticky = (
                info.st_uid == 0 and bool(info.st_mode & stat.S_ISVTX)
            )
            if not trusted_owner or (mode & 0o022 and not root_sticky):
                raise SafeWriteError(
                    "El directorio padre o uno de sus ancestros debe pertenecer a root o al usuario "
                    "efectivo y no ser modificable por terceros."
                )
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
        if (
            stat.S_ISLNK(before.st_mode)
            or _is_reparse_point(before)
            or not stat.S_ISREG(before.st_mode)
        ):
            raise SafeWriteError(
                "El archivo privado debe ser regular y no puede ser un enlace."
            )
    except FileNotFoundError:
        if not mode.startswith("a"):
            raise SafeWriteError("El archivo privado no existe.")

    flags = (
        getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
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




def _reject_link_components(directory):
    """Reject symlinks and reparse points in every input-path directory."""
    current = Path(directory)
    while True:
        try:
            info = current.lstat()
        except OSError as error:
            raise SafeWriteError("El directorio de entrada no está disponible.") from error
        if (
            stat.S_ISLNK(info.st_mode)
            or _is_reparse_point(info)
            or not stat.S_ISDIR(info.st_mode)
        ):
            raise SafeWriteError("La ruta de entrada no puede contener enlaces.")
        if current.parent == current:
            return
        current = current.parent


def is_real_directory(path):
    """Return whether path is a real directory, not a symlink or reparse point."""
    try:
        candidate = Path(os.path.abspath(os.fspath(path)))
        _reject_link_components(candidate.parent)
        info = candidate.lstat()
    except (OSError, SafeWriteError):
        return False
    return (
        stat.S_ISDIR(info.st_mode)
        and not stat.S_ISLNK(info.st_mode)
        and not _is_reparse_point(info)
    )


def read_regular_file(path, *, max_bytes=16 * 1024 * 1024):
    """Read a bounded regular file without following symlinks or hard links."""
    if (
        isinstance(max_bytes, bool)
        or not isinstance(max_bytes, int)
        or max_bytes < 0
    ):
        raise SafeWriteError("El límite de lectura debe ser un entero no negativo.")

    destination = Path(os.path.abspath(os.fspath(path)))
    _reject_link_components(destination.parent)
    try:
        before = destination.lstat()
    except OSError as error:
        raise SafeWriteError("El archivo de entrada no está disponible.") from error
    if (
        stat.S_ISLNK(before.st_mode)
        or _is_reparse_point(before)
        or not stat.S_ISREG(before.st_mode)
    ):
        raise SafeWriteError("La entrada debe ser un archivo regular sin enlaces.")
    if os.name == "posix" and before.st_nlink != 1:
        raise SafeWriteError("No se permiten enlaces duros en archivos de entrada.")
    if before.st_size > max_bytes:
        raise SafeWriteError("El archivo de entrada supera el límite de lectura.")

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    descriptor = None
    try:
        descriptor = os.open(destination, flags)
        opened = os.fstat(descriptor)
        _reject_link_components(destination.parent)
        after = destination.lstat()
        if (
            not stat.S_ISREG(opened.st_mode)
            or _is_reparse_point(opened)
            or stat.S_ISLNK(after.st_mode)
            or _is_reparse_point(after)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
        ):
            raise SafeWriteError("El archivo de entrada cambió durante su apertura.")
        if os.name == "posix" and opened.st_nlink != 1:
            raise SafeWriteError("No se permiten enlaces duros en archivos de entrada.")
        if opened.st_size > max_bytes:
            raise SafeWriteError("El archivo de entrada supera el límite de lectura.")

        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            content = stream.read(max_bytes + 1)
            if len(content) > max_bytes:
                raise SafeWriteError("El archivo de entrada supera el límite de lectura.")
            final = os.fstat(stream.fileno())
            _reject_link_components(destination.parent)
            path_info = destination.lstat()
            if (
                not stat.S_ISREG(final.st_mode)
                or _is_reparse_point(final)
                or stat.S_ISLNK(path_info.st_mode)
                or _is_reparse_point(path_info)
                or (final.st_dev, final.st_ino) != (path_info.st_dev, path_info.st_ino)
                or final.st_size != len(content)
                or final.st_size != opened.st_size
                or final.st_mtime_ns != opened.st_mtime_ns
            ):
                raise SafeWriteError("El archivo de entrada cambió durante su lectura.")
            if os.name == "posix" and final.st_nlink != 1:
                raise SafeWriteError("No se permiten enlaces duros en archivos de entrada.")
        return content
    except SafeWriteError:
        raise
    except OSError as error:
        raise SafeWriteError("No se pudo leer el archivo de forma segura.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def read_regular_text(path, *, encoding="utf-8", max_bytes=16 * 1024 * 1024):
    """Read and decode a bounded regular text file without following links."""
    try:
        return read_regular_file(path, max_bytes=max_bytes).decode(encoding)
    except UnicodeError as error:
        raise SafeWriteError("El archivo de entrada no contiene texto válido.") from error


def atomic_write_text(path, text, *, encoding="utf-8", mode=0o600, create_parents=False):
    """Write text through a private temporary file and atomically replace a regular file."""
    if not isinstance(text, str):
        raise SafeWriteError("El contenido debe ser texto.")
    if isinstance(mode, bool) or not isinstance(mode, int) or not 0 <= mode <= 0o777:
        raise SafeWriteError("El modo de archivo solicitado es inválido.")
    if os.name == "posix" and mode & 0o177:
        raise SafeWriteError(
            "El modo de salida POSIX debe ser privado y no ejecutable; "
            "no se permiten permisos de grupo u otros."
        )

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
                directory.mkdir(mode=0o700)
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
    directory_fd = None
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
        if os.name == "posix":
            directory_flags = (
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_CLOEXEC", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            directory_fd = os.open(parent, directory_flags)
            opened_directory = os.fstat(directory_fd)
            path_directory = parent.stat(follow_symlinks=False)
            if (
                not stat.S_ISDIR(opened_directory.st_mode)
                or not stat.S_ISDIR(path_directory.st_mode)
                or (opened_directory.st_dev, opened_directory.st_ino)
                != (path_directory.st_dev, path_directory.st_ino)
            ):
                raise SafeWriteError("El directorio padre cambió durante la publicación.")
            os.replace(
                temporary_path.name,
                destination.name,
                src_dir_fd=directory_fd,
                dst_dir_fd=directory_fd,
            )
        else:
            os.replace(temporary_path, destination)
        temporary_path = None
        if directory_fd is not None:
            # Persist the directory entry as well as the file contents.
            os.fsync(directory_fd)
            descriptor_to_close = directory_fd
            directory_fd = None
            os.close(descriptor_to_close)
    except SafeWriteError:
        raise
    except (OSError, UnicodeError) as error:
        raise SafeWriteError("No se pudo escribir el archivo de forma atómica.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if directory_fd is not None:
            os.close(directory_fd)
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
