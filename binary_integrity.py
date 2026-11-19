"""Race-aware hashing for external executables before and after execution."""
import hashlib
import os
import stat
from pathlib import Path


MAX_EXECUTABLE_BYTES = 2 * 1024 * 1024 * 1024


class BinaryIntegrityError(ValueError):
    """An executable could not be safely opened or remained stable while hashed."""


def hash_executable(path):
    """Hash a resolved regular executable without following a final symlink."""
    descriptor = None
    try:
        resolved = Path(path).resolve(strict=True)
        before = resolved.lstat()
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if (
            stat.S_ISLNK(before.st_mode)
            or getattr(before, "st_file_attributes", 0) & reparse_flag
            or not stat.S_ISREG(before.st_mode)
            or before.st_size <= 0
            or before.st_size > MAX_EXECUTABLE_BYTES
        ):
            raise BinaryIntegrityError("El ejecutable debe ser un archivo regular de tamaño permitido.")

        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        descriptor = os.open(resolved, flags)
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino)
            or opened.st_size != before.st_size
            or opened.st_mtime_ns != before.st_mtime_ns
        ):
            raise BinaryIntegrityError("El ejecutable cambió durante su apertura.")

        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_EXECUTABLE_BYTES:
                raise BinaryIntegrityError("El ejecutable supera el límite de tamaño.")
            digest.update(chunk)

        after = os.fstat(descriptor)
        path_after = resolved.lstat()
        identity = (opened.st_dev, opened.st_ino)
        if (
            (after.st_dev, after.st_ino) != identity
            or (path_after.st_dev, path_after.st_ino) != identity
            or not stat.S_ISREG(path_after.st_mode)
            or after.st_size != opened.st_size
            or after.st_mtime_ns != opened.st_mtime_ns
            or total != after.st_size
        ):
            raise BinaryIntegrityError("El ejecutable cambió mientras se calculaba su hash.")
        return {"resolved_path": str(resolved), "sha256": digest.hexdigest()}
    except BinaryIntegrityError:
        raise
    except (OSError, RuntimeError, ValueError) as error:
        raise BinaryIntegrityError("No se pudo verificar la integridad del ejecutable.") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


__all__ = ["BinaryIntegrityError", "hash_executable"]
