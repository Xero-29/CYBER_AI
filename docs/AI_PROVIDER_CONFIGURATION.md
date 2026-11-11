# Conectar una IA a CYBER_AI sin modificar código

CYBER_AI conserva memoria, biblioteca, Skillbook, especialistas, permisos y herramientas independientemente del proveedor del modelo. El proveedor se selecciona en `config/model_roles.json`.

## Estado del adaptador

- Ollama local: integrado como proveedor predeterminado.
- APIs compatibles con OpenAI Chat Completions y Embeddings: adaptador integrado.
- Anthropic: API nativa Messages para chat. No ofrece embeddings en este adaptador; asigna ECO a otro proveedor.
- Google Gemini: API nativa generateContent y embedContent.
- Otros proveedores: requieren un adaptador adicional; no se debe asumir compatibilidad solo por ser un proveedor de IA.
- Las claves API nunca se guardan en Git ni en este archivo.

## Activar un endpoint OpenAI-compatible

1. Configurar `llm_providers.openai_compatible.enabled` como `true`.
2. Especificar `base_url` con la URL base terminada en `/v1` (ejemplo: `https://api.proveedor.example/v1`).
3. Definir `CYBER_AI_LLM_API_KEY` como variable de entorno en el equipo donde se ejecuta CYBER_AI.
4. En cada especialista que se quiera enrutar, añadir `"provider": "openai_compatible"` y cambiar `model` por el identificador que entrega el proveedor.
5. Reiniciar el proceso de CYBER_AI. No hay que modificar Python ni migrar la biblioteca o las memorias.

Se puede mantener Ollama para algunos especialistas y asignar un proveedor remoto a otros. Para evitar mezclar espacios vectoriales, los embeddings remotos se guardan bajo el identificador proveedor::modelo; Ollama conserva su identificador histórico para no invalidar los vectores ya almacenados. Si se cambia el modelo de embeddings, los documentos deben reindexarse con ese modelo antes de que puedan recuperarse semánticamente desde el nuevo espacio. Las bases de datos, los documentos y las Skills permanecen en el mismo lugar.

## Ejemplo de configuración

```json
{
  "default_provider": "ollama",
  "llm_providers": {
    "ollama": {
      "enabled": true,
      "protocol": "ollama",
      "base_url": "http://127.0.0.1:11434",
      "requires_api_key": false
    },
    "openai_compatible": {
      "enabled": true,
      "protocol": "openai",
      "base_url": "https://api.proveedor.example/v1",
      "api_key_env": "CYBER_AI_LLM_API_KEY",
      "requires_api_key": true
    }
  },
  "agents": {
    "NEXO": {
      "provider": "openai_compatible",
      "model": "modelo-del-proveedor"
    }
  }
}
```

El fragmento ilustra los campos que se agregan; no reemplaza el resto de la definición del especialista.

## Límites y seguridad

- No se debe escribir ninguna clave API en archivos versionados, argumentos de consola, logs o prompts.
- Una API remota puede recibir el contenido de las tareas y el contexto que se le envía. Antes de habilitarla, configurar qué información puede salir del equipo y aplicar redacción de secretos/datos sensibles.
- La compatibilidad depende del protocolo declarado. Anthropic solo cubre chat; Gemini y OpenAI-compatible cubren chat y embeddings en estos adaptadores.
- La configuración de proveedor no otorga permisos para ejecutar herramientas ni pruebas de seguridad.
- El historial, los vectores locales y las Skills no se transfieren automáticamente al proveedor. Solo se envía el contexto que el ejecutor recupera para la tarea.
- La CLI de administración/descarga de modelos sigue siendo específica de Ollama; la abstracción cubre el flujo de inferencia de agentes y embeddings. No hay descubrimiento automático de modelos remotos: los nombres se configuran explícitamente.

## Pruebas

Ejecutar `python -m unittest tests.test_llm_providers -v` y después la suite completa. La configuración remota debe probarse con un endpoint de prueba y una clave inyectada como variable de entorno, nunca con secretos reales en CI.
