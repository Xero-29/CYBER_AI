# Autonomous Skill Lab (prototipo ejecutable)

## Objetivo

Probar un ciclo local con Ollama: el modelo principal formula una hipótesis, el modelo pequeño la convierte en un proyecto Rust, el sandbox ejecuta pruebas sin red y la evidencia vuelve al planificador para una revisión limitada.

## Flujo

1. Planner (por defecto `qwen3.5:9b`) devuelve una especificación JSON sin comandos.
2. Executor/aprendiz (por defecto `qwen3.5:2b-q4_K_M`) prepara archivos Rust y documenta el procedimiento.
3. El validador solo acepta `Cargo.toml`, `src/main.rs` y `src/lib.rs`; no admite dependencias ni build scripts.
4. Docker ejecuta `cargo test --offline` con red deshabilitada, filesystem raíz read-only, usuario no privilegiado, capacidades eliminadas y límites de recursos.
5. Si falla, el planificador recibe el resultado acotado y puede revisar la hipótesis. Máximo tres rondas.
6. Se genera un informe JSON. Una ejecución exitosa guarda la metodología en una memoria JSONL local como candidata no verificada; tareas parecidas pueden recuperarla como referencia, nunca ejecutarla como comando ni tratarla como aprobada.

## Preparación

Requisitos: Linux, Docker Engine operativo, Python 3.10+, Ollama local y los dos modelos descargados.

```bash
ollama pull qwen3.5:9b
ollama pull qwen3.5:2b-q4_K_M
sh ./build-rust-skill-lab.sh
```

## Prueba

```bash
sh ./run-skill-lab.sh --task "Demuestra con un laboratorio Rust que los accesos fuera de los límites de un vector son detectados de forma segura y añade pruebas unitarias."
```

Para cambiar modelos:

```bash
CYBER_AI_PLANNER_MODEL=cyber-nexo:9b \
CYBER_AI_EXECUTOR_MODEL=qwen3.5:4b-q4_K_M \
sh ./run-skill-lab.sh --task "..." 
```

El endpoint Ollama se puede cambiar con `CYBER_AI_OLLAMA_URL`, pero este prototipo solo acepta HTTP loopback.

## Evidencia y estados

El informe se escribe en `reports/skill_lab/latest.json` (directorio local ignorado). Estados:
- `passed`: el contenedor terminó y `cargo test --offline` devolvió 0.
- `failed`: el proyecto llegó al sandbox y las pruebas fallaron.
- `inconclusive`: Ollama, Docker o la configuración no permitieron concluir.

No se equipara `passed` con demostrar seguridad general ni con validar una vulnerabilidad. Los tests generados por el agente no son un oráculo independiente; deben revisarse y repetirse con fixtures independientes antes de promover una skill.

## Límites de seguridad y aprendizaje

- No se ejecutan comandos arbitrarios emitidos por modelos.
- No hay acceso de red desde el contenedor ni dependencias Cargo externas.
- El workspace es temporal y se elimina al terminar.
- El perfil inicial solo compila proyectos Rust mínimos; no permite extracción de secretos, explotación de sistemas reales ni acceso a objetivos externos.
- El modelo no reentrena sus pesos. El aprendizaje es procedimental: práctica, diagnóstico, iteración y memoria local de candidatos en data/autonomous_skill_lab/skill_candidates.jsonl. Candidatos parecidos se recuperan como contexto no confiable. La promoción al Skillbook requiere revisión independiente y repetición externa.
- La imagen instala Rust desde los repositorios Debian de Bookworm; el build registra su ID, pero la resolución exacta de paquetes debe fijarse para una cadena de suministro reproducible de producción.
