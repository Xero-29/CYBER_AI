# Conexión de IA sin modificar el núcleo

## Objetivo

CYBER_AI conserva la memoria, la biblioteca de conocimiento, el Skillbook,
las herramientas, las políticas y los historiales. El proveedor de IA es un
servicio intercambiable: cambiarlo no migra ni elimina esos datos.

La interfaz de proveedores normaliza las respuestas de chat y embeddings al
contrato que ya utiliza `agent_runner.py`. Los adaptadores no deben escribir
directamente en las bases de datos de memoria ni cambiar las Skills.

## Estado de los adaptadores

- `ollama`: proveedor local mediante su API HTTP.
- `openai_compatible`: proveedores remotos que implementan la API compatible
  de chat completions y embeddings.
- Un proveedor con API nativa incompatible necesita un adaptador nuevo dentro
  de `llm_providers.py` (o un módulo de adaptador registrado). No se debe
  fingir compatibilidad con solo cambiar una URL.

## Configuración sin tocar código

1. Copia o edita `config/model_roles.json` en la instalación local.
2. En `default_provider`, selecciona el identificador del proveedor habilitado.
3. Configura `base_url`, `protocol`, `default_model` y, cuando corresponda,
   `embedding_model` o el mapa `models`.
4. Guarda la clave API en la variable de entorno indicada por `api_key_env`.
   Nunca la guardes en Git, JSON de configuración compartido ni archivos de Skills.
5. Ejecuta las pruebas y una tarea inocua de diagnóstico antes de usarlo.

Ejemplo de configuración para un endpoint compatible con OpenAI:

```json
{
  "default_provider": "openai_compatible",
  "llm_providers": {
    "openai_compatible": {
      "enabled": true,
      "protocol": "openai",
      "base_url": "https://api.example/v1",
      "api_key_env": "CYBER_AI_LLM_API_KEY",
      "requires_api_key": true,
      "default_model": "modelo-chat",
      "embedding_model": "modelo-embeddings",
      "models": {
        "NEXO": "modelo-razonamiento",
        "FORJA": "modelo-codigo",
        "FILTRO": "modelo-chat",
        "VERITAS": "modelo-revision",
        "FARO": "modelo-chat",
        "ECO": "modelo-embeddings"
      }
    }
  }
}
```

Los nombres de modelo son identificadores que el proveedor remoto reconoce;
el ejemplo no presupone que esos modelos existan. Si no se especifica un modelo
por especialista, se utiliza `default_model`. Para ECO se prioriza su entrada
en `models`, después `embedding_model`, y luego `default_model`.

En Linux, configura la clave en el entorno de ejecución, por ejemplo:

```bash
export CYBER_AI_LLM_API_KEY="tu-clave"
```

No escribas la clave en este documento ni en el repositorio.

## Precedencia de selección de modelo

Para cada especialista:

1. `llm_providers[proveedor].models[NombreEspecialista]`
2. `llm_providers[proveedor].models[id]`
3. Para agentes de embeddings, `embedding_model`
4. `default_model` del proveedor
5. El modelo declarado originalmente en el agente (compatibilidad local)

El proveedor se elige por `agent.provider` si existe; si no, por
`default_provider`. Un agente puede usar un proveedor distinto sin cambiar
su memoria ni sus permisos.

## Datos que permanecen en CYBER_AI

- SQLite y archivos de la biblioteca de conocimiento.
- Índices y metadatos de documentos.
- Historial de tareas, evidencias y checkpoints.
- Lecciones verificadas.
- Skillbook y versiones de metodologías.
- Políticas, autorizaciones y auditoría.

Los embeddings sí dependen del modelo de embeddings: al cambiarlo, los vectores
antiguos pueden no ser comparables con los nuevos. La migración correcta es
mantener el identificador del modelo y sus dimensiones por vector, y reindexar
solo cuando se cambie el modelo o espacio vectorial. No se deben mezclar vectores
de modelos distintos en una misma búsqueda.

## Condiciones de aceptación para futuros adaptadores

- Implementar chat y, si se ofrece, embeddings con un contrato normalizado.
- Declarar capacidades y límites reales del proveedor.
- No solicitar ni persistir credenciales fuera del entorno seguro.
- No cambiar memoria, Skills, permisos ni evidencias.
- Errores de red, límites y respuestas incompatibles deben ser explícitos.
- Tener pruebas unitarias con respuestas simuladas.
- Permitir cambiar proveedor sin modificar módulos de negocio.
- Mantener una vía de ejecución local sin proveedor remoto.

## Limitaciones actuales

El adaptador remoto implementa el protocolo OpenAI-compatible. No significa que
cualquier API nativa de cualquier fabricante funcione directamente. Para
proveedores con protocolo propio se debe añadir y probar un adaptador, manteniendo
el mismo contrato interno. Esta ampliación no requiere modificar el Skillbook,
la biblioteca ni los módulos de ciberseguridad.
