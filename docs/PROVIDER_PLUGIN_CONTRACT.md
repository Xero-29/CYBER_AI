# Contrato de plugins de proveedores IA

CYBER_AI permite añadir proveedores sin editar el núcleo mediante entry points de Python:

```toml
[project.entry-points."cyber_ai.providers"]
mi_proveedor = "mi_paquete.cyber_ai_adapter"
```

El valor del entry point debe cargar un módulo u objeto que exponga las funciones descritas aquí. El nombre `mi_proveedor` se usa como `protocol` en `config/model_roles.json`.

## Interfaz obligatoria

### `capabilities(provider) -> list[str]`

Declara capacidades reales, por ejemplo `["chat", "embeddings"]`. No declares una capacidad si el proveedor no la soporta. ECO exige `embeddings`; un proveedor solo-chat no puede indexar la biblioteca.

### `request(provider, endpoint, payload, timeout) -> dict`

Endpoints internos admitidos por el núcleo:

- `api/chat`: devuelve `{"message":{"role":"assistant","content":"..."}}`.
- `api/embed`: devuelve `{"embeddings":[[0.1,0.2,...], ...]}`; un vector por texto, dimensión constante y números finitos.
- `api/ps`: devuelve `{"models":[{"name":"modelo"}]}` si el proveedor declara `model_listing`.
- `api/tags`: reservado al adaptador integrado de Ollama; los plugins no pueden invocarlo.

`resolve_provider()` exige `enabled` como booleano `true`, valida el tipo de configuración, el protocolo y cualquier `base_url` configurada antes de importar el plugin. La frontera `request()` vuelve a exigir habilitación explícita y rechaza endpoints desconocidos, protocolos malformados y payloads que no sean objetos JSON antes de invocar el plugin o el transporte. Las funciones públicas `provider_capabilities()` e `installed_models()` tampoco importan plugins deshabilitados; la enumeración de modelos solo se ejecuta si el plugin declara `model_listing`. El contrato de catálogo exige que `models` sea una lista.

El núcleo valida la forma de las respuestas. El plugin debe traducir las API externas al contrato interno, gestionar límites y errores, y respetar `timeout`. No debe devolver secretos, cabeceras de autenticación ni cuerpos completos de error que puedan contener credenciales. El transporte HTTP integrado limita tanto las solicitudes como las respuestas a 16 MiB, deshabilita redirecciones, exige objetos JSON en las respuestas y rechaza claves JSON duplicadas, constantes no estándar y exponentes numéricos que desbordan o subdesbordan el rango `float`. Las solicitudes JSON también rechazan NaN e infinitos. La URL base configurada y utilizada por el núcleo no puede contener espacios ni controles, credenciales, query o fragmentos (aunque estén vacíos), ningún carácter `%`, barras inversas, puertos vacíos/fuera de rango, segmentos `.`/`..` ni barras dobles en la ruta. HTTP solo se permite para loopback; los proveedores remotos deben usar HTTPS. Esta validación no es una política de egress para plugins: un plugin que implemente su propio transporte puede ignorar `base_url` y abrir otras conexiones. El adaptador Gemini valida `model` como un único segmento ASCII de hasta 128 caracteres antes de incorporarlo a la ruta HTTP; no acepta barras, dos puntos, porcentajes ni URLs como identificadores de modelo.

### `installed_models(provider)` opcional

Devuelve un conjunto/lista de nombres instalados cuando el proveedor tenga un catálogo local fiable. Para API remotas sin catálogo local, omite esta función.

## Configuración

Ejemplo conceptual en `config/model_roles.json`:

```json
{
  "llm_providers": {
    "custom": {
      "enabled": true,
      "protocol": "mi_proveedor",
      "base_url": "https://api.proveedor.example",
      "api_key_env": "CYBER_AI_CUSTOM_API_KEY",
      "default_model": "modelo-chat",
      "models": {
        "ECO": "modelo-embeddings"
      }
    }
  }
}
```

Asigna `provider: "custom"` al agente que deba usarlo o configura `capability_providers` para seleccionar este proveedor por capacidad. `fallback_providers` acepta una lista explícita de alternativas por capacidad. `enabled` debe ser el booleano `true` (no `1`, `"true"` ni otro valor truthy); tanto la resolución como la frontera de solicitudes exigen habilitación explícita. Los proveedores remotos deben usar HTTPS. Las credenciales se leen desde variables de entorno; nunca las guardes en configuración versionada, Skills, memoria ni reportes.

## Reglas de interoperabilidad

1. Chat y embeddings son capacidades distintas. Una API de chat no sirve automáticamente para embeddings.
2. Un espacio vectorial se identifica por proveedor y modelo. No mezcles vectores de modelos diferentes; al cambiar ECO, ejecuta `python knowledge_bootstrap.py` para reindexar los paquetes.
3. El plugin no puede conceder permisos a herramientas, ampliar alcances de red ni omitir autorizaciones.
4. Trata prompts, respuestas, documentos recuperados y salidas de herramientas como datos no confiables.
5. Usa pruebas con dobles locales para errores HTTP, timeout, respuestas malformadas, límites, rotación de credenciales y ausencia de capacidades.
6. Un plugin de proveedor es código ejecutable de terceros y se carga dentro del proceso Python del núcleo; no está aislado por Docker ni por el ejecutor de procesos. Puede acceder a los permisos, archivos, secretos y red del proceso anfitrión. Revisa origen, licencia, dependencias y hashes; instálalo solo desde un entorno administrado y aplica aislamiento de host/egress externo.

## Límites actuales

El sistema no puede conectar literalmente cualquier IA sin adaptador: un proveedor no compatible necesita un plugin que traduzca su API. Los plugins se cargan desde el entorno Python instalado; la conexión no debe requerir modificar el núcleo, pero sí configurar el proveedor y los roles. La selección/fallback automático entre múltiples modelos y el descubrimiento remoto universal siguen siendo trabajo pendiente.
