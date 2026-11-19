# Compendio técnico: seguridad de aplicaciones y servicios

**ID:** `appsec` · **Versión:** 2.1.0 · **Idioma:** español  
**Madurez editorial:** desarrollo técnico ampliado; no equivale a revisión integral de estándares, validación experta, laboratorio ejecutado ni certificación K4/K5.  
**Ámbito:** aplicaciones web, servicios, APIs, frontend, backend, componentes, SDLC y cadena de suministro de software.

## 0. Propósito, límites y resultados de aprendizaje

Este módulo enseña a diseñar, construir, verificar y operar software con controles de seguridad verificables. No reduce AppSec a pruebas de penetración ni a una lista de vulnerabilidades. El objeto de análisis es el sistema completo: requisitos, arquitectura, código, datos, identidades, dependencias, pipeline, despliegue, telemetría y proceso de corrección.

Al completar la ruta, un profesional o agente debe poder:

1. delimitar aplicación, activos, roles, datos, dependencias y límites de confianza;
2. convertir amenazas y obligaciones en requisitos comprobables;
3. revisar autenticación, sesiones, autorización y aislamiento multi-tenant;
4. reconocer clases de fallos de entrada/salida, lógica, serialización y disponibilidad;
5. seleccionar controles según contexto y explicar sus límites;
6. diseñar pruebas unitarias, de integración, contrato, seguridad y regresión;
7. combinar análisis estático, dinámico, dependencias, secretos y revisión manual;
8. medir calidad de detección sin confundir alertas con vulnerabilidades confirmadas;
9. asegurar build, artefactos, dependencias y despliegue;
10. producir evidencia trazable, reproducible y proporcional a las conclusiones.

**Regla de alcance:** toda prueba dinámica se ejecuta en código propio, laboratorio aislado o activo con autorización expresa y alcance escrito. No se prueban objetivos de terceros, no se extraen datos reales, no se persiste acceso y no se evaden controles fuera de un ejercicio autorizado y delimitado.

## 1. Modelo de seguridad de una aplicación

### 1.1 Sistema y activos

Modelar como mínimo:
- sujetos: usuarios, operadores, administradores, servicios, jobs, dispositivos y cuentas de soporte;
- recursos: registros, archivos, funciones, colas, tenants, secretos, modelos y artefactos;
- acciones: leer, crear, modificar, borrar, exportar, aprobar, delegar y administrar;
- datos: clasificación, propietario, finalidad, retención, sensibilidad y ubicación;
- componentes: navegador, frontend, API gateway, backend, ORM, base de datos, caché, object storage, colas, IdP, proveedor externo y pipeline;
- límites de confianza: navegador/API, servicio/DB, tenant/tenant, workload/cloud control plane, CI/registry y organización/proveedor.

Un diagrama de flujo de datos debe mostrar origen, transformación, destino, protocolo, identidad usada y frontera de confianza. Un diagrama de despliegue no reemplaza al de flujo: uno muestra ubicación y otro cómo circula la información.

### 1.2 Amenazas y requisitos

STRIDE puede ayudar a clasificar spoofing, tampering, repudiation, information disclosure, denial of service y elevation of privilege; no es un sustituto del análisis de lógica de negocio. Para cada escenario registrar activo, actor, precondición, ruta, debilidad, impacto, control, evidencia y riesgo residual.

Los requisitos de seguridad deben ser verificables. Evitar frases como “la aplicación debe ser segura”. Preferir: “cada lectura o mutación de un objeto debe comprobar que el sujeto autenticado puede ejecutar la acción sobre ese objeto dentro del tenant actual; la prueba debe demostrar denegación para un objeto ajeno y éxito para uno propio”.

### 1.3 Modelo formal de autorización

Representar una decisión como:

`Allow(subject, action, resource, context) = Policy(subject, action, resource, context)`

La identidad no demuestra autoridad. La autorización debe evaluarse en el servidor y en cada operación sensible. RBAC ayuda a agrupar permisos, pero puede ser insuficiente para propiedad de objeto, tenant, atributos contextuales o relaciones dinámicas. ABAC y ReBAC modelan atributos y relaciones, pero elevan complejidad de política y pruebas.

Una matriz mínima sujeto–acción–recurso–contexto debe incluir:
- sujeto anónimo, usuario A, usuario B, administrador y servicio;
- recurso propio, ajeno, inexistente y de otro tenant;
- acciones de lectura, escritura, exportación, borrado y administración;
- estados activo, suspendido, expirado y revocado;
- respuestas esperadas y evidencia de auditoría.

**BOLA/IDOR:** no es simplemente un identificador predecible. El fallo es que una referencia controlada por cliente llega a un recurso sin comprobar la relación de autorización. UUID no es control de acceso. Ocultar botones en frontend no autoriza operaciones.

## 2. Identidad, autenticación, sesión y recuperación

Separar:
- identificación: declarar quién es el sujeto;
- autenticación: verificar la declaración;
- autorización: decidir qué puede hacer;
- gestión de sesión: mantener y terminar el contexto autenticado;
- recuperación: restablecer acceso sin abrir una ruta de toma de cuenta.

Controles a evaluar:
- MFA y resistencia a phishing según riesgo;
- protección contra enumeración en login y recuperación;
- limitación de intentos sin crear denegación fácil de servicio;
- almacenamiento de contraseñas mediante funciones de derivación apropiadas y parámetros vigentes;
- rotación de sesión tras autenticación o elevación;
- expiración por inactividad y duración absoluta;
- revocación efectiva al cerrar sesión, suspender cuenta o cambiar credenciales;
- cookies Secure, HttpOnly y SameSite según el flujo;
- protección CSRF cuando el navegador adjunta credenciales automáticamente;
- validación de issuer, audience, firma, algoritmo, expiración, nonce y estado en tokens según protocolo.

No asumir que JWT cifra su contenido: normalmente firma/integridad no equivale a confidencialidad. No aceptar algoritmo indicado por el token sin política fija. No usar CORS como mecanismo de autenticación o autorización.

### OAuth 2.0 / OpenID Connect

Distinguir autorización delegada (OAuth) de autenticación federada (OIDC). Validar redirect URI exacta, state, nonce, PKCE en clientes públicos y flujo apropiado. Los tokens deben tener audiencia y alcance mínimos, vida limitada, almacenamiento seguro y revocación/rotación según arquitectura. No colocar secretos de cliente en aplicaciones móviles o SPA públicas.

## 3. Manejo de entrada, salida y ejecución

### 3.1 Inyección

La inyección ocurre cuando datos no confiables se interpretan como parte de la gramática de un lenguaje o comando. La defensa principal es separar estructura y datos:
- SQL: consultas parametrizadas para valores; allowlist fija para nombres de tabla/columna y dirección de orden que no admiten bind parameters;
- shell: evitar construir comandos; invocar APIs específicas y pasar argumentos separados, con rutas y opciones controladas;
- LDAP/XPath/NoSQL: usar APIs y parámetros propios del lenguaje, no interpolación textual;
- plantillas: codificación contextual y autoescape; no marcar entrada arbitraria como HTML seguro.

La validación de tipo, longitud y formato complementa la parametrización; no la reemplaza. El escaping manual es frágil por diferencias de dialecto, charset y contexto.

Ejemplo seguro de SQL en Python con DB-API:

```python
# El valor del usuario se envía como parámetro, no se concatena al SQL.
cursor.execute(
    "SELECT id, display_name FROM accounts WHERE account_id = ?",
    (account_id,),
)
```

El marcador real depende del driver (qmark, format, pyformat, named, etc.). El ejemplo no debe copiarse sin consultar la API del controlador utilizado.

### 3.2 XSS y salida contextual

XSS aparece cuando datos controlables influyen en un contexto ejecutable del navegador. Diferenciar HTML body, atributo, JavaScript, CSS y URL: cada contexto tiene reglas de codificación distintas. Preferir sinks seguros y APIs DOM que traten contenido como texto; evitar `innerHTML` con datos no confiables. Sanitizar HTML solo cuando el producto necesita aceptar HTML, usando sanitizador mantenido y política explícita.

CSP es defensa en profundidad, no sustituto de codificación. Desplegar primero en modo report-only, revisar violaciones y evitar políticas permisivas como comodines amplios o `unsafe-inline` sin justificación.

### 3.3 CSRF y CORS

CSRF explota la inclusión automática de credenciales del navegador. Usar tokens anti-CSRF vinculados a sesión/acción, cookies SameSite cuando sea compatible, comprobación de Origin/Referer como defensa adicional y métodos/semánticas correctas. No realizar cambios de estado con GET. CORS controla qué orígenes pueden leer respuestas desde navegadores; no bloquea por sí mismo solicitudes ni sustituye autorización.

### 3.4 SSRF

SSRF ocurre cuando el servidor realiza solicitudes a destinos influenciados por entrada no confiable. Mitigar con destinos permitidos por negocio, validación DNS/IP después de resolución, bloqueo de rangos internos/link-local/loopback y metadatos cloud, control de red de salida, límites de redirección, esquemas permitidos, timeouts y tamaño máximo. Resolver DNS y luego conectar debe evitar TOCTOU/rebinding; validar solo el texto inicial de URL no basta. Separar fetcher de red de la lógica principal y registrar destino final de forma segura.

### 3.5 Deserialización, archivos y rutas

No deserializar formatos que ejecuten constructores o tipos arbitrarios sobre datos no confiables. Preferir formatos de datos simples con esquemas estrictos y límites de tamaño/profundidad. En uploads: validar tipo real además de extensión y MIME declarado, generar nombres internos, almacenar fuera del webroot, limitar tamaño/cantidad, analizar contenido según riesgo y evitar ejecución. Para rutas: canonicalizar y verificar que la ruta final permanece dentro del directorio autorizado; considerar symlinks, separadores alternativos y diferencias de plataforma.

### 3.6 Disponibilidad y lógica de negocio

Proteger operaciones costosas con cuotas, límites de concurrencia, timeouts, paginación acotada, límites de tamaño y presupuestos por identidad/tenant. Los límites solo por IP fallan ante NAT y botnets. Modelar abuso de flujos: cupones, transferencias, reembolsos, invitaciones, reservas y cambios de titularidad. Las pruebas deben comprobar invariantes de negocio, idempotencia y concurrencia, no solo payloads.

## 4. APIs y arquitectura distribuida

Inventariar rutas, métodos, versiones, esquemas, autenticación, autorización, scopes, propietarios, consumidores y dependencias. Retirar endpoints obsoletos con proceso de deprecación y telemetría. Para cada endpoint comprobar:
- autorización a nivel de objeto, propiedad y función;
- filtrado de campos de entrada y salida;
- límites por usuario, tenant y operación;
- validación de tipos y estados;
- consistencia entre API gateway y servicio;
- protección de webhooks (firma, timestamp, replay, idempotencia);
- errores sin stack traces, secretos ni datos internos;
- trazabilidad correlacionada sin registrar tokens o cuerpos sensibles.

GraphQL requiere límites de profundidad/complejidad, control de introspección según exposición, autorización por resolver/campo, límites de batching y protección de consultas costosas. gRPC requiere identidad de servicio, autorización por método/recurso, límites de mensajes y deadlines. La seguridad del gateway no sustituye controles dentro del servicio.

## 5. Criptografía aplicada, secretos y datos

Usar bibliotecas criptográficas mantenidas; no inventar algoritmos ni protocolos. Definir objetivo (confidencialidad, integridad, autenticidad), modelo de amenaza, ciclo de vida de claves, rotación, backup y recuperación. TLS protege el canal bajo configuración y validación correctas, pero no corrige autorización ni exposición en endpoints.

Secretos:
- no versionar claves, tokens ni certificados privados;
- usar secret manager o mecanismo equivalente;
- separar secretos por entorno y workload;
- limitar permisos y duración;
- rotar tras exposición y verificar revocación;
- evitar secretos en logs, trazas, argumentos de proceso y artefactos.

Minimizar datos, cifrar según clasificación, controlar exportación y retención, y probar eliminación/anonimización según requisitos legales. El cifrado en reposo no evita abuso por una aplicación ya autorizada.

## 6. SDLC seguro y cadena de suministro

Integrar seguridad en requisitos, diseño, implementación, revisión, build, release, despliegue y operación. El SSDF de NIST ofrece prácticas de alto nivel integrables en diferentes modelos SDLC; no prescribe un pipeline universal ni certifica que el proceso sea eficaz.

Controles de pipeline:
- revisión de cambios y protección de ramas;
- dependencias fijadas y actualización controlada;
- SCA con política de severidad, explotabilidad y contexto;
- escaneo de secretos antes de merge y en historia según riesgo;
- SAST en código propio y reglas revisadas;
- pruebas unitarias/de integración de controles;
- DAST en staging autorizado;
- SBOM en formato interoperable y asociado a artefacto;
- procedencia del build, firmas y verificación de artefactos;
- aislamiento de runners, permisos mínimos y tokens de corta duración;
- separación de build y release, aprobación para producción y rollback.

Un SBOM describe componentes conocidos, no prueba que el software sea seguro ni que el inventario sea completo. Un escaneo limpio tampoco prueba ausencia de vulnerabilidades.

## 7. Verificación técnica y herramientas

| Técnica | Observa | Límites principales |
|---|---|---|
| SAST | patrones y flujos en código/bytecode | depende de reglas, lenguaje, contexto y modelado de taint |
| DAST | comportamiento observable de aplicación en ejecución | cobertura limitada por rutas, roles, estados y configuración |
| IAST | señales desde instrumentación durante pruebas | impacto de instrumentación y cobertura de ejecución |
| SCA | componentes, versiones, licencias y advisories | SBOM incompleto, backports, reachability y falsos positivos |
| Secret scanning | patrones de credenciales | formatos desconocidos, secretos cifrados y falsos positivos |
| Fuzzing | robustez ante entradas generadas | calidad del corpus, oráculos, cobertura y sanitizers |
| Revisión manual | lógica de negocio, arquitectura y contexto | coste, sesgo y variabilidad entre revisores |

No sumar alertas de herramientas como si fueran vulnerabilidades independientes. Normalizar por activo, versión, causa raíz y evidencia. Confirmar explotabilidad solo en entorno autorizado y con impacto mínimo. Documentar falsos positivos, falsos negativos conocidos y zonas no cubiertas.

## 8. Análisis matemático y métricas

Para un clasificador de hallazgos sobre un conjunto etiquetado:
- TP: vulnerabilidad real correctamente detectada;
- FP: alerta sobre caso no vulnerable;
- FN: vulnerabilidad existente no detectada;
- TN: caso correctamente clasificado como negativo.

`Precision = TP / (TP + FP)` mide proporción de alertas que son verdaderas en la muestra etiquetada.  
`Recall = TP / (TP + FN)` mide proporción de defectos conocidos detectados.  
`F1 = 2 × Precision × Recall / (Precision + Recall)` combina ambas, pero oculta costes asimétricos y no debe ser la única métrica.

Añadir cobertura de rutas/roles/estados, tiempo por hallazgo confirmado, coste de revisión, tasa de regresión, defectos escapados, severidad, impacto, reproducibilidad y latencia. Reportar intervalos de confianza cuando el tamaño muestral lo permita. Un benchmark con vulnerabilidades sembradas puede sesgar hacia patrones conocidos y no representa necesariamente defectos reales.

La priorización debe considerar severidad técnica, exposición, explotabilidad, privilegios, impacto empresarial, controles compensatorios y confianza de evidencia. CVSS describe severidad técnica bajo supuestos definidos; no es probabilidad de explotación ni riesgo empresarial completo.

## 9. Laboratorios fríos reproducibles

Los siguientes laboratorios están **diseñados, no ejecutados**. Requieren entorno local aislado, aplicación deliberadamente vulnerable, datos sintéticos, snapshots, red de salida bloqueada salvo necesidad justificada y registro de versiones.

### LAB-APPSEC-01 — Matriz de autorización multi-tenant
- Crear dos tenants y usuarios ficticios A/B.
- Sembrar recursos propios y cruzados con identificadores opacos.
- Definir matriz sujeto–acción–recurso–tenant.
- Ejecutar pruebas de lectura, edición, borrado y exportación.
- Resultado esperado: acceso permitido solo a combinaciones explícitas; intentos cruzados denegados y auditados.
- Evidencia: fixtures, casos, respuestas, logs saneados y reporte de cobertura.

### LAB-APPSEC-02 — Separación código/datos
- Crear aplicación local con endpoint de búsqueda y DB efímera.
- Comparar implementación parametrizada con versión deliberadamente insegura, sin exponerla a red externa.
- Probar entradas normales, vacías, largas, Unicode y delimitadores como datos.
- Resultado esperado: el comportamiento de la consulta se mantiene estructuralmente estable; el input no altera gramática.
- Evidencia: tests, query plan/log controlado, diff y resultado antes/después.

### LAB-APPSEC-03 — XSS y codificación contextual
- Crear página de laboratorio con contextos HTML/texto/atributo.
- Introducir valores sintéticos inocuos y comprobar que se representan como texto, no como código.
- Verificar CSP report-only y política final.
- Resultado esperado: ningún input de usuario ejecuta script; política CSP no rompe funciones legítimas.
- Evidencia: pruebas DOM, cabeceras y reportes de violación.

### LAB-APPSEC-04 — Comparación de herramientas
- Preparar repositorio sintético con defectos conocidos etiquetados y versiones congeladas.
- Ejecutar SAST, SCA y revisión manual con reglas predefinidas.
- Deduplicar por causa raíz y etiquetar resultados por revisor independiente.
- Resultado esperado: métricas precision/recall/F1, cobertura, tiempo y discrepancias; no proclamar ganador universal.
- Evidencia: dataset, hashes, configuración, resultados brutos, scripts y análisis.

### LAB-APPSEC-05 — Pipeline y supply chain
- Construir aplicación de prueba desde commit fijo.
- Generar SBOM, registrar dependencias, procedencia y firma del artefacto.
- Verificar que artefacto desplegado coincide con el artefacto aprobado.
- Resultado esperado: cambios no aprobados o artefactos no verificables bloqueados.
- Evidencia: hashes, attestation, SBOM y logs.

Criterios de parada: pérdida de aislamiento, acceso a datos no sintéticos, tráfico fuera del scope, consumo inesperado, persistencia, exposición de secreto o impacto sobre servicios compartidos. Detener, preservar evidencia mínima, limpiar entorno y documentar desviación.

## 10. Evaluación y rúbrica

La evaluación no se aprueba por recordar nombres de vulnerabilidades. Debe demostrar razonamiento y ejecución:

| Competencia | Peso | Evidencia |
|---|---:|---|
| Modelo de amenazas y requisitos | 15% | diagrama, activos, escenarios y requisitos verificables |
| Identidad y autorización | 20% | matriz y pruebas negativas por rol/objeto/tenant |
| Manejo de datos e inyección | 15% | revisión de código y regresiones |
| APIs y lógica de negocio | 15% | inventario, límites, invariantes y pruebas |
| SDLC y supply chain | 15% | pipeline, SBOM y verificación de artefactos |
| Herramientas y análisis | 10% | deduplicación, métricas y falsos positivos |
| Evidencia y reproducibilidad | 10% | versiones, datos, hashes, protocolo y límites |

Umbral sugerido para evaluación interna: 80/100 y ningún fallo crítico de autorización, gestión de secretos o aislamiento. El umbral debe validarse y calibrarse; no es certificación profesional.

## 11. Preguntas de investigación abiertas

1. ¿Cuánto aumenta la detección de BOLA al usar una matriz sujeto–objeto–acción–tenant frente a pruebas endpoint-centric?
2. ¿Qué combinaciones de SAST/DAST/SCA reducen defectos escapados sin elevar excesivamente el coste de triage?
3. ¿Cómo cambia la precisión de análisis de flujo cuando se modelan fuentes/sinks y sanitizadores específicos del framework?
4. ¿Qué controles de SSRF resisten mejor DNS rebinding, redirecciones y cambios de resolución?
5. ¿Qué señales predicen mejor riesgo real de dependencias: CVSS, EPSS, KEV, reachability, contexto de despliegue o combinación?
6. ¿Qué evidencia mínima demuestra que una SBOM y la procedencia del build corresponden al artefacto desplegado?

Estas preguntas no tienen resultados asignados. Cada estudio debe definir hipótesis, muestra, comparador, métricas, amenazas a validez y protocolo antes de ejecutar.

## 12. Fuentes y estado de revisión

| ID | Fuente | Estado editorial |
|---|---|---|
| `OWASP-ASVS-5.0.0` | OWASP ASVS 5.0.0 | Página oficial y versión estable inspeccionadas; estándar completo pendiente |
| `OWASP-API-TOP10-2023` | OWASP API Security Top 10 2023 | Página y categorías oficiales inspeccionadas |
| `OWASP-API1-BOLA-2023` | API1 Broken Object Level Authorization | Página de riesgo oficial inspeccionada |
| `OWASP-WSTG-4.2` | OWASP WSTG 4.2 | Página de versiones y referencias versionadas inspeccionadas; escenarios completos pendientes |
| `NIST-SP-800-218-SSDF-1.1` | NIST SSDF 1.1 | Página oficial y abstract inspeccionados; texto íntegro pendiente |
| `MITRE-CWE-TOP25-2025` | CWE Top 25 2025 | Lista, ranking y notas oficiales inspeccionados; metodología detallada pendiente |
| `OWASP-SQLI-PREVENTION` | OWASP SQL Injection Prevention Cheat Sheet | Recomendaciones oficiales inspeccionadas; ejemplos por motor/driver pendientes |

## 13. Brechas y estado de madurez

- Lectura integral de ASVS, WSTG, SSDF y documentación complementaria pendiente.
- Revisión sistemática de literatura académica pendiente.
- Los cinco laboratorios están diseñados, no ejecutados.
- No hay resultados experimentales ni benchmarks propios.
- No hay revisión independiente documentada.
- No hay Skills AppSec promovidas por validación práctica en este cambio.

**Límite empírico: no M3/M4/M5.** El módulo permanece en desarrollo técnico ampliado. La inspección de páginas oficiales no equivale a lectura integral; un protocolo diseñado no equivale a experimento ejecutado; y una matriz de pruebas no equivale a eficacia demostrada. No declarar K4/K5 hasta superar las puertas aplicables del estándar experto e investigación.
