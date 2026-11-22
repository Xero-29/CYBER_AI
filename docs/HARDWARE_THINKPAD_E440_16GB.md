# Perfil de ejecución: ThinkPad E440 con 16 GiB de RAM

## Objetivo

Ejecutar CYBER_AI en un portátil de recursos limitados, priorizando estabilidad sobre velocidad. Este perfil usa ejecución secuencial de especialistas y evita mantener varios modelos conversacionales cargados a la vez.

## Hardware conocido y límites

- Equipo: Lenovo ThinkPad E440.
- RAM instalada: 16 GiB (confirmada por el usuario).
- GPU: el perfil no depende de aceleración gráfica; se planifica inferencia por CPU.
- CPU exacta: debe verificarse en el equipo. El nombre E440 incluye distintas configuraciones.
- No se ha realizado una prueba de rendimiento en el portátil.

## Política aplicada

La política está guardada en `config/model_roles.json`:

| Parámetro | Valor | Motivo |
|---|---:|---|
| Modelos conversacionales simultáneos | 1 | Evita competir por RAM |
| Contexto predeterminado | 2.048 tokens | Reduce memoria KV |
| Contexto por especialista | 2.048 tokens | Evita que un agente sobrescriba el límite conservador |
| Reserva objetivo de RAM | 5 GiB | Mantiene margen para Linux y otros procesos |
| Permanencia normal | 0 s | No solicita permanencia normal adicional |
| Permanencia para continuación | 120 s | Evita recargar el mismo modelo entre fragmentos |
| Caché especulativa | Desactivada | Evita consumo adicional |

El ejecutor serializa las llamadas de CYBER_AI mediante un bloqueo y, antes de una llamada local a Ollama, descarga los otros modelos que encuentre activos. Esto protege el flujo de CYBER_AI; no impide que otro programa externo cargue modelos directamente en Ollama.

La reserva de 5 GiB se utiliza como margen en la operación de precarga `model_memory_manager.py warm`; no es un límite del sistema operativo ni una garantía de que cualquier modelo vaya a caber en memoria.

## Orden de trabajo recomendado

DIRECTOR es el coordinador Python: no consume una carga de modelo conversacional.

| Paso | Especialista | Modelo configurado | Cuándo ejecutarlo |
|---:|---|---|---|
| 0 | DIRECTOR | Python | Siempre: clasifica la tarea y decide el flujo |
| 1 | ECO | `nomic-embed-text:latest` | Solo cuando se necesite búsqueda semántica/embeddings |
| 2 | NEXO | `qwen3.5:4b-q4_K_M` | Análisis principal y formulación de hipótesis |
| 3 | INVESTIGADOR | `qwen3.5:0.8b` | Solo si NEXO detecta una brecha de conocimiento |
| 4 | FORJA | `qwen2.5-coder:3b` | Solo si hay que analizar o modificar código |
| 5 | FILTRO | `qwen2.5:1.5b` | Revisión adversarial cuando haya hipótesis o propuestas que refutar |
| 6 | VERITAS | `granite3.3:2b` | Verificación de afirmaciones, fuentes y evidencias |
| 7 | FARO | `qwen3.5:0.8b` | Revisión final de metodología y calidad |

No se deben ejecutar todos los especialistas por rutina. DIRECTOR debe omitir los que no aporten valor, guardar los resultados entre pasos y detener el flujo si falta evidencia esencial. ECO es un modelo de embeddings, no un revisor conversacional.

Este orden documenta el flujo recomendado. El comando actual `agent_runner.py ask` ejecuta un especialista por invocación; no debe interpretarse este documento como evidencia de que ya existe una orquestación automática de toda la cadena.

## Instalación de modelos

Desde la terminal, con Ollama instalado y en ejecución, descarga solo los modelos que falten:

```bash
ollama pull nomic-embed-text:latest
ollama pull qwen3.5:4b-q4_K_M
ollama pull qwen3.5:0.8b
ollama pull qwen2.5-coder:3b
ollama pull qwen2.5:1.5b
ollama pull granite3.3:2b
```

FARO e INVESTIGADOR comparten `qwen3.5:0.8b`; no hace falta descargarlo dos veces.

## Comprobación inicial en el portátil

Desde la raíz del repositorio:

```bash
python model_memory_manager.py status
ollama ps
free -h
lscpu
```

Comprueba que los seis modelos aparecen instalados, que no haya varios modelos conversacionales cargados al mismo tiempo y que Linux conserva memoria disponible suficiente.

Para preparar la caché de archivos de un modelo sin cargarlo en Ollama:

```bash
python model_memory_manager.py warm NEXO
```

La precarga se cancela si el tamaño de los archivos más la reserva configurada supera la RAM disponible.

## Límites conocidos antes de pruebas en caliente

1. La configuración reduce el contexto y limita las cargas del ejecutor, pero no garantiza una velocidad aceptable: el rendimiento dependerá del procesador exacto y del tamaño real de cada modelo.
2. La GPU integrada no se ha configurado como acelerador. Se asume CPU para evitar depender de una ruta de aceleración no verificada.
3. No se ha ejecutado Ollama ni se han descargado modelos en el ThinkPad desde este cambio.
4. Si el equipo se queda sin memoria, baja el contexto de forma controlada o deshabilita temporalmente los agentes más grandes; no aumentes el número de modelos cargados.
5. La ejecución de tareas de varios especialistas debe coordinarse secuencialmente y conservar checkpoints/resultados antes de cambiar de modelo.

## Criterio de aceptación en frío

- [x] Perfil de 16 GiB registrado en configuración.
- [x] Un solo modelo conversacional como objetivo de ejecución.
- [x] Contexto limitado a 2.048 tokens para los especialistas.
- [x] Reserva de 5 GiB configurada para la precarga.
- [x] Orden recomendado de especialistas documentado.
- [ ] Verificar CPU, RAM disponible y modelos instalados en el portátil.
- [ ] Ejecutar una prueba de cada modelo y medir RAM máxima, tiempo de carga, tokens/s y estabilidad.
- [ ] Ajustar contexto/modelos según mediciones reales.
