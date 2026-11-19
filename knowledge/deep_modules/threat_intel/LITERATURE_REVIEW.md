# Revisión de literatura — threat_intel

**Corte editorial:** 2026-11-19  
**Estado:** revisión exploratoria de fuentes registradas y alcance oficial; no revisión sistemática ni lectura integral de todas las fuentes.  
**Madurez:** M2 editorial como máximo; M3/M4/M5 pendientes.

## Pregunta

¿Qué métodos producen inteligencia accionable, calibrada y trazable, y reducen errores de correlación, caducidad y atribución?

## Síntesis crítica inicial

ATT&CK es una base de conocimiento de tácticas y técnicas basada en observaciones; debe fijarse versión y modelo de datos. Sus releases recientes cambiaron conceptos defensivos y requieren migrar contenido antiguo de detección cuando corresponda. STIX estructura objetos y relaciones; TAXII transporta colecciones; MISP soporta intercambio y correlación. Ninguno elimina la necesidad de revisar procedencia, markings, expiración y contexto. CISA KEV identifica vulnerabilidades explotadas conocidas; EPSS estima probabilidad de explotación en una ventana temporal y no debe confundirse con impacto ni criticidad local. La atribución requiere hipótesis rivales, evidencia multi-fuente y confianza explícita; una coincidencia ATT&CK o IOC no prueba identidad del actor.

## Fuentes primarias y técnicas que orientan el módulo

MITRE ATT&CK (https://attack.mitre.org/), ATT&CK STIX data (https://github.com/mitre-attack/attack-stix-data), CISA KEV (https://www.cisa.gov/known-exploited-vulnerabilities-catalog), FIRST EPSS (https://www.first.org/epss/).

## Identificadores del registro de fuentes

- `MITRE-ATTACK-STIX-DATA`
- `MITRE-ATTACK-V18-RELEASE`
- `MITRE-ATTACK-VERSION-HISTORY`
- `CISA-KEV`
- `FIRST-EPSS-FAQ`
- `FIRST-EPSS-METHOD`

## Límites de esta revisión

- Los identificadores anteriores acreditan que existe una referencia en el registro; no demuestran lectura íntegra.
- No se afirma evaluación de conformidad, certificación ni validación de producto.
- Las afirmaciones normativas deben comprobarse contra edición, erratas, jurisdicción y fecha vigentes.
- Las taxonomías y guías organizan el análisis; no sustituyen evidencia observada.
- No se ha ejecutado el protocolo experimental ni se han obtenido resultados confirmatorios.

## Brechas de investigación

1. Recuperar texto completo de cada fuente primaria y registrar páginas/secciones efectivamente leídas.
2. Extraer requisitos y afirmaciones concretas con vínculo a subtema y criterio de prueba.
3. Incorporar estudios empíricos revisados por pares con criterios de inclusión/exclusión reproducibles.
4. Contrastar recomendaciones, contradicciones, supuestos y limitaciones entre fuentes.
5. Ejecutar protocolos con corpus autorizado, ground truth, controles negativos y resultados brutos.
6. Someter el análisis a revisión independiente y registrar correcciones.

**Conclusión limitada:** esta revisión constituye un mapa inicial de literatura y fuentes. No permite afirmar exhaustividad documental ni madurez científica superior a M2.
