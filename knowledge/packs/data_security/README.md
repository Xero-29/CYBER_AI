# Seguridad y gobierno de datos — Guía de dominio

**ID:** `data_security` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Protege datos estructurados y no estructurados durante creación, uso, compartición, almacenamiento, backup y eliminación. Considera confidencialidad, integridad, disponibilidad, privacidad, calidad, linaje y soberanía. Clasificación y cifrado no sustituyen controles de acceso ni gobierno de finalidad.

## Competencias
- Inventariar datasets, propietarios, consumidores y linaje.
- Clasificar datos públicos, internos, confidenciales y sensibles.
- Diseñar controles de acceso, cifrado, tokenización y seudonimización.
- Gestionar data loss prevention, retención y borrado.
- Evaluar exposición en logs, backups, analytics, RAG y entrenamiento ML.
- Proteger data lakes, warehouses, object storage y pipelines.
- Medir calidad, integridad y trazabilidad de transformaciones.

## Controles prioritarios
- Minimización y finalidad definida.
- ACL por dataset/columna/fila y segregación de tenants.
- Cifrado en tránsito y reposo con gestión de claves separada.
- Tokenización de identificadores y redacción de campos sensibles.
- DLP contextual y revisión de exportaciones.
- Integridad con hashes, firmas y linaje.
- Retención automática, legal hold y borrado verificable.
- Acceso temporal y recertificación periódica.
- Backups cifrados, aislados y restauración ensayada.

## Metodología
1. Identificar fuentes, sistemas, sujetos y propietarios.
2. Mapear flujos, copias, exportaciones y transferencias.
3. Clasificar sensibilidad y definir propósito/retención.
4. Evaluar amenazas de acceso indebido, corrupción y fuga.
5. Diseñar controles por nivel de dato y contexto.
6. Probar acceso negativo, redacción, cifrado y borrado.
7. Verificar backups, recuperación y consistencia de linaje.
8. Monitorizar acceso anómalo y cambios de permisos.
9. Revisar ante nuevos usos, modelos o proveedores.

## Laboratorio
Dataset sintético con PII ficticia. Aplicar clasificación, masking, RBAC por columna y retención; comprobar que exports, logs y RAG no filtran campos restringidos.

## Evaluación
Cada dataset tiene dueño, clasificación, finalidad, acceso, retención, linaje y evidencia de controles. El borrado y restore se verifican.

## Referencias
NIST Privacy Framework, ISO/IEC 27040, DAMA-DMBOK, OWASP Data Security, NIST SP 800-88 y CIS Controls.

## Instrucciones para agentes IA
No incluyas datos personales reales en fixtures. No exportes datasets completos para probar una hipótesis. Diferencia cifrado, anonimización y seudonimización.

## Arquitectura
Trazar el ciclo de vida del dato desde creación/captura, clasificación, uso, movimiento, almacenamiento, compartición, archivo y eliminación. Identificar productores, consumidores, procesadores, regiones, copias, caches, logs, backups y terceros. Separar plano de gobierno (catálogo, políticas, consentimiento/propósito y retención) del plano de datos (almacenamiento, pipelines, APIs y analítica). Los límites de confianza incluyen exportaciones, replicación, ETL, entornos de desarrollo y herramientas de observabilidad.
