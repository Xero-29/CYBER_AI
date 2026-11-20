# Secciones de profundización — Seguridad de datos

## Modelo de amenazas
Trazar datos desde captura hasta borrado: productores, consumidores, ETL, APIs, almacenes, réplicas, logs, backups y terceros. Amenazas: acceso excesivo, fuga por exportación, reidentificación, pérdida de integridad, retención indefinida, exfiltración y uso secundario no autorizado. Incluir metadatos y copias temporales.

## Detección
Auditar consultas, cambios de permisos, exportaciones, descargas masivas, acceso fuera de horario, cambios de clasificación y actividad de cuentas de servicio. Correlacionar sujeto, finalidad, dataset, volumen, destino y aprobación. Detectar desactivación de auditoría y movimiento de datos a ubicaciones no aprobadas.

## Respuesta a incidentes
Contener canal de fuga, revocar accesos y tokens, preservar logs y copias, determinar categorías y sujetos afectados, evaluar exposición de réplicas/backups y coordinar privacidad/legal. Rotar claves cuando corresponda, eliminar copias no autorizadas tras preservación y aplicar retención legal. Validar que la causa raíz no persiste en pipelines.

## Casos prácticos
Un pipeline de analítica copia datos personales a un bucket de desarrollo con acceso amplio. Detectar transferencia, trazar origen y consumidores, restringir acceso, clasificar datos, comprobar logs y backups, aplicar minimización y retención. Repetir con dataset sintético seudonimizado y evaluar riesgo de reidentificación.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST Privacy Framework, NIST SP 800-53, ISO/IEC 27701 y regulación de datos aplicable. Registrar finalidad, jurisdicción y fecha de revisión.
