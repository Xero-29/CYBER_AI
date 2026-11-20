# Secciones de profundización — Ingeniería de privacidad

## Modelo de amenazas
Trazar datos personales y derivados desde captura hasta eliminación: sistemas, procesadores, analítica, logs, backups, transferencias y terceros. Amenazas: reidentificación, uso secundario, acceso excesivo, retención indebida, linkage, filtración y pérdida de derechos. Definir finalidad, base legal, población, sensibilidad y jurisdicción.

## Detección
Auditar accesos, exportaciones, cambios de finalidad, consentimientos, transferencias, retención y solicitudes de titulares. Detectar consultas masivas, uso fuera de propósito, datos en entornos de desarrollo y fallos de eliminación. Medir minimización, cumplimiento de retención, tiempos de derechos y exposición residual.

## Respuesta a incidentes
Contener el flujo, preservar evidencia mínima, identificar categorías y sujetos afectados, evaluar riesgo de privacidad, notificar según ley aplicable y coordinar responsable/encargado. Revocar accesos, corregir pipeline, eliminar copias indebidas cuando proceda y documentar base legal, decisiones y plazos.

## Casos prácticos
Un pipeline copia datos personales a un entorno analítico sin necesidad. Usar dataset sintético, trazar campos y finalidad, aplicar minimización/seudonimización, revisar logs y backups y probar eliminación. Evaluar si los datos derivados permiten reidentificación y documentar riesgo residual.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para NIST Privacy Framework, ISO/IEC 27701, GDPR y legislación local aplicable. La obligación depende de jurisdicción, rol y contexto.
