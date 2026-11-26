"""Private SQLite file and sidecar validation for local CYBER_AI stores."""
import os
import sqlite3
import stat
from pathlib import Path

from safe_io import SafeWriteError, ensure_private_directory


def _is_reparse_point(info):
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(info, "st_file_attributes", 0) & flag)


def _inspect_private_file(path):
    try:
        before = path.lstat()
    except FileNotFoundError:
        return
    except OSError as error:
        raise SafeWriteError("No se pudo inspeccionar un archivo SQLite.") from error

    if (
        stat.S_ISLNK(before.st_mode)
        or _is_reparse_point(before)
        or not stat.S_ISREG(before.st_mode)
    ):
        raise SafeWriteError("SQLite solo puede usar archivos regulares sin enlaces.")

    if os.name == "posix":
        if before.st_uid != os.geteuid():
            raise SafeWriteError("El archivo SQLite debe pertenecer al usuario efectivo.")
        if before.st_nlink != 1:
            raise SafeWriteError("No se permiten enlaces duros en archivos SQLite.")
        if stat.S_IMODE(before.st_mode) != 0o600:
            try:
                os.chmod(path, 0o600, follow_symlinks=False)
            except (OSError, NotImplementedError) as error:
                raise SafeWriteError("No se pudieron restringir los permisos SQLite.") from error

    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    descriptor = None
    try:
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        after = path.lstat()
        if (
            not stat.S_ISREG(opened.st_mode)
            or stat.S_ISLNK(after.st_mode)
            or _is_reparse_point(after)
            or (opened.st_dev, opened.st_ino) != (after.st_dev, after.st_ino)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
        ):
            raise SafeWriteError("El archivo SQLite cambió durante su validación.")
        if os.name == "posix" and (
            opened.st_uid != os.geteuid()
            or opened.st_nlink != 1
            or stat.S_IMODE(opened.st_mode) & 0o077
        ):
            raise SafeWriteError("El archivo SQLite no conserva propiedad y permisos privados.")
    except SafeWriteError:
        raise
    except OSError as error:
        raise SafeWriteError("No se pudo abrir de forma segura un archivo SQLite.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def secure_sqlite_path(path):
    """Create/validate a private DB and reject unsafe journal/WAL/SHM sidecars."""
    try:
        destination = Path(os.path.abspath(os.fspath(path)))
    except (TypeError, ValueError, OSError) as error:
        raise SafeWriteError("La ruta SQLite no es válida.") from error

    ensure_private_directory(destination.parent, create=True)

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        descriptor = os.open(destination, flags, 0o600)
    except FileExistsError:
        pass
    except OSError as error:
        raise SafeWriteError("No se pudo crear el archivo SQLite privado.") from error
    else:
        try:
            if os.name == "posix":
                os.fchmod(descriptor, 0o600)
        finally:
            os.close(descriptor)

    for candidate in (
        destination,
        Path(f"{destination}-journal"),
        Path(f"{destination}-wal"),
        Path(f"{destination}-shm"),
    ):
        _inspect_private_file(candidate)
    return destination


def connect_private_sqlite(path, *, timeout=10):
    """Open SQLite only after validating its private path and rechecking identity."""
    destination = secure_sqlite_path(path)
    try:
        before = destination.lstat()
    except OSError as error:
        raise SafeWriteError("El archivo SQLite no está disponible.") from error

    connection = None
    try:
        connection = sqlite3.connect(str(destination), timeout=timeout)
        secure_sqlite_path(destination)
        after = destination.lstat()
        if (
            stat.S_ISLNK(after.st_mode)
            or _is_reparse_point(after)
            or not stat.S_ISREG(after.st_mode)
            or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
        ):
            raise SafeWriteError("El archivo SQLite cambió durante la conexión.")
        connection.execute("PRAGMA trusted_schema=OFF")
        connection.execute("PRAGMA secure_delete=ON")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection
    except Exception:
        if connection is not None:
            connection.close()
        raise


__all__ = ["connect_private_sqlite", "secure_sqlite_path"]
