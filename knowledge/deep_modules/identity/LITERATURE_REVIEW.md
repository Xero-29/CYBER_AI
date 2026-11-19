# Revisión de literatura — identity

**Corte editorial:** 2026-11-19  
**Estado:** revisión exploratoria de fuentes registradas y alcance oficial; no revisión sistemática ni lectura integral de todas las fuentes.  
**Madurez:** M2 editorial como máximo; M3/M4/M5 pendientes.

## Pregunta

¿Qué combinación de ciclo de vida, autenticación resistente a phishing, federación y autorización reduce accesos indebidos sin crear fallos inaceptables de disponibilidad o usabilidad?

## Síntesis crítica inicial

NIST SP 800-63-4 reorganiza las guías de identidad digital en prueba de identidad, autenticación/gestión de autenticadores y federación/assertions. La arquitectura debe seleccionar niveles y controles según riesgo, no asumir que MFA equivale a identidad confiable. SP 800-63B-4 trata autenticadores y autenticación; SP 800-63C-4 trata federación y assertions. SP 800-207 aporta el enfoque Zero Trust, donde la confianza no se concede por ubicación de red y la decisión de acceso considera sujeto, dispositivo, recurso y contexto. RFC 9700 recoge prácticas actuales de seguridad para OAuth 2.0; complementa, pero no sustituye, los perfiles OIDC/SAML ni la validación de implementación. La lectura de metadatos y alcances oficiales no demuestra que se hayan revisado todas las cláusulas ni que un IdP cumpla los requisitos.

## Fuentes primarias y técnicas que orientan el módulo

NIST SP 800-63-4 (https://doi.org/10.6028/NIST.SP.800-63-4), NIST SP 800-63B-4 (https://doi.org/10.6028/NIST.SP.800-63b-4), NIST SP 800-63C-4 (https://doi.org/10.6028/NIST.SP.800-63c-4), NIST SP 800-207 (https://doi.org/10.6028/NIST.SP.800-207), RFC 9700 (https://www.rfc-editor.org/rfc/rfc9700).

## Identificadores del registro de fuentes

- `NIST-SP-800-63-4`
- `NIST-SP-800-63B-4`
- `NIST-SP-800-63C-4`
- `NIST-SP-800-207`
- `NIST-SP-800-53r5`
- `IETF-RFC9700`

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
