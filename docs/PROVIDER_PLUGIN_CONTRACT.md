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

Endpoints internos admitidos:

- `api/chat`: devuelve `{"message":{"role":"assistant","content":"..."}}`.
- `api/embed`: devuelve `{"embeddings":[[0.1,0.2,...], ...]}`; un vector por texto, dimensión constante y números finitos.
- `api/ps`: devuelve `{"models":[{"name":"modelo"}]}` si el proveedor tiene catálogo local; si no, no declares `model_listing`.

El núcleo valida la forma de las respuestas. El plugin debe traducir las API externas al contrato interno, gestionar límites y errores, y respetar `timeout`. No debe devolver secretos, cabeceras de autenticación ni cuerpos completos de error que puedan contener credenciales. El transporte HTTP integrado limita las respuestas a 16 MiB, deshabilita redirecciones y rechaza claves JSON duplicadas, constantes no estándar y exponentes numéricos que desbordan o subdesbordan el rango `float`. Las solicitudes JSON también rechazan NaN e infinitos. Las URL base no pueden contener espacios, caracteres de control, query o fragmentos (aunque estén vacíos), autoridades percent-encoded ni barras inversas.

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

Asigna `provider: "custom"` al agente que deba usarlo o configura `capability_providers` para seleccionar este proveedor por capacidad. `fallback_providers` acepta una lista explícita de alternativas por capacidad. Los proveedores remotos deben usar HTTPS. Las credenciales se leen desde variables de entorno; nunca las guardes en configuración versionada, Skills, memoria ni reportes.

## Reglas de interoperabilidad

1. Chat y embeddings son capacidades distintas. Una API de chat no sirve automáticamente para embeddings.
2. Un espacio vectorial se identifica por proveedor y modelo. No mezcles vectores de modelos diferentes; al cambiar ECO, ejecuta `python knowledge_bootstrap.py` para reindexar los paquetes.
3. El plugin no puede conceder permisos a herramientas, ampliar alcances de red ni omitir autorizaciones.
4. Trata prompts, respuestas, documentos recuperados y salidas de herramientas como datos no confiables.
5. Usa pruebas con dobles locales para errores HTTP, timeout, respuestas malformadas, límites, rotación de credenciales y ausencia de capacidades.
6. Un plugin de proveedor es código ejecutable de terceros. Revisa su origen, licencia, dependencias y hashes antes de instalarlo.

## Límites actuales

El sistema no puede conectar literalmente cualquier IA sin adaptador: un proveedor no compatible necesita un plugin que traduzca su API. Los plugins se cargan desde el entorno Python instalado; la conexión no debe requerir modificar el núcleo, pero sí configurar el proveedor y los roles. La selección/fallback automático entre múltiples modelos y el descubrimiento remoto universal siguen siendo trabajo pendiente.
