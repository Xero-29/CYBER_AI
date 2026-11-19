# Revisión de fuentes primarias y correcciones disciplinares — Foundations

**Fecha de revisión:** 2026-11-19  
**Rama:** `knowledge/develop-foundations`  
**Estado:** revisión de secciones pertinentes y síntesis crítica; no equivale a revisión sistemática ni revisión externa.

## 1. Método y límites

Se consultaron las versiones oficiales disponibles y se inspeccionaron el texto PDF/HTML de las secciones indicadas. El estado `selected_sections_reviewed` significa que se leyeron secciones pertinentes y se registró su alcance; no significa lectura lineal completa. Los experimentos de este módulo son simulaciones deterministas de propiedades acotadas, no evidencia de eficacia en producción ni generalización poblacional.

## 2. Fuentes primarias revisadas y extracción

### S1 — NIST SP 800-160 Vol. 1 Rev. 1 (2022)
- URL canónica: https://doi.org/10.6028/NIST.SP.800-160v1r1
- Artefacto: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf
- Secciones inspeccionadas: abstract y autoridad; marco de ingeniería de sistemas seguros (pp. 32–36); assurance case (pp. 35–36 y apéndice F); desarrollo de requisitos de seguridad y distinción requisito/política/mecanismo (apéndice C.2–C.3); principios de diseño (apéndice D); tailoring y procesos del ciclo de vida (apéndices H–K).
- Hallazgos aplicados:
  1. El framework de Systems Security Engineering se compone de contextos que interactúan; no es un flujo lineal universal.
  2. Los requisitos de seguridad incluyen capacidades, comportamiento, calidad, procesos de assurance y evidencia requerida.
  3. Requisito, política y mecanismo son conceptos distintos: el requisito especifica capacidad/comportamiento; la política define comportamiento en contexto operacional; el mecanismo lo realiza.
  4. Los procesos deben adaptarse al contexto, complejidad, tecnología y recursos, sin perder resultados/evidencia.
- Corrección aplicada: el Tema 1 separa política/mecanismo/enforcement; el Tema 7 exige evidencia del control; el Tema 1 y la sección de ciclo de vida distinguen procesos iterativos de una secuencia rígida.
- Límite: no se declara lectura lineal de las 195 páginas.

### S2 — NIST SP 800-30 Rev. 1 (2012)
- URL canónica: https://doi.org/10.6028/NIST.SP.800-30r1
- Artefacto: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf
- Secciones inspeccionadas: marco/modelo de evaluación; identificación de fuentes y eventos; vulnerabilidades y condiciones predisponentes; probabilidad de iniciación/ocurrencia y probabilidad de impacto; impacto; determinación/comunicación del riesgo; tratamiento de incertidumbre y supuestos (cap. 2, cap. 3 y apéndices pertinentes).
- Hallazgos aplicados:
  1. Amenazas adversariales y eventos no adversariales deben tratarse de forma diferenciada.
  2. La probabilidad de un evento dañino puede descomponerse en iniciación/ocurrencia y probabilidad de impacto, condicionada por vulnerabilidades y condiciones predisponentes.
  3. NIST no prescribe un algoritmo universal para combinar escalas semicuantitativas; el modelo y sus reglas dependen de la organización y deben explicitarse.
  4. Riesgo incluye impacto y probabilidad, pero también incertidumbre, supuestos, restricciones y tolerancia. La incertidumbre se propaga desde factores individuales a la evaluación final; debe documentarse y tratarse, no ocultarse en una cifra puntual.
- Corrección aplicada: Tema 3 incluye fallos no adversariales y dependencias; Tema 7 prohíbe tratar matrices 5×5 como magnitudes cardinales o fórmulas universales.
- Límite: no se declara lectura lineal de las 95 páginas.

### S3 — NIST SP 800-37 Rev. 2 (2018)
- URL canónica: https://doi.org/10.6028/NIST.SP.800-37r2
- Artefacto: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf
- Secciones inspeccionadas: introducción; Prepare; Categorize; Select; Implement; Assess; Authorize; Monitor; integración de privacidad, ciclo de vida y supply-chain risk management.
- Hallazgos aplicados:
  1. El RMF se organiza en siete pasos: Prepare, Categorize, Select, Implement, Assess, Authorize y Monitor.
  2. La autorización es una decisión de autoridad responsable con un paquete de riesgo/evidencia; no es un simple estado automático del sistema.
  3. Monitor requiere observar cambios del sistema/entorno y evaluaciones continuas.
  4. Prepare-System incluye identificar misión, stakeholders, ciclo de vida de información, evaluación de riesgo y requisitos de seguridad/privacidad priorizados; el plan de monitoreo debe adaptarse a volatilidad y criticidad de controles.
  4. Los controles comunes, heredados y específicos necesitan responsables y evidencia de implantación/eficacia.
- Corrección aplicada: Tema 7 explicita el ciclo y los roles; se separa assessment de aceptación del riesgo.
- Límite: no se declara lectura lineal de las 183 páginas.

### S4 — NIST SP 800-61 Rev. 3 (2025)
- URL canónica: https://doi.org/10.6028/NIST.SP.800-61r3
- Artefacto: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
- Secciones inspeccionadas: abstract, sección 2 y modelo de ciclo de vida; roles y responsabilidades; relación de las funciones CSF 2.0 con preparación, detección, respuesta, recuperación y mejora.
- Hallazgos aplicados:
  1. La respuesta a incidentes está integrada en la gestión de riesgo y no es una actividad aislada del SOC.
  2. Govern, Identify y Protect soportan preparación; Detect, Respond y Recover articulan la respuesta; Improvement alimenta continuamente las funciones.
  3. La respuesta depende de múltiples roles internos y externos, incluyendo dirección, tecnología, legal y proveedores.
  4. Rev. 3 sustituye Rev. 2 (2012).
- Corrección aplicada: Tema 6 se alinea al modelo CSF 2.0 y evita presentar una cadena lineal de cuatro fases como modelo universal.
- Límite: no se declara lectura lineal de las 48 páginas.

### S5 — NIST SP 800-88 Rev. 2 (2025)
- URL canónica: https://doi.org/10.6028/NIST.SP.800-88r2
- Artefacto: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf
- Secciones inspeccionadas: autoridad, alcance, executive summary; métodos de sanitización; uso de criptografía y cryptographic erase (sec. 3.2); programa general y sanitization validation (sec. 4.5.2).
- Hallazgos aplicados:
  1. La sanitización es un programa de gobierno y aseguramiento, no solo ejecutar un comando de borrado.
  2. La selección depende de sensibilidad, reutilización/disposición, medio y confianza en la implementación del proveedor.
  3. La validación de sanitización decide aprobar o rechazar la eficacia y puede exigir repetir con otra técnica o escalar a método más seguro; no es lo mismo que comprobar que el comando terminó sin error.
  4. La revisión reemplaza SP 800-88 Rev. 1 (2014); no se debe usar la edición antigua como fuente vigente. Cryptographic erase depende de la procedencia/calidad de la criptografía, generación de claves, protección y condiciones previas; no es un botón mágico.
- Corrección aplicada: Tema 2 incorpora ciclo de vida de retiro/sanitización y evidencia del proveedor; el inventario conserva el estado de disposición.
- Límite: se inspeccionaron secciones pertinentes; no lectura lineal completa.

### S6 — IETF RFC 9700 / BCP 240 (enero 2025)
- URL canónica: https://www.rfc-editor.org/rfc/rfc9700.html
- Texto: https://www.rfc-editor.org/rfc/rfc9700.txt
- Secciones inspeccionadas: 2.1–2.6, modelo de atacante y secciones 4.1–4.17 sobre ataques/mitigaciones; en particular redirect validation, PKCE, token replay, sender constraint, audience restriction y refresh-token protection.
- Hallazgos aplicados:
  1. Redirect URI debe compararse exactamente, con excepción acotada para puertos localhost de aplicaciones nativas.
  2. Clientes públicos deben usar PKCE; S256 evita exponer el verifier en la solicitud.
  3. El implicit grant no debe usarse como opción normal; el flujo authorization code reduce exposición de tokens en URL.
  4. Sender-constrained tokens (mTLS/DPoP) reducen replay, pero no protegen si atacante obtiene token y material de clave o compromete el cliente.
  5. Refresh-token rotation debe detectar reutilización de tokens invalidados; requiere conservar relación de familia/estado.
- Corrección aplicada: Tema 4 agrega requisitos concretos, ataques, condiciones y límites de OAuth 2.0; se evita tratar validación de claims como sustituto de verificación de firma.
- Límite: RFC completo disponible y consultado; la implementación real de protocolos queda fuera de este laboratorio.

### S7 — NIST CSWP 29, CSF 2.0 (2024)
- URL canónica: https://doi.org/10.6028/NIST.CSWP.29
- Artefacto: https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
- Secciones inspeccionadas: propósito, estructura de Core, Profiles y Tiers, y relación con gestión de riesgo.
- Hallazgos aplicados: CSF describe resultados y lenguaje común; no prescribe por sí mismo una única implementación, no es una certificación automática y los perfiles deben adaptarse al contexto.
- Corrección aplicada: Temas 2, 6 y 7 separan resultado de marco, control implementado y evidencia de eficacia.
- Límite: secciones pertinentes revisadas, no lectura lineal completa.

### S8 — NIST FIPS 204 y FIPS 205 (2024)
- FIPS 204: https://doi.org/10.6028/NIST.FIPS.204
- FIPS 205: https://doi.org/10.6028/NIST.FIPS.205
- Secciones inspeccionadas: portada, abstract, anuncio de estándar, aplicabilidad y descripción de uso de firmas.
- Hallazgos aplicados: ML-DSA (FIPS 204) y SLH-DSA (FIPS 205) son algoritmos de firma digital post-cuántica; no son KEM ni cifrado de datos.
- Corrección aplicada: Tema 5 separa firma digital de establecimiento de claves y remite ML-KEM a FIPS 203.
- Límite: no se declara lectura completa de los algoritmos ni validación de implementación. FIPS 203 fue contrastado en la ficha oficial y su aviso de errata, pero no se pudo inspeccionar el PDF íntegro en esta sesión.

### S9 — NIST SP 800-53 Release 5.2.0 (2025)
- Página: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- Aviso oficial: https://csrc.nist.gov/news/2025/nist-releases-revision-to-sp-800-53-controls
- Hallazgo: Release 5.2.0 incorpora nuevos controles y revisiones relacionadas con ingeniería/desarrollo, pruebas, resiliencia, actualizaciones e integridad de software. Los crosswalks no prueban equivalencia uno a uno.
- Corrección aplicada: mantener referencia de versión y evitar citar la ficha de 2020 como si no hubiera actualizaciones.
- Límite: se revisó anuncio y registro de publicación; no el catálogo completo de controles 5.2.0.

### S10 — MITRE ATT&CK v20.1 (13 de octubre de 2026)
- Versiones: https://attack.mitre.org/resources/versions/
- Cambios: https://attack.mitre.org/resources/updates/
- Hallazgo: el catálogo es versionado; v20.1 es la versión actual en la fecha de revisión. ATT&CK representa conocimiento de tácticas/técnicas observadas; no aporta por sí solo probabilidad, cobertura completa ni prueba de aplicabilidad al sistema.
- Corrección aplicada: Tema 3 obliga a registrar versión/fecha y usar ATT&CK como taxonomía contextual, no como puntuación de riesgo.
- Límite: se revisó el registro de versiones y changelog, no todos los objetos del catálogo.

### S11 — OWASP ASVS 5.0.0 (30 de mayo de 2025)
- URL: https://asvs.owasp.org/
- Descargas: https://asvs.owasp.org/downloads/
- Hallazgo: ASVS 5.0.0 es la versión estable publicada y sirve para especificar/verificar requisitos técnicos de aplicaciones web y servicios web; no es un estándar general de inventario, riesgo empresarial o gobierno.
- Corrección aplicada: su uso queda limitado al contexto de verificación de aplicación, sin atribuirle alcance universal.
- Límite: se revisó página oficial y versión, no el conjunto completo de requisitos CSV/PDF.

### S12 — NIST SP 800-57 Part 1 Rev. 5 (2020), ficha oficial
- URL: https://doi.org/10.6028/NIST.SP.800-57pt1r5
- Hallazgo: guía de gestión de material criptográfico, tipos de claves, protección, funciones, recuperación y períodos de uso.
- Límite: ficha y abstract inspeccionados; el PDF completo no pudo recuperarse en esta sesión. No se marca lectura integral.

## 3. Correcciones técnicas obligatorias en los siete temas

1. **Tema 1:** modelo de confianza como sistema de contextos y enforcement; no equiparar Zero Trust con RBAC/ABAC; separar requisito, política y mecanismo; incluir bypass, revocación y consistencia.
2. **Tema 2:** añadir ciclo de vida de activos, recursos efímeros, procedencia, confianza de matching, fuentes correlacionadas y sanitización de retiro según SP 800-88r2.
3. **Tema 3:** separar amenaza adversarial/no adversarial; DFD/attack graph complementan STRIDE y ATT&CK; ATT&CK se fija por versión y no representa probabilidad.
4. **Tema 4:** agregar exact redirect URI, PKCE S256, desaconsejar implicit grant, validar issuer/audience/expiry/scope/nonce/state/firma según protocolo y explicar límites de sender-constrained/refresh rotation.
5. **Tema 5:** diferenciar AES (cifrado simétrico), HMAC (integridad/autenticidad), firmas (FIPS 204/205), KEM (FIPS 203) y gestión de claves (SP 800-57). No afirmar que HMAC cifra ni que ML-DSA/SLH-DSA establecen claves.
6. **Tema 6:** sustituir ciclo aislado de IR por integración CSF 2.0 de seis funciones y mejora continua, conforme SP 800-61r3.
7. **Tema 7:** usar RMF de siete pasos, modelo explícito de riesgo, reglas de combinación y autoridad formal; no presentar escalas ordinales como probabilidades cardinales.

## 4. Matriz afirmación → fuente → capa

| Afirmación o decisión | Fuente/sección | Tema/capa | Estado |
|---|---|---|---|
| Requisito, política y mecanismo son distintos | SP 800-160r1, apéndice C.3 | 1/L1-L4, 7/L3-L5 | Revisado |
| SSE es un marco de contextos interactivos, no un flujo rígido | SP 800-160r1, marco SSE | 1/L3-L6 | Revisado |
| Riesgo distingue evento, vulnerabilidad, probabilidad de iniciación/ocurrencia, impacto e incertidumbre | SP 800-30r1, cap. 3 y apéndices D-I | 3/L1-L6, 7/L1-L6 | Revisado |
| No existe algoritmo universal NIST para escalas semi-cuantitativas | SP 800-30r1, preparación/modelo de riesgo | 7/L2-L6 | Revisado |
| RMF contiene Prepare/Categorize/Select/Implement/Assess/Authorize/Monitor | SP 800-37r2, cap. 3 | 7/L3-L5 | Revisado |
| IR se integra con seis funciones CSF 2.0 y mejora continua | SP 800-61r3, sec. 2 | 6/L1-L5 | Revisado |
| Redirect URI exacta, PKCE, sender constraint y refresh rotation | RFC 9700, sec. 2 y 4 | 4/L3-L7 | Revisado |
| Sanitización es programa con assurance y selección por sensibilidad/medio | SP 800-88r2 | 2/L4-L6, 5/L7-L12 | Revisado |
| ML-DSA/SLH-DSA son firmas; ML-KEM es KEM | FIPS 204/205; FIPS 203 ficha oficial | 5/L1-L5 | Parcial (FIPS 203 ficha) |
| ATT&CK versionado; v20.1 vigente en corte | MITRE version history/changelog | 3/L4-L5, L12 | Revisado |
| ASVS 5.0.0 es verificación de seguridad de aplicaciones web | OWASP ASVS 5.0.0 | 3/L4, 7/L4 | Metadata/version reviewed |

## 5. Resultado de experimentación sintética

Los siete protocolos se implementaron como harness local determinista en:
- `knowledge/deep_modules/foundations/labs/runner.py`
- `tests/test_foundations_labs.py`
- salida: `knowledge/deep_modules/foundations/labs/results.json`

Semilla fija: 20261119. Ocho pruebas unitarias pasan en la ejecución local del harness. Los resultados sintéticos y límites se documentan en `labs/README.md`.

**No inferir de estos resultados:** eficacia en producción, probabilidad real de incidentes, rendimiento general, seguridad criptográfica de una implementación, validez externa, ni aprobación de G5-G8. El laboratorio 4 solo simula validación de claims y no verifica firmas JWT. El laboratorio 5 usa HMAC-SHA-256 para integridad/autenticidad; no cifra ni valida AES/FIPS/KMS. El laboratorio 3 verifica rutas modeladas, no explotación. Ninguno ejecuta sanitización de medios, assurance case independiente ni RMF organizacional real.

## 6. Brechas que siguen abiertas

- Lectura integral y extracción por sección de fuentes adicionales, especialmente SP 800-57, catálogo 800-53 5.2.0 y FIPS 203.
- Incorporar referencias específicas para inventario y clasificación (por ejemplo, controles/estándares aplicables al entorno) y legislación colombiana por sector, con análisis jurídico competente.
- Ampliar datasets: el dataset de activos actual es sintético y generado, no una muestra representativa.
- Revisión de los escenarios de threat modeling por dos evaluadores independientes.
- Implementaciones reales aisladas de protocolos/controles (IdP, KMS, SIEM) y pruebas de interoperabilidad.
- Reproducción en un segundo entorno/runner independiente.
- Revisión externa de un especialista; no disponible en esta iteración.

**Dictamen:** fuentes primarias seleccionadas revisadas y cambios técnicos trazados; siete pruebas sintéticas locales reproducibles. Madurez permanece M2. G5-G7 pasan a `in_progress`, no `passed`; G8 permanece `blocked`. No K3/K4/K5 ni validación científica.
