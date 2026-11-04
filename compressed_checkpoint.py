#!/usr/bin/env python3
"""Almacena y recupera salidas parciales completas mediante bloques comprimidos."""

import json

import compressed_store

REFERENCE_PREFIX = "@compressed-chain:"


def get_block_ids(reference):
    """Extrae los IDs de un checkpoint comprimido; None si es texto antiguo."""
    if not isinstance(reference, str):
        return None

    if not reference.startswith(REFERENCE_PREFIX):
        return None

    try:
        ids = json.loads(reference[len(REFERENCE_PREFIX):])
    except json.JSONDecodeError as error:
        raise ValueError("La referencia del checkpoint está dañada.") from error

    if not isinstance(ids, list) or not all(
        isinstance(item, str) and item for item in ids
    ):
        raise ValueError("La lista de bloques del checkpoint no es válida.")

    return ids


def restore_partial_output(reference, session_id):
    """Recupera todos los fragmentos, o devuelve el texto de un checkpoint antiguo."""
    if not reference:
        return ""

    block_ids = get_block_ids(reference)

    # Compatibilidad con checkpoints antiguos guardados como texto.
    if block_ids is None:
        return str(reference)

    fragments = []
    for block_id in block_ids:
        block = compressed_store.read_block(block_id, session_id)
        fragments.append(block["content"])

    # Se conservan exactamente los caracteres de cada fragmento y su orden.
    return "".join(fragments)


def restore_partial_tail(reference, session_id, max_chars=1400):
    """Recupera solo la cola necesaria para continuar una respuesta."""
    max_chars = max(1, int(max_chars))

    if not reference:
        return ""

    block_ids = get_block_ids(reference)

    # Compatibilidad con checkpoints antiguos guardados como texto.
    if block_ids is None:
        return str(reference)[-max_chars:]

    fragments = []
    collected_chars = 0

    # Leer primero los bloques más recientes; detenerse al tener contexto.
    for block_id in reversed(block_ids):
        block = compressed_store.read_block(block_id, session_id)
        fragment = block["content"]
        fragments.append(fragment)
        collected_chars += len(fragment)

        if collected_chars >= max_chars:
            break

    return "".join(reversed(fragments))[-max_chars:]


def save_partial_chunk(
    *,
    content,
    session_id,
    task_id,
    previous_reference=None,
):
    """Comprime el nuevo fragmento y devuelve una referencia a toda la cadena."""
    if not session_id:
        raise ValueError("session_id es obligatorio.")

    if not task_id:
        raise ValueError("task_id es obligatorio.")

    block_ids = []

    if previous_reference:
        existing_ids = get_block_ids(previous_reference)

        if existing_ids is not None:
            # Validar acceso y sesión antes de reutilizar referencias existentes.
            for block_id in existing_ids:
                compressed_store.read_block(block_id, session_id)
            block_ids.extend(existing_ids)
        else:
            # Migrar el texto de checkpoints antiguos a un bloque comprimido.
            old_block = compressed_store.store_block(
                content=str(previous_reference),
                session_id=session_id,
                task_id=task_id,
                kind="partial_output",
                metadata={"origin": "legacy_checkpoint"},
            )
            block_ids.append(old_block["id"])

    if content:
        new_block = compressed_store.store_block(
            content=content,
            session_id=session_id,
            task_id=task_id,
            kind="partial_output",
            metadata={"sequence": len(block_ids)},
        )
        block_ids.append(new_block["id"])

    if not block_ids:
        return None

    return REFERENCE_PREFIX + json.dumps(
        block_ids, separators=(",", ":")
    )
