# Auditoría de profundidad de compendios — 2026-11-19

**Rama auditada:** `knowledge/develop-foundations`  
**Base:** commit `6ae2b4a9292e2ddea6ea4c7c196652143ee14e9f`  
**Alcance:** inspección automatizada/manual de los 48 archivos `TECHNICAL_COMPENDIUM.md`, con lectura del estándar, tracker, agenda y muestras de contenido.  
**Estado:** diagnóstico editorial preliminar; no es revisión disciplinar independiente ni validación científica.

## 1. Resultado ejecutivo

Los 48 compendios existen y contienen ampliaciones específicas, pero **no se puede concluir que las 48 áreas tengan profundidad experta**. La evidencia actual es desigual:

- 48/48 archivos fueron recuperados y examinados en esta auditoría.
- Los tamaños observados van aproximadamente de 10.7 kB a 31 kB. El tamaño no es una métrica de profundidad.
- Fundamentos, AppSec y API muestran estructuras más extensas y laboratorios/casos más concretos en la inspección realizada.
- 37 áreas adicionales muestran encabezados disciplinares específicos y una estructura técnica diferenciada; esto prueba especialización editorial, no que cada mecanismo esté explicado con rigor suficiente.
- Ocho áreas contenían un bloque repetido de siete apartados genéricos: `mobile`, `crypto`, `identity`, `malware`, `forensics`, `incident_response`, `threat_intel` y `reverse`. Las ocho han recibido sustitución editorial de los bloques genéricos; esto no demuestra profundidad experta ni validación.
- La agenda de investigación de 48 áreas mantiene hipótesis y diseños propuestos, no resultados.
- El tracker reconoce fuentes integrales, laboratorios ejecutados y revisión independiente como pendientes.

## 2. Método y límites

Se inspeccionaron los 48 compendios mediante recuperación del archivo completo, recuento de caracteres, extracción de encabezados y búsqueda de un patrón textual repetido. Se leyeron con mayor detalle el estándar normativo, el tracker, la agenda y muestras representativas (Fundamentos, AppSec, API, red, Linux, Windows/AD, cloud, contenedores, móvil, criptografía, identidad, malware y otros).

Este método detecta ausencias estructurales y texto plantilla, pero **no demuestra** corrección técnica, exhaustividad temática, vigencia de cada afirmación ni profundidad K1–K5. Tampoco sustituye una lectura de cada línea por un especialista. La inspección de encabezados no debe confundirse con revisión del contenido completo de cada tema.

## 3. Hallazgos concretos

### H1 — Desigualdad de profundidad
**Estado:** confirmado como hallazgo editorial.

La profundidad no es uniforme. Algunos módulos presentan modelos, procedimientos y laboratorios detallados; otros consisten en una base común más un apéndice temático relativamente corto. Debe medirse por unidad temática y no por longitud total del archivo.

### H2 — Bloques plantilla en ocho áreas
**Estado:** confirmado por coincidencia textual.

En las ocho áreas enumeradas se repite siete veces el mismo patrón genérico de explicación. Aunque el texto define qué debe cubrir un tema, no desarrolla los detalles disciplinares. Debe reemplazarse cada repetición con contenido técnico propio del tema: modelos, variantes, protocolos, algoritmos, comandos, casos límite, resultados esperados y contraejemplos.

### H3 — Agenda de investigación transversal demasiado abstracta en el diseño experimental
**Estado:** confirmado en la matriz central.

En muchas entradas el diseño mínimo usa una formulación común (“definir baseline y dataset/topología/controlado, variar una dimensión…”). Sirve como recordatorio de método, pero no constituye protocolo ejecutable. Cada área necesita variables, unidad de análisis, corpus, criterios de inclusión/exclusión, baseline real, tamaño de muestra justificado, controles y análisis propios.

### H4 — Evidencia primaria y validación experimental aún no demostradas
**Estado:** explícito en el tracker y manifiesto.

No hay base para declarar lectura integral de las 102 referencias registradas, laboratorios ejecutados, revisión independiente ni reproducción externa. No asignar K4/K5 por el hecho de que el compendio o la agenda existan.

### H5 — Necesidad de granularidad por tema
**Estado:** brecha de diseño prioritaria.

La estructura actual es mayormente un documento por especialidad. El estándar requiere trazabilidad por tema: fuente → afirmación → mecanismo → amenaza → control → procedimiento → prueba → resultado → limitación. Sin esa granularidad, el índice puede recuperar el documento correcto pero no necesariamente la evidencia concreta que una IA necesita para responder o ejecutar.

## 4. Priorización de remediación

| Prioridad | Áreas/alcance | Trabajo requerido | Criterio de salida |
|---|---|---|---|
| P0 | Ocho áreas con bloques plantilla | Reescritura disciplinar de cada tema afectado; eliminar texto repetido | Ningún bloque de plantilla sustituye explicación técnica; ejemplos y límites propios |
| P0 | Agenda de 48 áreas | Convertir diseños comunes en protocolos específicos | Variables, corpus, baseline, controles, muestra y métricas definidos |
| P1 | 37 áreas con apéndices disciplinares | Auditar cada encabezado contra las 12 capas y el currículo | Matriz de cobertura tema×capa con evidencia y estado |
| P1 | Las 48 áreas | Trazabilidad de afirmaciones y fuentes | Citas por afirmación, edición, fecha, licencia, páginas y estado de lectura |
| P2 | Laboratorios prioritarios | Implementar en frío con datos sintéticos/entornos aislados | Scripts, hashes, ground truth, controles negativos, logs y resultados |
| P2 | Todas las áreas prioritarias | Evaluación y revisión | Rúbrica, métricas, incertidumbre, revisión independiente y registro de correcciones |

## 5. Orden de ejecución recomendado

1. Verificar la remediación editorial de `identity`, `malware`, `forensics`, `incident_response`, `threat_intel` y `reverse`; después, auditar granularmente las 48 áreas.
2. Desarrollar los protocolos concretos de AppSec, API, redes, Linux, Windows/AD, cloud, contenedores, criptografía, forense, IR, malware y seguridad de IA.
3. Construir la matriz tema×12 capas×K1–K5 para las 48 especialidades.
4. Leer y sintetizar fuentes primarias antes de elevar estados de revisión.
5. Ejecutar laboratorios fríos reproducibles y conservar resultados negativos.
6. Revisar independientemente y asignar madurez por tema, nunca por volumen de texto.

## 6. Regla de publicación

Hasta completar estas tareas, la clasificación correcta es **biblioteca estructurada con compendios editoriales ampliados y profundidad desigual, validación científica pendiente**. No declarar “biblioteca experta completa”. Las pruebas de software del repositorio validan el comportamiento del código cubierto por esos tests; no validan la verdad científica del contenido de conocimiento.


## 7. Remediación posterior a la auditoría

**Actualización:** 2026-11-19, después del diagnóstico inicial.

- Se reescribió el bloque de desarrollo de los siete subtemas de `mobile`: Android sandbox/Keystore, iOS sandbox/Keychain, almacenamiento/backups, TLS/OAuth, deep links/IPC/WebView, MASVS/MASTG y MDM/respuesta.
- Se sustituyó el texto genérico repetido por mecanismos, riesgos, controles y casos de prueba específicos de seguridad móvil.
- El módulo `crypto` también fue remediado: sus siete temas ahora contienen desarrollo disciplinar, se añadieron protocolos experimentales por tema, una agenda específica y una revisión documental ampliada. Las seis áreas restantes recibieron remediación editorial en la actualización del 19-11-2026; sus fuentes integrales, laboratorios y revisión independiente siguen pendientes.
- La sustitución editorial de móvil no representa laboratorio ejecutado ni validación independiente. Sus fuentes y pruebas siguen pendientes de revisión y ejecución.


### 8. Remediación posterior: Criptografía

**Actualización:** 2026-11-19.

- Se sustituyeron los siete bloques plantilla por desarrollo específico: entropía/DRBG; hash, MAC, KDF, password hashing y firmas; cifrado simétrico/AEAD; DH/ECDH/KEM; TLS/SSH/IPsec; ciclo de vida de claves; fallos de implementación y side channels.
- Se añadieron fórmulas y límites de interpretación, pruebas negativas, requisitos de nonce, análisis de transcript y advertencias de vigencia de SP 800-90C, SP 800-56A Rev. 3, FIPS 197 y FIPS 203.
- Se definieron siete laboratorios fríos (RBG, primitivas, AEAD, KEM, protocolos, rotación/PKI y fuzzing/side channels), con criterios de aceptación y evidencia mínima. **No se han ejecutado.**
- Se reemplazó la agenda genérica por protocolos con hipótesis, corpus, variables, controles, métricas y amenazas a validez.
- Se amplió la revisión bibliográfica y se registraron 12 nuevas referencias primarias/RFC; el registro pasa de 90 a **102 entradas**, sin IDs duplicados esperados (requiere auditoría automática posterior).
- El tracker ahora refleja el estado editorial M2 propuesto. No se eleva el conteo de fuentes íntegramente verificadas; los laboratorios, revisión independiente y validación M3–M5 siguen pendientes.


### 9. Remediación P0 de seis especialidades — 2026-11-19

Se sustituyeron los siete bloques repetidos por contenido disciplinar específico en:

- **identity:** IAM/IGA/PAM, MFA/WebAuthn, OAuth/OIDC/SAML/Kerberos, RBAC/ABAC/ReBAC, workload identity, SoD y recuperación de cuentas.
- **malware:** PE/ELF/Mach-O/documentos, análisis estático, sandbox, persistencia/memoria, YARA/Sigma, familias y contención.
- **forensics:** cadena de custodia, adquisición/write blockers, filesystems/timeline, memoria, red/correo/browser, cloud/móvil e informes.
- **incident_response:** preparación, triage, contención/preservación, erradicación/recuperación, escenarios sectoriales, comunicación y postmortem.
- **threat_intel:** PIR/ciclo, OSINT y fiabilidad, STIX/TAXII/MISP, ATT&CK/TTP, IOC/caducidad, atribución y productos.
- **reverse:** ABI/arquitectura, desensamblado/decompilación, CFG/data flow, parsers, emulación, firmware, fuzzing y divulgación.

Para los seis módulos se reemplazaron también las agendas genéricas por protocolos con unidad de análisis, variables, controles, métricas y amenazas a validez. Se actualizaron las revisiones exploratorias de literatura y sus IDs de fuentes existentes. Se diseñaron laboratorios fríos con datasets sintéticos, ground truth, criterios de aceptación y límites de seguridad.

**Estado de evidencia:** contenido y protocolos editoriales M2; las fuentes no se declaran leídas íntegramente, los laboratorios no se declaran ejecutados, y no hay revisión independiente ni reproducción externa. La reescritura no elimina la prioridad P1 de auditar las otras 42 áreas por tema×12 capas.
