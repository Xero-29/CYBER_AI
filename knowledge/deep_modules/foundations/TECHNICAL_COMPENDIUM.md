# Compendio técnico: Fundamentos de ciberseguridad

ID: `foundations` · Versión: 0.2.0 · Idioma: español · Madurez editorial: desarrollo técnico ampliado; **no equivale a validación experta ni experimental**.

## 0. Cómo usar este módulo

Este módulo establece los modelos comunes que los demás dominios de CYBER_AI deben reutilizar. No sustituye los módulos especializados de redes, sistemas operativos, criptografía, identidad, desarrollo seguro, respuesta a incidentes o gobierno.

### Resultados de aprendizaje

Al terminar, una persona o agente debe poder:

1. delimitar un sistema y sus dependencias sin inventar activos ni permisos;
2. distinguir activo, amenaza, evento, vulnerabilidad, exposición, impacto, riesgo y control;
3. construir inventario y clasificación trazables;
4. representar límites de confianza y flujos de datos;
5. formular escenarios de amenaza con precondiciones y consecuencias;
6. seleccionar controles proporcionales y definir evidencia de eficacia;
7. evaluar riesgo inherente y residual sin convertir escalas ordinales en probabilidades falsas;
8. proponer pruebas seguras, reproducibles y autorizadas;
9. explicar incertidumbre, limitaciones y decisiones.

### Convenciones de evidencia

- **Hecho observado:** respaldado por una fuente o artefacto inspeccionado.
- **Afirmación de fuente:** lo que una publicación declara; no implica que se haya probado en el entorno.
- **Inferencia:** conclusión derivada de hechos y supuestos explícitos.
- **Hipótesis:** proposición que todavía debe contrastarse.
- **Resultado experimental:** salida obtenida con protocolo, muestra, versiones y datos registrados.
- **Pendiente:** no existe evidencia suficiente.

No elevar una afirmación a resultado porque aparezca en una guía, estándar o respuesta de un modelo.

---

## 1. Modelos de seguridad y confianza

### 1.1 Sistema, contexto y objetivo

Un sistema es un conjunto de componentes que interactúan para cumplir una misión. El límite de análisis debe incluir, según el caso:

- personas, roles y procesos;
- aplicaciones, servicios, procesos y bibliotecas;
- equipos, firmware, redes y servicios de infraestructura;
- identidades humanas, de máquina y de workload;
- datos en reposo, tránsito, uso, copias y registros;
- proveedores, SaaS, APIs, DNS, PKI, CI/CD y dependencias;
- instalaciones, energía, conectividad y mecanismos de recuperación.

El inventario de componentes no es todavía un modelo de seguridad. Hay que describir quién usa qué, desde dónde, con qué autoridad, qué datos mueve y qué ocurre cuando falla.

**Objetivo de seguridad** = propiedad que se quiere preservar bajo un contexto y una amenaza definidos. Ejemplos: impedir lectura no autorizada de expedientes; evitar modificación de firmware sin autorización; mantener disponibilidad del servicio dentro de un objetivo acordado.

### 1.2 Propiedades de seguridad

- **Confidencialidad:** evitar divulgación a sujetos o procesos no autorizados.
- **Integridad:** evitar o detectar alteraciones no autorizadas o incorrectas.
- **Disponibilidad:** mantener acceso oportuno y fiable a servicios y datos.
- **Autenticidad:** verificar que una entidad, mensaje o dato corresponde a quien/lo que afirma ser.
- **Responsabilidad y trazabilidad:** atribuir acciones con registros suficientemente íntegros y contexto.
- **Privacidad:** gestionar tratamiento de datos personales conforme a propósito, minimización, transparencia, derechos y obligaciones aplicables.
- **Resiliencia:** sostener, degradar de forma controlada y recuperar funciones ante perturbaciones.

Estas propiedades pueden entrar en tensión. Por ejemplo, una autenticación más estricta puede elevar seguridad, pero si no existe recuperación segura puede reducir disponibilidad. La decisión debe documentar el trade-off.

### 1.3 Modelos de control y confianza

Un **sujeto** solicita una acción sobre un **objeto**. Un **monitor de referencia** aplica la decisión de acceso. Para ser confiable, el mecanismo debe mediar las solicitudes relevantes, resistir alteraciones y poder ser evaluado. En sistemas reales, la mediación puede estar distribuida entre aplicación, sistema operativo, gateway, proveedor de identidad y servicio de datos.

Modelos conceptuales que se deben distinguir:

- **Control de acceso discrecional (DAC):** el propietario o una autoridad delega permisos.
- **Control obligatorio (MAC):** políticas centrales y etiquetas restringen el acceso.
- **Control basado en roles (RBAC):** permisos se agrupan en roles; hay que controlar asignación, jerarquía y separación de funciones.
- **Control basado en atributos (ABAC):** decisión según atributos del sujeto, recurso, acción y contexto.
- **Zero Trust:** elimina la confianza implícita basada solo en ubicación o pertenencia a red; exige decisiones explícitas y evaluación continua según riesgo. No es un producto ni significa verificar una vez y confiar indefinidamente.
- **Defensa en profundidad:** capas complementarias reducen dependencia de un único control; no justifica controles duplicados sin análisis de cobertura y fallos comunes.

Un límite de confianza es una frontera donde cambian autoridad, nivel de confianza, propietario, política o exposición. Ejemplos: navegador→API; API→base de datos; cuenta corporativa→tenant de proveedor; red IT→OT; pipeline CI→registro de artefactos.

### 1.4 Modelo de sistema mínimo

Para cada componente registrar:

| Campo | Pregunta |
|---|---|
| Identificador | ¿Cómo se referencia sin ambigüedad? |
| Función | ¿Qué misión cumple? |
| Propietario | ¿Quién acepta el riesgo? |
| Operador | ¿Quién lo administra? |
| Entorno | ¿Producción, desarrollo, laboratorio, nube, OT? |
| Datos | ¿Qué procesa, almacena o transmite? |
| Identidades | ¿Qué humanos, servicios o dispositivos acceden? |
| Interfaces | ¿Qué API, puerto, protocolo, consola o canal humano expone? |
| Dependencias | ¿De qué proveedor, servicio, librería o equipo depende? |
| Criticidad | ¿Qué impacto produce su pérdida o alteración? |
| Evidencia | ¿Qué artefacto demuestra cada dato y cuándo se verificó? |

### 1.5 Errores de modelado

- Confundir una VLAN o subnet con un límite de confianza efectivo.
- Tratar un proveedor como una caja negra sin dependencias ni responsabilidades.
- Suponer que el inventario del CMDB refleja todos los activos reales.
- Confundir autenticación correcta con autorización adecuada.
- Considerar que cifrar datos elimina riesgos de acceso, endpoint, metadatos o disponibilidad.
- Modelar solo ataques externos y omitir error humano, abuso interno, fallos físicos, proveedor y errores de automatización.

---

## 2. Inventario y clasificación de activos

### 2.1 Qué es un activo

Activo es cualquier recurso que tiene valor para una misión y cuya pérdida, alteración, exposición o indisponibilidad puede causar consecuencias. Puede ser tangible o intangible: datos, credenciales, software, marca, procesos, conocimiento, equipo, servicio, clave criptográfica o capacidad operacional.

No confundir:
- **activo:** aquello que se protege;
- **componente:** elemento que implementa una función;
- **dato:** información con ciclo de vida y sensibilidad;
- **servicio:** capacidad entregada a un consumidor;
- **dependencia:** elemento necesario para que otro funcione.

Un mismo activo puede depender de varios componentes y un componente puede alojar múltiples activos.

### 2.2 Descubrimiento y reconciliación

Fuentes posibles: inventario de endpoints, nube, directorio de identidades, DNS, DHCP, EDR, MDM, CMDB, repositorios, SBOM, IaC, contratos, diagramas, entrevistas y observación autorizada.

El proceso debe:
1. fijar alcance, propietarios y fecha de corte;
2. recoger fuentes sin alterar producción;
3. normalizar identificadores (hostname, UUID, serial, cloud resource ID);
4. resolver duplicados sin borrar procedencia;
5. asociar propietario, entorno, criticidad y dependencias;
6. marcar confianza y antigüedad de cada registro;
7. reconciliar diferencias y activos no atribuibles;
8. asignar responsable de corrección y fecha de revisión.

No inferir que dos registros son el mismo activo solo por compartir nombre. Usar identificadores fuertes y mantener historial de cambios.

### 2.3 Clasificación de información

La organización debe definir sus propias etiquetas y reglas. Una escala ilustrativa (no normativa):

- **Pública:** divulgación autorizada.
- **Interna:** uso dentro de la organización.
- **Confidencial:** acceso limitado por función y necesidad.
- **Restringida/Crítica:** divulgación o alteración puede causar daño grave, obligación legal o impacto físico.

La etiqueta debe determinar manejo: acceso, cifrado, transmisión, retención, copia, exportación, borrado y respuesta a incidentes. No basta con etiquetar archivos si los metadatos, backups y exportaciones quedan fuera.

### 2.4 Criticidad e impacto

Evaluar consecuencias por dimensión y horizonte temporal:
- seguridad de personas y medio ambiente;
- operación y continuidad;
- finanzas y fraude;
- privacidad y derechos;
- obligaciones legales/contractuales;
- propiedad intelectual;
- confianza, reputación y terceros.

Separar impacto máximo plausible de impacto más probable. Documentar supuestos y escenarios. En sistemas industriales o médicos, seguridad física y continuidad pueden dominar la decisión.

### 2.5 Calidad del inventario

Métricas útiles:
- cobertura = activos confirmados / activos esperados en el alcance;
- completitud = campos obligatorios completos / campos obligatorios aplicables;
- atribución = activos con propietario validado / activos confirmados;
- frescura = registros verificados dentro del intervalo definido / registros activos;
- reconciliación = discrepancias resueltas / discrepancias detectadas.

Estas métricas no demuestran que el universo esperado sea correcto. Registrar cómo se estimó el denominador y qué fuentes no se pudieron consultar.

---

## 3. Superficie de ataque y modelado de amenazas

### 3.1 Superficie de ataque

Conjunto de puntos y rutas por los que un actor puede interactuar con el sistema, directa o indirectamente. Incluir:

- interfaces de red, puertos, protocolos y endpoints;
- APIs, formularios, cargas de archivos y flujos de autenticación;
- interfaces administrativas, consola, SSH/RDP y acceso remoto;
- dependencias, paquetes, imágenes, plugins y pipeline;
- identidades, tokens, claves, sesiones y procesos de recuperación;
- servicios de terceros, integraciones y cadena de suministro;
- canales físicos y humanos: USB, soporte, ingeniería social y acceso a instalaciones.

La superficie cambia con versiones, configuración, identidad, topología y dependencias. Un escaneo puntual es una observación parcial en un momento dado, no un inventario exhaustivo.

### 3.2 Escenario de amenaza

Describir cada escenario con:
1. activo y objetivo;
2. actor/capacidad o causa de fallo;
3. precondiciones y acceso inicial;
4. ruta y técnica;
5. debilidad explotada;
6. evento observable;
7. consecuencia e impacto;
8. controles existentes;
9. evidencia disponible;
10. incertidumbre y supuestos.

Evitar frases vagas como “un hacker puede entrar”. Un escenario debe ser específico y refutable.

### 3.3 STRIDE como técnica de generación

STRIDE ayuda a preguntar por clases de amenazas:
- **Spoofing:** suplantación de identidad.
- **Tampering:** modificación no autorizada.
- **Repudiation:** negación plausible de una acción por falta de evidencia.
- **Information Disclosure:** exposición de información.
- **Denial of Service:** pérdida o degradación de disponibilidad.
- **Elevation of Privilege:** obtención de autoridad superior.

STRIDE no calcula riesgo ni reemplaza análisis contextual. Una amenaza puede afectar varias propiedades y una categoría no implica que el escenario sea viable.

### 3.4 Árboles de ataque y rutas

Un árbol expresa un objetivo adversario y combinaciones AND/OR de subobjetivos. Permite examinar caminos alternativos, dependencias y puntos de interrupción. No asignar probabilidades numéricas a ramas sin datos y modelo explícitos.

Complementar con:
- diagramas de flujo de datos;
- límites de confianza;
- análisis de abuso;
- MITRE ATT&CK para tácticas/técnicas observadas o descritas;
- CAPEC para patrones de ataque;
- CWE para clases de debilidad.

No tratar ATT&CK como catálogo exhaustivo de amenazas ni como prueba de que una técnica ocurrió.

### 3.5 Priorización

La prioridad debe combinar exposición, impacto, plausibilidad, precondiciones, facilidad de detección, eficacia de controles, alcance y coste/tiempo de remediación.

No usar CVSS como sinónimo de riesgo empresarial. CVSS describe severidad técnica de una vulnerabilidad bajo su modelo; el riesgo contextual exige activo, exposición, explotación, controles e impacto local. EPSS estima probabilidad de explotación observada en un horizonte definido, no impacto de negocio ni certeza de ataque.

---

## 4. Identidad, privilegios y autenticación

### 4.1 Conceptos

- **Identificación:** declarar quién o qué solicita acceso.
- **Autenticación:** demostrar control de uno o más autenticadores.
- **Autorización:** decidir qué acciones puede realizar la identidad sobre un recurso.
- **Contabilidad/auditoría:** registrar qué ocurrió, cuándo, dónde y bajo qué contexto.
- **Federación:** aceptar una afirmación de identidad emitida por otra autoridad bajo una relación de confianza.
- **Sesión:** contexto temporal autenticado que mantiene estado y autoridad.
- **Privilegio:** capacidad de realizar acciones sensibles o administrativas.

La identidad puede ser humana, servicio, workload, dispositivo, proceso o agente automatizado. Las identidades no humanas requieren propietario, ciclo de vida, credencial protegida, alcance mínimo y revocación.

### 4.2 Autenticación y factores

Factores clásicos: algo que sabes, tienes o eres. Dos pasos no equivalen automáticamente a MFA si ambos dependen de la misma clase de factor. Evaluar resistencia a phishing, robo de sesión, recuperación, sincronización, dispositivo comprometido y soporte.

No almacenar contraseñas reversibles. Para sistemas que verifican contraseñas, usar funciones de derivación de contraseñas diseñadas para ese fin, sal única por registro y parámetros revisables. No confundir hash rápido general con KDF de contraseña.

### 4.3 Autorización y privilegio mínimo

Definir decisiones como tuplas: sujeto, acción, recurso, contexto y resultado. Revisar:
- mínimo privilegio y necesidad de saber;
- separación de funciones;
- privilegios temporales/JIT;
- cuentas administrativas separadas;
- acceso de emergencia (*break glass*) con alerta y revisión;
- expiración, revocación y recertificación;
- control de tokens, scopes, claims y audiencia.

RBAC simplifica administración cuando las funciones son estables; ABAC expresa contexto granular, pero aumenta complejidad de políticas y depuración. Pueden combinarse.

### 4.4 Ciclo de vida de identidad

Alta → prueba/validación → asignación de autenticadores → asignación de permisos → uso → revisión → cambio de rol → suspensión → revocación → eliminación/retención de evidencias.

Cada transición debe tener actor autorizado, evidencia, tiempo objetivo y tratamiento de sesiones/tokens ya emitidos.

### 4.5 Fallos comunes

Permisos heredados sin revisión; cuentas compartidas; secretos embebidos; tokens sin expiración adecuada; scopes excesivos; MFA vulnerable a phishing; procesos de recuperación débiles; cuentas huérfanas; identidades de servicio sin propietario; falta de revocación de sesiones tras un incidente.

---

## 5. Seguridad de redes y sistemas

Este tema define principios comunes; los detalles de TCP/IP, routing, firewalling, Linux, Windows, cloud, Kubernetes y protocolos se desarrollan en sus módulos especializados.

### 5.1 Modelo de comunicación

Representar origen, destino, protocolo, puerto/servicio, dirección, identidad, datos, cifrado, intermediarios y política. Diferenciar plano de datos, plano de control y plano de administración.

La segmentación debe basarse en función, criticidad, identidad y flujos necesarios. Una separación lógica no sirve si existen rutas alternativas, credenciales compartidas, administración transversal o reglas permisivas.

### 5.2 Controles fundamentales

- configuración segura y reducción de servicios expuestos;
- parcheo basado en riesgo y ventanas controladas;
- filtrado de entrada/salida y segmentación;
- administración por canales separados y autenticados;
- cifrado y validación de certificados cuando corresponda;
- protección de endpoints y ejecución;
- sincronización temporal confiable;
- registros con protección de integridad y retención;
- backups aislados y pruebas de restauración;
- gestión de configuración como código y revisión de cambios.

### 5.3 Baseline y deriva

Un baseline define estado esperado por rol y versión. Comparar estado real contra baseline, clasificar diferencias y determinar si son aprobadas, peligrosas o desconocidas. No revertir automáticamente cambios sin entender el contexto: puede romper disponibilidad o borrar evidencia.

---

## 6. Gestión de vulnerabilidades

### 6.1 Vocabulario

- **Debilidad:** condición que puede contribuir a un fallo.
- **Vulnerabilidad:** debilidad explotable en un contexto determinado.
- **Exposición:** posibilidad de interacción con el componente vulnerable.
- **Exploit:** técnica o artefacto que aprovecha una vulnerabilidad.
- **Mitigación:** medida que reduce probabilidad o impacto.
- **Remediación:** corrección de la causa o eliminación del componente afectado.
- **Excepción:** aceptación temporal y autorizada de riesgo, con controles y vencimiento.

### 6.2 Flujo de gestión

1. descubrir y atribuir activo;
2. identificar producto, versión, configuración y dependencia;
3. correlacionar advisories, CVE/CWE y fuentes del fabricante;
4. validar aplicabilidad sin pruebas destructivas;
5. estimar exposición, impacto y explotabilidad;
6. priorizar por riesgo contextual;
7. asignar responsable y SLA basado en criticidad;
8. remediar o aplicar mitigación temporal;
9. verificar versión/configuración corregida;
10. cerrar con evidencia o documentar excepción y vencimiento.

Un hallazgo de scanner es una hipótesis de vulnerabilidad hasta validar activo, versión, condición y evidencia. Gestionar falsos positivos, duplicados y vulnerabilidades sin CVE.

### 6.3 Datos que no deben perderse

Identificador del hallazgo; activo y propietario; fuente; CVE/CWE si aplica; producto/versión; evidencia; fecha; método; exposición; impacto; estado de explotación conocido; controles; decisión; responsable; fecha límite; excepción; retest; hash de evidencia.

### 6.4 Priorización sin falsa precisión

Puede usarse una matriz ordinal para ordenar trabajo, pero no presentar multiplicaciones de escalas cualitativas como probabilidades científicas. Si se usan scores, documentar definición, calibración, limitaciones y sensibilidad. Separar severidad técnica, probabilidad de explotación, exposición e impacto local.

---

## 7. Telemetría, respuesta y recuperación

### 7.1 Telemetría útil

Una señal debe responder: qué entidad actuó, qué hizo, sobre qué recurso, cuándo, desde dónde, con qué resultado y bajo qué identidad. Fuentes típicas: endpoint, identidad, red, aplicación, nube, DNS, correo, control de cambios, base de datos y entorno físico.

Los logs deben tener esquema, reloj, origen, nivel de confianza, retención, control de acceso, protección contra alteración y política de minimización. Centralizar no garantiza integridad: proteger canal, almacenamiento, permisos, borrado y administración.

### 7.2 Detección y triage

Una alerta es una señal que requiere evaluación, no prueba automática de incidente. Registrar:
- regla y versión;
- datos que la dispararon;
- entidad y ventana temporal;
- hipótesis;
- contexto y señales corroborantes;
- falso positivo/negativo conocido;
- decisión y analista;
- acciones ejecutadas y autorizaciones.

### 7.3 Respuesta

Preparación → detección/análisis → contención → erradicación → recuperación → lecciones aprendidas. Adaptar el ciclo a la guía vigente aplicable; no convertirlo en secuencia rígida si hay peligro inmediato o restricciones operacionales.

Antes de una acción: confirmar alcance, autoridad, impacto colateral, preservación de evidencia, reversibilidad y criterio de parada. En OT, salud y sistemas físicos, coordinar con responsables de seguridad funcional y operación.

### 7.4 Recuperación y resiliencia

Definir RTO (tiempo objetivo de recuperación) y RPO (punto objetivo de recuperación) por servicio, no copiar valores genéricos. Probar restauración, credenciales, dependencias, DNS, llaves, configuración y capacidad de operar degradado. Un backup que nunca se ha restaurado no demuestra recuperación.

### 7.5 Calidad de respuesta

Medir tiempo de detección y contención, precisión de alertas, cobertura de telemetría, integridad de evidencia, éxito de restauración y recurrencia. Publicar definiciones, denominadores, exclusiones y distribución; no usar promedios solos cuando hay colas largas.

---

## 8. Modelo de riesgo: de escenario a decisión

### 8.1 Cadena causal

Activo → amenaza/causa → evento → debilidad o condición → consecuencia → impacto → riesgo → decisión/control → riesgo residual.

La cadena evita saltar de “existe una CVE” a “la organización tiene riesgo crítico” sin demostrar activo afectado, exposición y consecuencia.

### 8.2 Riesgo inherente y residual

- **Inherente:** estimación antes de considerar controles específicos.
- **Residual:** estimación después de considerar controles existentes y su eficacia demostrada.
- **Aceptación:** decisión explícita del dueño del riesgo dentro de su autoridad.
- **Tratamiento:** mitigar, evitar, transferir/compartir o aceptar, según contexto.

Los controles declarados no reducen riesgo si no están implementados, operan mal o carecen de evidencia. La eficacia debe basarse en pruebas, configuración, muestreo y monitoreo.

### 8.3 Modelo cuantitativo y límites

En escenarios donde existan datos suficientes puede modelarse pérdida esperada:

\[
E[L] = \sum_{i=1}^{n} P(S_i) \cdot Impacto(S_i)
\]

Donde los escenarios (S_i) deben ser mutuamente excluyentes o ajustarse para evitar doble conteo. Si las probabilidades no se pueden estimar con fundamento, no inventarlas: usar rangos, escenarios y análisis de sensibilidad.

Una matriz 5×5 es una herramienta de comunicación y priorización, no una medición científica automática. No multiplicar “probabilidad 4 × impacto 5” y llamar al resultado pérdida esperada.

### 8.4 Ejemplo didáctico

Sistema ficticio: portal de clientes con frontend, API, base de datos y proveedor de identidad.

- Activo: registros personales.
- Flujo: navegador → frontend → API → base de datos.
- Frontera: API y proveedor de identidad.
- Escenario: token de servicio con permisos excesivos se filtra en pipeline.
- Precondición: secreto accesible a un actor con acceso al repositorio/log.
- Consecuencia: consulta no autorizada de registros.
- Impacto: privacidad, obligación de notificación, fraude y daño reputacional.
- Controles: secret scanning, identidad de workload, permisos mínimos, rotación, segmentación de datos, alertas de uso anómalo.
- Evidencia requerida: política del token, configuración real, logs de acceso, resultado de prueba negativa y prueba de revocación.
- Residual: no puede declararse bajo hasta comprobar revocación de sesiones, ausencia de copias del secreto y cobertura de logs.

Este caso es sintético; no representa un incidente observado.

---

## 9. Procedimiento reproducible para analizar un sistema

### Entrada

Alcance escrito, propietario, autorización, arquitectura disponible, inventario, clasificación de datos, restricciones, ventana, contactos y criterio de parada.

### Pasos

1. Validar autorización, alcance, exclusiones y ambiente.
2. Registrar fecha, commit/configuración y fuentes disponibles.
3. Construir mapa de componentes, datos, identidades y dependencias.
4. Identificar activos y propietarios; marcar incertidumbres.
5. Dibujar flujos y límites de confianza.
6. Formular escenarios con precondiciones y consecuencias.
7. Identificar controles existentes y evidencia de funcionamiento.
8. Evaluar riesgo inherente/residual y alternativas.
9. Diseñar pruebas no destructivas o simuladas; definir rollback.
10. Ejecutar solo con permiso y en entorno acordado.
11. Registrar resultados, limitaciones y falsos positivos.
12. Revisar mitigaciones y retest.
13. Entregar hallazgos con severidad contextual, evidencia y responsable.

### Condiciones de parada

Detener si se detectan activos fuera de alcance, degradación inesperada, datos personales no previstos, sistemas críticos no autorizados, riesgo físico, pérdida de trazabilidad o ausencia de responsable de decisión.

### Plantilla de hallazgo

| Campo | Contenido |
|---|---|
| ID | Identificador único |
| Resumen | Afirmación breve y verificable |
| Activo | Identificador y propietario |
| Evidencia | Artefacto, fecha, hash y origen |
| Condición | Precondición reproducible |
| Impacto | Consecuencia contextual |
| Alcance | Componentes/usuarios afectados |
| Confianza | Confirmado, probable, posible o no reproducido |
| Recomendación | Acción específica y alternativa |
| Riesgo residual | Lo que permanece tras el cambio |
| Retest | Procedimiento y resultado |
| Aprobación | Responsable y fecha |

---

## 10. Laboratorio frío de Fundamentos

**Entorno:** aplicación ficticia local con frontend, API, base de datos y proveedor de identidad simulado. Datos completamente sintéticos. Sin conexión a objetivos externos.

### Escenarios

1. **Baseline:** registrar componentes, versiones, identidades y flujos.
2. **Activo olvidado:** añadir un servicio ficticio que no aparece en el inventario y medir si se detecta.
3. **Permiso excesivo:** asignar a una identidad de prueba un permiso que no necesita; demostrar acceso permitido y luego denegado tras remediación.
4. **Secreto expuesto:** colocar un token sintético canario en un repositorio de laboratorio y validar detección, revocación y ausencia de uso.
5. **Telemetría incompleta:** retirar un campo de auditoría y medir qué preguntas ya no pueden responderse.
6. **Recuperación:** restaurar una copia sintética y medir RTO/RPO del ejercicio.

### Matriz de pruebas

| ID | Prueba | Resultado esperado | Evidencia |
|---|---|---|---|
| FND-COLD-01 | Inventario inicial | Activos y propietarios trazables | JSON/CSV, fuentes, fecha |
| FND-COLD-02 | Activo nuevo | Discrepancia detectada | Diferencia antes/después |
| FND-COLD-03 | Privilegio excesivo | Acceso no necesario identificado | Política y test negativo |
| FND-COLD-04 | Secreto canario | Detección y revocación | Log, hash, estado de token |
| FND-COLD-05 | Log incompleto | Pérdida de capacidad de atribución demostrada | Eventos y análisis |
| FND-COLD-06 | Restauración | Servicio recuperado dentro del objetivo definido | Tiempos y verificación funcional |

No se declaran ejecutadas estas pruebas por estar documentadas.

---

## 11. Evaluación del conocimiento

### Preguntas de dominio

1. ¿Por qué una subnet no es necesariamente un límite de confianza?
2. ¿Cuál es la diferencia entre autenticación y autorización?
3. ¿Por qué un registro de inventario necesita procedencia y fecha?
4. ¿Qué información falta en la afirmación “el servidor tiene riesgo crítico”?
5. ¿Por qué CVSS no equivale a riesgo empresarial?
6. ¿Qué prueba demuestra que un backup es recuperable?
7. ¿Qué diferencia hay entre control declarado, implementado y eficaz?
8. ¿Qué datos necesita una alerta para permitir triage reproducible?
9. ¿Cuándo una escala ordinal no debe tratarse como probabilidad?
10. ¿Qué condición obliga a detener una prueba?

### Rúbrica

Puntuar 0–3 por dimensión: 0 ausente/incorrecto; 1 superficial; 2 correcto con lagunas; 3 completo, contextualizado y sustentado.

- precisión conceptual;
- trazabilidad de activos y datos;
- calidad del modelo de amenazas;
- razonamiento de riesgo;
- selección y evidencia de controles;
- reproducibilidad;
- seguridad y proporcionalidad;
- comunicación de incertidumbre.

**Regla de aprobación:** ninguna dimensión crítica puede quedar en 0; el caso práctico debe ser reproducible por otra persona; no se aprueba si se inventan permisos, resultados o fuentes.

---

## 12. Referencias y estado de revisión

Las siguientes fuentes son referencias primarias para este módulo. El estado indicado describe el trabajo editorial de este repositorio, no la calidad intrínseca de la publicación.

| ID | Fuente | Uso en este módulo | Estado |
|---|---|---|---|
| `NIST-CSWP-29-CSF-2.0` | NIST CSF 2.0 | Taxonomía de resultados y perfiles | Página oficial y resumen inspeccionados; texto completo pendiente |
| `NIST-SP-800-30r1` | NIST SP 800-30 Rev. 1 | Proceso de evaluación de riesgos | Página oficial y abstract inspeccionados; texto completo pendiente |
| `NIST-SP-800-53r5` | NIST SP 800-53 Rev. 5 | Catálogo de controles de seguridad y privacidad | Página oficial y abstract inspeccionados; texto completo pendiente |
| `CIS-CONTROLS-v8.1` | CIS Critical Security Controls v8.1 | Salvaguardas priorizadas e implementación | Página oficial inspeccionada; texto íntegro pendiente |
| `NIST-SP-800-37r2` | NIST Risk Management Framework Rev. 2 | Integración del riesgo en ciclo de vida | Referencia catalogada; lectura pendiente |
| `MITRE-ATTACK` | MITRE ATT&CK | Lenguaje de tácticas/técnicas | Usar versión concreta y registrar fecha de snapshot |

### Notas de interpretación

- NIST CSF 2.0 describe resultados de alto nivel y remite a recursos para cómo lograrlos; no es una receta técnica prescriptiva.
- NIST SP 800-30 Rev. 1 orienta evaluación de riesgo; sus resultados requieren contexto, supuestos y juicio.
- NIST SP 800-53 es un catálogo adaptable de controles; seleccionar un control no prueba que esté implementado ni sea eficaz.
- CIS Controls v8.1 ofrece salvaguardas priorizadas; su aplicabilidad depende de activos, entorno y alcance.
- No reproducir contenido protegido de estándares ISO/IEC. Registrar metadatos y mapas permitidos; adquirir legalmente el texto para revisión autorizada.

## 13. Brechas pendientes y puerta de madurez

### Pendientes de investigación

- lectura íntegra y extracción de secciones relevantes de las fuentes primarias;
- análisis comparativo CSF 2.0 ↔ SP 800-30 ↔ SP 800-53 ↔ CIS v8.1;
- incorporar NICE Framework para competencias y vocabulario;
- incorporar fuentes académicas sobre modelado de amenazas, medición de riesgo y eficacia de controles;
- validar ejemplos con un especialista independiente;
- ejecutar los seis escenarios fríos y conservar resultados;
- añadir pruebas automatizadas de consistencia de los artefactos.

### Estado honesto

Este documento ya contiene desarrollo técnico específico y procedimientos diseñados. No demuestra todavía lectura íntegra de todas las referencias, validación experta, ejecución de laboratorio ni reproducción independiente. Mantener el módulo en estado **desarrollo técnico ampliado / validación pendiente** hasta completar esas puertas.
