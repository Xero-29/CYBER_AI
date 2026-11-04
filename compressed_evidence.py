#!/usr/bin/env python3
"""Conecta el grafo de evidencia con el almacén comprimido."""

import json

import compressed_store
import evidence_graph


def store_evidence(
    *,
    title,
    content,
    session_id,
    task_id=None,
    kind="evidence",
    status="pending",
    source_url=None,
    source_quote=None,
    confidence=None,
    metadata=None,
):
    """Guarda el contenido completo comprimido y crea un índice en el grafo."""
    if not str(title).strip():
        raise ValueError("title es obligatorio.")

    if not evidence_graph.get_session(session_id):
        raise ValueError("La sesión indicada no existe.")

    extra_metadata = dict(metadata or {})

    block = compressed_store.store_block(
        content=content,
        session_id=session_id,
        task_id=task_id,
        kind=kind,
        metadata={
            "title": title,
            "source_url": source_url,
        },
    )

    # El nodo almacena un índice, no una segunda copia del contenido completo.
    node_metadata = {
        **extra_metadata,
        "storage": "compressed_block",
        "compressed_block_id": block["id"],
        "compressed_sha256": block["sha256"],
        "original_bytes": block["original_bytes"],
        "compressed_bytes": block["compressed_bytes"],
    }

    try:
        node_id = evidence_graph.add_node(
            kind=kind,
            content=title,
            task_id=task_id,
            session_id=session_id,
            status=status,
            source_url=source_url,
            source_quote=source_quote,
            confidence=confidence,
            metadata=node_metadata,
        )
    except Exception:
        # El bloque sin referencia se conserva para no borrar datos
        # automáticamente ante un fallo inesperado al crear el nodo.
        raise

    return {
        "node_id": node_id,
        "block_id": block["id"],
        "session_id": session_id,
        "original_bytes": block["original_bytes"],
        "compressed_bytes": block["compressed_bytes"],
        "sha256": block["sha256"],
    }


def read_evidence(node_id, session_id):
    """Lee una evidencia por referencia, solo dentro de su sesión."""
    node = evidence_graph.get_node(node_id)

    if node is None or node.get("session_id") != session_id:
        raise KeyError("Nodo inexistente o ajeno a esta sesión.")

    node_metadata = json.loads(node.get("metadata_json") or "{}")
    block_id = node_metadata.get("compressed_block_id")

    if not block_id:
        # Compatibilidad con nodos anteriores que guardan texto directamente.
        full_content = node["content"]
        storage = "graph"
    else:
        block = compressed_store.read_block(block_id, session_id)
        full_content = block["content"]
        storage = "compressed_block"

    return {
        "node_id": node_id,
        "session_id": session_id,
        "title": node["content"],
        "content": full_content,
        "status": node["status"],
        "source_url": node.get("source_url"),
        "source_quote": node.get("source_quote"),
        "storage": storage,
        "metadata": node_metadata,
    }
