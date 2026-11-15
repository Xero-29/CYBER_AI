# Inteligencia de amenazas — Guía de dominio

**ID:** `threat_intel` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Convierte información sobre amenazas en decisiones defensivas oportunas y trazables. La inteligencia debe responder una pregunta operativa: qué proteger, qué detectar, qué priorizar y qué cambiar. No es una colección de IOCs ni una lista de actores. La atribución es probabilística y no debe presentarse como certeza sin evidencia suficiente.

## Fuentes y modelo
Fuentes posibles: telemetría propia, CERT/CSIRT, advisories de fabricantes, CVE/NVD, CISA KEV, FIRST EPSS, ISAC, repositorios de malware, informes públicos y fuentes OSINT. Registrar origen, fecha de observación/publicación, método, confianza, licencias y restricciones de redistribución. Distinguir inteligencia estratégica, operacional, táctica y técnica.

## Competencias específicas
- Formular requisitos de inteligencia (PIR/IR) con propietario y decisión esperada.
- Evaluar fiabilidad de fuente y credibilidad de información.
- Normalizar indicadores y relaciones en STIX/TAXII.
- Mapear TTP a MITRE ATT&CK y controles D3FEND.
- Correlacionar campañas, infraestructura, vulnerabilidades y sectores.
- Calcular vigencia y confianza de IOCs; evitar bloquear indicadores caducados.
- Producir alertas, informes y recomendaciones accionables.
- Proteger fuentes, privacidad y datos de terceros.

## Controles y calidad
- Registrar procedencia y licencia por cada dato.
- No fusionar observación con inferencia ni atribución.
- Añadir timestamps, zona horaria, confianza y expiración a IOCs.
- Validar indicadores contra múltiples fuentes cuando sea posible.
- Evitar listas de bloqueo sin contexto y riesgo de falsos positivos.
- Redactar datos personales y secretos.
- Mantener control de acceso, retención y trazabilidad de consultas.
- Medir valor por decisiones y detecciones mejoradas, no por volumen.

## Metodología
1. Definir pregunta, audiencia, horizonte y decisión.
2. Recopilar fuentes autorizadas y registrar metadatos.
3. Normalizar entidades, observables, TTP y relaciones.
4. Evaluar fiabilidad, corroboración y vigencia.
5. Mapear a ATT&CK y superficie propia.
6. Identificar brechas de detección y exposición.
7. Proponer acción con prioridad, confianza y fecha de expiración.
8. Distribuir en formato apropiado y registrar feedback.
9. Revisar indicadores obsoletos y retirar los que no sean válidos.

## Laboratorio seguro
Usar feeds públicos con licencia compatible y datos sintéticos STIX. Crear un informe que relacione TTP con reglas de detección sobre logs ficticios. No descargar muestras ni consultar infraestructura hostil desde entornos productivos.

## Evaluación
Cada producto responde a un requisito, cita fuentes, marca confianza y vigencia, y propone una acción comprobable. Se mide utilidad por reducción de tiempo de detección o exposición.

## Referencias y herramientas
MITRE ATT&CK, D3FEND, STIX 2.1, TAXII 2.1, FIRST EPSS, CISA KEV, MISP y OpenCTI.

## Instrucciones para agentes IA
No atribuyas campañas por similitud superficial. Marca fecha y confianza. No copies fuentes restringidas a la biblioteca compartida ni conviertas IOCs sin contexto en reglas de bloqueo.