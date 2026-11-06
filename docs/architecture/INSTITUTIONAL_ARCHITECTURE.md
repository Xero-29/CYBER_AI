# CYBER_AI — Arquitectura institucional objetivo

## Propósito
CYBER_AI es una plataforma modular para inventariar activos autorizados, analizar exposición, identificar y verificar vulnerabilidades, apoyar remediación, evaluar resiliencia y producir conocimiento auditable. Incorporar estos contratos no implica estar lista para producción.

## Estados que nunca deben confundirse
- Descubrimiento: se encontró un componente o recurso.
- Validación técnica: se comprobó estructura, versión, dependencias o resultado.
- Confianza: procedencia e integridad suficientes.
- Habilitación: un administrador permite el componente.
- Autorización de ejecución: una política autoriza una acción concreta dentro de alcance y ventana definidos.

Ningún estado implica automáticamente el siguiente.

## Planos
1. Control: identidad, tenants, roles, políticas, alcance, aprobaciones, límites, kill switch y auditoría.
2. Descubrimiento: inventarios de activos, herramientas, agentes, modelos, fuentes y dependencias; solo metadatos.
3. Conocimiento: taxonomía, fuentes, ingestión, procedencia, clasificación, evidencias y relaciones.
4. Análisis: correlación, priorización, revisión de código, configuración y enriquecimiento CVE/CWE/CVSS/EPSS/KEV.
5. Ejecución: adaptadores aislados para escaneo, verificación activa, parcheo y pruebas de resiliencia, sujetos a política.
6. Observabilidad: eventos, métricas, trazas, informes, cadena de custodia y auditoría resistente a alteraciones.

## Extensibilidad
Los componentes se describen mediante `*.component.json` conforme al esquema de `config/component_manifest.schema.json`. `core/plugin_registry.py` valida metadatos; `core/component_discovery.py` construye un inventario. El descubrimiento no importa módulos, no ejecuta entrypoints, no instala dependencias y no concede permisos.

Cada manifiesto declara identidad, versión, tipo, capacidades, dependencias y permisos solicitados. Antes de habilitar un componente en producción se requieren firma/verificación de artefactos, allowlist, SBOM, revisión de código, análisis de dependencias, sandbox, aislamiento de red y aprobación administrativa.

Los modelos Ollama se consultan en tiempo de ejecución mediante `core/model_discovery.py` y `GET /api/tags`. Detectar un modelo no lo aprueba ni lo asigna automáticamente.

## Ciclo de vulnerabilidades
1. Definir organización, activos y alcance.
2. Descubrir pasivamente y normalizar activos.
3. Analizar código, configuraciones y versiones.
4. Enriquecer con fuentes reconocidas y datos versionados.
5. Priorizar por severidad, exposición, explotabilidad y criticidad.
6. Verificar con pruebas mínimas reproducibles dentro del alcance.
7. Solicitar aprobación para explotación, cambios, parches o estrés real.
8. Ejecutar con límites, ventana, respaldo y reversión.
9. Verificar y conservar evidencia antes/después.
10. Cerrar con criterios de aceptación y revisión.

## Autorización
Toda operación activa requiere principal/operador, organización, activo, prueba permitida, alcance, exclusiones, ventana, intensidad máxima, presupuesto de solicitudes, timeout, condiciones de parada, aprobación, respaldo, rollback y referencia de autorización. Acciones de explotación, parcheo y estrés en sistemas reales deben denegarse por defecto cuando falte un control o aprobación (fail closed).

## Requisitos antes de producción
- Autenticación real, MFA y autorización RBAC/ABAC; separación de tenants probada.
- Gestión de secretos fuera del repositorio.
- Firma de artefactos, SBOM, pinning y revisión de dependencias.
- Sandboxes y aislamiento de procesos/red.
- Auditoría con integridad, retención y exportación.
- Política de vulnerabilidades de la propia plataforma.
- Backups y restauración probados, recuperación y rollback.
- CI con lint, tipos, pruebas, SAST, dependencias y secretos.
- Modelos de amenaza, privacidad y controles de acceso.
- Procedimientos, responsables, SLAs, cambios e incidentes.

## Estado
Esta entrega añade contratos iniciales, descubrimiento estático de manifiestos, consulta de modelos locales y taxonomía. No implementa aún runtime seguro de plugins, firma, motor de políticas, autorización multiusuario, sandbox, parcheo orquestado ni estrés seguro. No debe describirse como plataforma certificada o lista para producción.
