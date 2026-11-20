# FND-01.03 — Activo, sujeto, objeto, recurso, dato, proceso, servicio, misión y stakeholder

**Estado:** desarrollo teórico en borrador; L1–L12 en progreso; T0/O0.  
**Fecha:** 2026-11-20.  
**Propósito:** establecer una ontología operacional para identificar qué se protege, quién actúa, qué se usa, qué misión se soporta y quién asume responsabilidades.

## 1. L1 — Fundamentos y vocabulario

### 1.1 Activo
Un activo es algo que tiene valor para una organización, una persona o una misión y cuya pérdida, alteración, divulgación, indisponibilidad o compromiso puede producir consecuencias. El valor no es solo financiero: incluye misión, seguridad física, privacidad, cumplimiento, continuidad, reputación, propiedad intelectual y confianza.

Los activos pueden ser tangibles o intangibles:
- físicos: instalaciones, máquinas, sensores, PLC, servidores, redes, medios;
- digitales: software, firmware, configuraciones, modelos, cuentas, certificados, claves;
- informacionales: bases de datos, registros, diseños, telemetría, backups, modelos derivados;
- organizacionales: procesos, servicios, conocimiento, roles, relaciones con proveedores;
- externos/dependencias: SaaS, nube, DNS, identidad federada, conectividad, soporte de fabricante.

No todo activo es propiedad legal de la organización. Un servicio externo puede ser un activo de dependencia y riesgo aunque el cliente no controle su infraestructura.

### 1.2 Recurso
Un recurso es una capacidad, medio o elemento que puede utilizarse para alcanzar un objetivo: cómputo, almacenamiento, ancho de banda, tiempo, personal, presupuesto, datos, credenciales o capacidad de proveedor. Un recurso puede ser limitado, compartido, sustituible o externo. Puede ser un activo si posee valor y requiere protección, pero ambos términos no son idénticos.

### 1.3 Sujeto y objeto
En modelos de control de acceso, el sujeto es la entidad activa que solicita o ejecuta una operación; puede ser una persona, proceso, servicio, dispositivo o identidad de workload. El objeto es el recurso sobre el que recae la operación: archivo, registro, API, dispositivo, proceso, cola, secreto o servicio.

Sujeto/objeto describen una relación de interacción, no una clasificación universal de activos. Un mismo componente puede actuar como sujeto en una operación y como objeto en otra. La identidad del sujeto debe distinguirse de la persona u organización responsable de él.

### 1.4 Dato e información
Dato es una representación codificada o registro. Información es el significado que se interpreta en un contexto. Los datos pueden ser personales, operativos, técnicos, comerciales, de seguridad o de misión. Su clasificación debe considerar contenido, metadatos, inferencias, combinaciones, procedencia, finalidad, retención, ubicación y destinatarios.

Un dato puede ser simultáneamente activo, objeto, recurso y entrada de un proceso. Un hash o firma puede preservar integridad/procedencia de una representación sin demostrar verdad semántica.

### 1.5 Proceso y servicio
Un proceso es un conjunto de actividades relacionadas que transforma entradas en resultados mediante personas, reglas, sistemas y recursos. Un servicio es una capacidad entregada a un consumidor o usuario con condiciones de acceso, calidad, disponibilidad y responsabilidades. Un servicio puede depender de varios procesos, activos internos y proveedores externos.

### 1.6 Misión
La misión expresa el propósito y los resultados esenciales que una organización o sistema debe cumplir. No es sinónimo de aplicación, proceso, servicio o activo. Una misión se descompone en objetivos, funciones, capacidades, servicios y dependencias. La criticidad de un activo deriva, en parte, de cómo su fallo afecta a la misión.

### 1.7 Stakeholder o parte interesada
Stakeholder es una persona, grupo u organización que puede afectar, verse afectada o percibirse afectada por una decisión, sistema, servicio o riesgo. Roles posibles:
- propietario del activo;
- custodio técnico;
- operador;
- usuario/consumidor;
- propietario de misión o proceso;
- responsable de seguridad, privacidad o safety;
- proveedor, fabricante y mantenedor;
- regulador o autoridad;
- titular de datos/persona afectada;
- auditor, evaluador y autoridad de aceptación de riesgo;
- adversario o actor de amenaza, que debe modelarse como actor pero no como parte interesada legítima.

Los roles pueden coexistir, pero deben asignarse explícitamente. “Owner” no significa necesariamente administrador técnico ni responsable legal del tratamiento.

## 2. L2 — Ontología formal y métricas

### 2.1 Grafo de activos y misión

Representar el contexto como un grafo tipado:

G = (V, E, τ, α)

- V: entidades (activos, actores, sujetos, objetos, datos, procesos, servicios, misiones, stakeholders, controles, proveedores).
- E: relaciones tipadas entre entidades.
- τ(v): tipo de entidad.
- α(v): atributos y metadatos.

Relaciones mínimas:
- owns, governs, operates, maintains, uses;
- accesses, processes, stores, transmits, produces, consumes;
- depends_on, supports, provides, controls, monitors;
- located_at, supplied_by, connected_to, part_of;
- impacts, authorized_for, accountable_to.

La ontología debe permitir relaciones muchos-a-muchos y cambios de rol. Evitar árboles rígidos que no representen servicios compartidos, activos multi-tenant, dependencias externas o sistemas de sistemas.

### 2.2 Frontera del sistema

Definir sistema de interés S como un conjunto de componentes, interfaces, personas, procesos, datos y dependencias que participan en una función/misión delimitada. La frontera de autorización de seguridad puede ser distinta de la frontera física, contractual, organizacional o de datos.

Registrar:
- inclusiones y exclusiones;
- interfaces y conexiones externas;
- componentes compartidos y controles heredados;
- dependencias de terceros;
- límites geográficos/jurisdiccionales;
- flujos de datos;
- autoridad de operación y aceptación.

Una conexión externa no queda “fuera del riesgo” por estar fuera de la frontera administrativa.

### 2.3 Criticidad multidimensional

La criticidad no debe reducirse a una puntuación única sin calibración. Modelar para cada activo a:

C(a) = (M, S, P, L, O, F, R)

donde:
- M: impacto en misión;
- S: impacto en safety;
- P: impacto en privacidad;
- L: impacto legal/regulatorio;
- O: impacto operacional;
- F: impacto financiero/estratégico;
- R: dificultad/tiempo de recuperación.

Cada dimensión debe tener escala, definición, evidencia, horizonte y autoridad de aprobación. La agregación requiere una regla explícita y análisis de sensibilidad. Un activo de baja valoración financiera puede ser crítico para la seguridad física o la continuidad de un servicio esencial.

### 2.4 Calidad de inventario

Métricas recomendadas:
- cobertura estimada = activos identificados / activos estimados en alcance;
- cobertura de propietario = activos con responsable vigente / total en alcance;
- frescura = registros actualizados dentro del SLA / total;
- cobertura de dependencias = dependencias críticas mapeadas / dependencias críticas conocidas;
- trazabilidad = registros con fuente, fecha, confianza y evidencia / total;
- tasa de huérfanos = activos sin owner o función / total;
- tasa de duplicados = identidades ambiguas o duplicadas / total;
- cobertura de ciclo de vida = activos con estado, soporte y fecha de revisión / total.

El denominador de cobertura puede ser incierto. Informar intervalo, método de estimación y fuentes; no presentar un 100 % cuando la población real no puede conocerse.

## 3. L3 — Arquitectura y modelo de información

### 3.1 Capas de arquitectura
1. Misión y objetivos de negocio/servicio.
2. Procesos y funciones que realizan la misión.
3. Servicios consumidos por usuarios y sistemas.
4. Aplicaciones, APIs, workloads, modelos y software.
5. Datos, registros, secretos y artefactos.
6. Infraestructura: cómputo, almacenamiento, red, nube y virtualización.
7. Tecnología operacional: sensores, actuadores, PLC, HMI, RTU, historiadores y redes industriales.
8. Identidades, privilegios, certificados y mecanismos de confianza.
9. Personas, proveedores, contratos, soporte y procesos de cambio.
10. Instalaciones, energía, comunicaciones y ambiente físico.

### 3.2 Mapa de dependencias
Un activo debe relacionarse con:
- servicio/proceso que soporta;
- misión que depende de ese servicio;
- datos que procesa;
- sujetos/actores que lo administran y consumen;
- proveedores y servicios externos;
- componentes de identidad, DNS, tiempo, energía, red y logging;
- controles y evidencias que lo protegen.

Una CMDB o inventario de red aislado no representa por sí solo el grafo de misión. Deben reconciliarse inventario técnico, catálogo de servicios, mapa de datos, gestión de proveedores, arquitectura, compras y conocimiento de operadores.

### 3.3 Activos efímeros y modernos
Incluir recursos efímeros y no tradicionales: contenedores, pods, funciones serverless, instancias cloud, identidades de workload, tokens, APIs, repositorios, pipelines CI/CD, modelos ML, datasets, endpoints móviles, SaaS, dispositivos IoT, firmware, cuentas de terceros y copias de datos.

IP/MAC/hostname no son identificadores estables suficientes. Usar IDs canónicos y relaciones de identidad; mantener alias, cambios y observaciones temporales.

## 4. L4 — Marcos y controles de referencia

| Fuente | Aplicación en este subtema | Límite |
|---|---|---|
| NIST CSF 2.0 | categorías ID.AM para inventario, clasificación, dependencias, ciclo de vida y priorización | resultados de alto nivel; no sustituye inventario técnico |
| NIST SP 800-53 Rev. 5 Release 5.2.0 | CM-8 inventario de componentes; PM-5 inventario de sistemas; CM-12 ubicación de información; CM-13 mapeo de acciones de datos | catálogo de controles; adaptar a contexto y riesgo |
| NIST SP 800-37 Rev. 2 | RMF, preparación, categorización, selección, implementación, evaluación, autorización y monitoreo | marco federal estadounidense; adaptar obligaciones locales |
| NIST SP 800-30 Rev. 1 | riesgo de activos, amenazas, vulnerabilidades, probabilidad e impacto | guía de evaluación, no una ontología de activos |
| NISTIR 8286A Rev. 1 | escenarios y registros de riesgo empresarial vinculados a activos y objetivos de misión | usar Rev. 1 (2025), no la edición 2021 retirada |
| NIST SP 800-128 | gestión de configuración centrada en seguridad y baselines | complementa, no sustituye inventario |
| CISA et al. (2025) OT Asset Inventory Guidance | cinco pasos: alcance, identificación/atributos, taxonomía, gestión de datos y ciclo de vida | guía OT; no exhaustiva ni sustituto de safety engineering |
| ISO/IEC/IEEE 15288:2023 | procesos de ciclo de vida, stakeholders, adquisición, operación, mantenimiento y retiro | estándar de procesos; no prescribe método único |
| ISO/IEC 27001:2022 + Amd 1:2024 | sistema de gestión de seguridad de información y enfoque basado en riesgo | el texto completo no se ha consultado; no afirmar conformidad |

## 5. L5 — Implementación técnica del inventario

### 5.1 Esquema mínimo de registro

Cada registro debe poder expresar:
- asset_id canónico y alias;
- nombre, tipo, rol y descripción;
- fabricante, modelo, serie, firmware/software y versión;
- ubicación física/lógica y zona/conduit;
- owner, custodian, operator y supplier;
- función, proceso, servicio y misión soportada;
- criticidad por dimensión y justificación;
- datos tratados, clasificación, finalidad, retención y ubicación;
- interfaces, protocolos, puertos, conexiones y dependencias;
- identidad asociada, cuentas, certificados y privilegios;
- logging, monitoring, backup y recuperación;
- soporte, EOL/EOS, garantía, mantenimiento y lifecycle_state;
- first_seen, last_seen, last_validated, source, confidence y reviewer;
- evidencia, hash, fecha y método de descubrimiento.

### 5.2 Pipeline de inventario
1. Definir alcance y autoridad.
2. Descubrir desde fuentes autorizadas: inspección, APIs cloud, EDR, CMDB, compras, DNS/DHCP, certificados, red, SBOM, IAM y entrevistas.
3. Normalizar tipos, identificadores, unidades, nombres y fechas.
4. Resolver duplicados y entidades equivalentes.
5. Reconciliar fuentes conflictivas con confianza y procedencia.
6. Asignar owner/custodian y función.
7. Clasificar criticidad, datos y dependencias.
8. Validar con operador/propietario y evidencia.
9. Publicar inventario versionado con controles de acceso.
10. Monitorear drift, obsolescencia y cambios.
11. Revisar periódicamente y retirar/sanitizar activos fuera de servicio.

### 5.3 Reglas de identificación
- No usar IP como identidad primaria.
- No unir registros solo por hostname sin comprobar contexto.
- Mantener IDs de proveedor como atributos, no como único identificador.
- Registrar confianza de coincidencia y fuentes contradictorias.
- Tratar activos desconocidos como hallazgos que requieren triage, no como falsos positivos automáticos.
- En OT, priorizar métodos pasivos y revisión con operadores; escaneo activo solo con autorización, ventana, límites y evaluación de safety.

## 6. L6 — Análisis avanzado y casos límite

### Caso A — Shadow IT
Un equipo adopta SaaS con datos de clientes sin registrarlo. El servicio, identidades, datos, contrato, subprocesadores, región, API y backups forman parte del contexto. Bloquearlo sin análisis puede interrumpir proceso legítimo; ignorarlo deja una dependencia desconocida. El tratamiento es descubrir, identificar owner, clasificar datos, evaluar finalidad/contrato, mapear dependencias y decidir con autoridad.

### Caso B — PLC sin soporte
Un PLC antiguo ejecuta función crítica y no admite parche. La clasificación debe incluir misión, safety, exposición, disponibilidad, proveedor, compensating controls y dependencia. “Sin CVE conocido” no equivale a bajo riesgo. La mitigación puede ser segmentación, control de acceso, monitorización pasiva, repuestos, procedimientos y plan de sustitución.

### Caso C — Modelo ML
El modelo, pesos, dataset, pipeline, feature store, registro, endpoint, identidad de servicio y proveedor de cómputo son activos distintos pero relacionados. Inventariar solo el servidor omite procedencia, datos de entrenamiento, versiones y dependencias de inferencia.

### Caso D — Dato replicado
Una tabla se replica a un lago, backup, entorno de prueba y proveedor analítico. Cada copia tiene ubicación, finalidad, retención, acceso, owner y riesgo de privacidad propios. El inventario debe representar lineage y no solo el sistema original.

### Caso E — Activo huérfano
Un dispositivo sigue transmitiendo, pero no tiene owner, función ni soporte confirmado. No asignar criticidad por intuición. Registrar incertidumbre, aislar de forma proporcional y segura, consultar operador, proveedor y registros de cambio, y documentar decisión.

## 7. L7 — Perspectiva de seguridad y amenazas

Amenazas contra el propio inventario:
- envenenamiento de registros para ocultar o introducir activos;
- spoofing de hostname, IP, MAC o identidad;
- manipulación de timestamps y last_seen;
- acceso no autorizado al inventario para planificar ataques;
- extracción de mapas de red, proveedores y puntos únicos de fallo;
- abuso de API de discovery;
- credenciales de escaneo excesivas;
- agentes de inventario comprometidos;
- datos de CMDB desactualizados usados como verdad;
- eliminación de activos críticos de la lista.

Controles: autenticación fuerte, autorización por rol/atributo, firmas o integridad de exportaciones, auditoría, separación de funciones, revisión de cambios, protección de credenciales de discovery, cifrado, minimización, retención y validación cruzada.

En OT, la identificación activa puede afectar disponibilidad o seguridad física. La política debe definir zonas permitidas, ventanas, límites de tasa, exclusiones, stop conditions y aprobación del responsable operacional.

## 8. L8 — Investigación científica y preguntas abiertas

Preguntas:
1. ¿Qué combinación de fuentes logra mayor cobertura y menor tasa de falsos positivos en entornos híbridos?
2. ¿Cómo estimar confianza de identidad de activos efímeros?
3. ¿Qué modelo de grafo predice mejor el impacto de perder una dependencia compartida?
4. ¿Cómo medir obsolescencia y riesgo de activos OT sin escaneo activo?
5. ¿Cómo conciliar inventarios de IT, OT, cloud, IAM, datos y proveedores sin duplicar entidades?
6. ¿Cómo medir la calidad de ownership y clasificación sin confundir registro con realidad?

Diseño experimental: comparar un baseline CMDB con un método multi-fuente; definir ground truth independiente; medir precision/recall de descubrimiento, resolución de entidades, freshness, ownership, dependencia y cobertura; estratificar por IT/OT/cloud; documentar sesgo y falsos negativos.

## 9. L9 — Laboratorio y dataset sintético

LAB-FND-13A usa un grafo sintético con PLC, HMI, sensor, historian, gateway remoto, proveedor SaaS, identity provider, red OT, backup y activos de datos. Detecta:
- activos de criticidad alta sin owner;
- registros obsoletos;
- datos sin clasificación;
- activos críticos sin logging;
- dependencias externas con soporte desconocido;
- identidades no canónicas.

El laboratorio prueba la lógica del inventario, no la exactitud de un descubrimiento real ni la seguridad de una red OT.

## 10. L10 — Evaluación y benchmark

Criterios:
- distinguir los diez conceptos del subtema con ejemplos;
- definir frontera y alcance sin omitir dependencias;
- construir un grafo tipado;
- diseñar esquema de inventario y claves canónicas;
- asignar criticidad multidimensional y justificarla;
- identificar riesgos de privacidad y seguridad del inventario;
- seleccionar controles y fuentes según ámbito;
- medir calidad, frescura y cobertura con supuestos;
- explicar falsos positivos, falsos negativos y limitaciones.

No existe umbral universal de cobertura. El criterio debe fijarse según población, sector, misión, capacidad de descubrimiento y tolerancia al riesgo.

## 11. L11 — Skill candidata y conocimiento operativo

La Skill candidata SKILL-FND-01-03-ASSET-MISSION-INVENTORY define precondiciones, entradas, método, salidas, validación y límites. No está activa ni registrada en skillbook. Requiere:
- autorización del alcance;
- fuentes de descubrimiento permitidas;
- no escanear OT activamente sin aprobación;
- registrar confianza y procedencia;
- revisión de owner;
- evidencia de dos ejecuciones independientes;
- aprobación conforme al protocolo de Skills.

## 12. L12 — Trazabilidad y mantenimiento

Registrar versión del esquema, IDs, fuentes, fechas, hashes, propietario, método de descubrimiento, confianza y cambios. Mantener historial de alta/baja, cambios de firmware, owner, ubicación, proveedor, conexión, criticidad y lifecycle_state.

Revisar inventario tras adquisiciones, cambios de arquitectura, despliegues cloud, cambios de proveedor, incidentes, migraciones, actualizaciones, retiros y cambios de misión. Los SLAs de actualización deben diferenciar activos efímeros, OT estable, endpoints y servicios cloud.

## Fuentes y vigencia

- NIST CSF 2.0, ID.AM: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-53 Rev. 5, Release 5.2.0; CM-8, PM-5, CM-12, CM-13: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-37 Rev. 2: https://doi.org/10.6028/NIST.SP.800-37r2
- NIST SP 800-30 Rev. 1: https://doi.org/10.6028/NIST.SP.800-30r1
- NISTIR 8286A Rev. 1 (2025): https://csrc.nist.gov/pubs/ir/8286/a/r1/final
- NIST SP 800-128: https://doi.org/10.6028/NIST.SP.800-128
- CISA et al., Foundations for OT Cybersecurity: Asset Inventory Guidance for Owners and Operators (2025): https://www.cisa.gov/sites/default/files/2025-08/joint-guide-foundations-for-OT-cybersecurity-asset-inventory-guidance_508c.pdf
- ISO/IEC/IEEE 15288:2023: https://www.iso.org/standard/81702.html
- ISO/IEC 27001:2022 + Amd 1:2024: https://www.iso.org/standard/27001

Las fuentes NIST y CISA se revisaron en las secciones indicadas y los catálogos ISO se consultaron solo por metadatos/abstract. No se declara lectura integral de estándares de pago. NISTIR 8286A original de 2021 fue retirado el 2025-12-18 y sustituido por Rev. 1; utilizar la revisión vigente.

## Estado de aceptación

El contenido cubre las doce capas en borrador. El laboratorio es sintético; el instrumento se prepara, no se administra. La revisión independiente y la validación de inventarios reales siguen pendientes. No promover madurez por estructura, cantidad de campos o ejecución de CI.
