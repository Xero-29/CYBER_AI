"""Atomic file writes that reject symlink destinations and parents."""
import os
import stat
import tempfile
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


def atomic_write_text(path, text, *, encoding="utf-8", mode=0o600, create_parents=False):
    """Write text through a private temporary file and atomically replace a regular file."""
    if not isinstance(text, str):
        raise SafeWriteError("El contenido debe ser texto.")
    if isinstance(mode, bool) or not isinstance(mode, int) or not 0 <= mode <= 0o777:
        raise SafeWriteError("El modo de archivo solicitado es inválido.")

    destination = Path(os.path.abspath(os.fspath(path)))
    parent = destination.parent
    if create_parents:
        parent.mkdir(parents=True, exist_ok=True)
    if not parent.is_dir():
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
