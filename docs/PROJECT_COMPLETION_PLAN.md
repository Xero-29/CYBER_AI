# Plan maestro de cierre de CYBER_AI

**Corte de análisis:** 2026-11-17  
**Rama de referencia:** `main`  
**HEAD observado:** `125f6a21fa08c38188b2d4ce8fe52ceb95fe7c05`  
**Tipo de revisión:** análisis estático del repositorio, documentación, estructura, contratos y evidencia CI disponible. No es una auditoría de penetración ni una validación operacional completa.

## 1. Visión de producto y definición de terminado

CYBER_AI debe ser una plataforma modular de investigación y operaciones de ciberseguridad asistidas por IA. El proveedor de modelos debe ser intercambiable sin perder la biblioteca, las memorias, las Skills, las políticas ni la evidencia. El sistema debe poder comprender una tarea, identificar dominios pertinentes, recuperar conocimiento y metodologías verificadas, seleccionar capacidades, solicitar autorización cuando corresponda, ejecutar herramientas dentro de límites técnicos, validar los resultados y conservar evidencia trazable. El aprendizaje debe convertir experiencias en metodologías reutilizables solo después de verificación independiente.

El sistema no se considerará terminado por acumular módulos, herramientas o documentos. Cada capacidad debe tener un propósito, un consumidor, contratos explícitos, pruebas positivas y negativas, observabilidad, límites de seguridad y evidencia de funcionamiento.

### Criterios globales de cierre

1. **Coherencia:** visión, arquitectura, CLI, inventarios, perfiles, documentación y pruebas describen el mismo comportamiento.
2. **Integración:** cada subsistema está conectado a un flujo real o queda explícitamente identificado como herramienta independiente.
3. **Conocimiento utilizable:** contenido con procedencia, versión, vigencia, licencias, extracción, indexación y recuperación evaluada; distinguir contenido propio, referencias catalogadas y fuentes realmente revisadas.
4. **Calidad técnica:** pruebas automatizadas, integración con proveedores reales, herramientas reales y laboratorios autorizados; resultados medidos y reproducibles.
5. **Seguridad:** mínimo privilegio, denegación por defecto, aislamiento de procesos y red, autorización verificable, secretos externos y evidencia íntegra.
6. **Operabilidad:** instalación reproducible, preflight honesto, backups/restauración probados, logs, límites de recursos y procedimientos de recuperación.
7. **Gobierno:** riesgos aceptados por responsables, revisión independiente, licencias y release gates aprobados.

No se promete una cobertura universal y perpetuamente completa de toda la ciberseguridad. Se define una cobertura mantenible y medible por dominios, resultados, versiones y escenarios. El marco de referencia transversal será NIST CSF 2.0 (Govern, Identify, Protect, Detect, Respond, Recover), complementado con estándares y taxonomías especializados por dominio.

## 2. Diagnóstico consolidado

### Capacidades presentes

- CLI principal para tareas, equipos de agentes, informes, lotes, escaneo autorizado y autopruebas.
- DIRECTOR, agentes especializados, orquestador multiagente, planificador, contratos de workflows y simulador.
- Adaptadores de proveedores Ollama, OpenAI-compatible, Anthropic y Gemini; contrato de plugins externos.
- Recuperación híbrida de conocimiento, SQLite/FTS, embeddings, aislamiento de fragmentos por tenant, bootstrap, reindexación e ingestión documental.
- 48 paquetes de conocimiento offline, 48 perfiles de dominio y módulos de profundización con agendas y revisiones bibliográficas.
- Inventario y adaptadores de herramientas, runner Docker para YARA/TShark, runner remoto de Nuclei y autorización central de red.
- Ledger, grafo de evidencia, memoria, Skillbook, promoción controlada, regresión de Skills y auditoría del ciclo de aprendizaje.
- Backups, preflight, SBOM, manifiesto de artefactos de dependencias y CI Python/Docker.
- Último CI observado sobre HEAD: Python y Docker sandbox completados correctamente.

### Brechas confirmadas o explícitamente reconocidas

**P0 — Coherencia del producto**
- README y documentos históricos contienen recuentos y estados anteriores de herramientas, CI y capacidades.
- La matriz de implementación contiene filas/tablas malformadas y estados de CI de commits antiguos.
- La auditoría institucional tiene fecha y rama históricas; no debe usarse como diagnóstico vigente sin una nueva pasada.
- Falta un documento canónico que relacione objetivo, subsistemas, consumidores, contratos y criterios de aceptación.

**P1 — Seguridad de ejecución**
- Aislamiento general de adaptadores host y herramientas personalizadas pendiente.
- Nmap no fuerza firewall/aislamiento de egress a nivel del sistema operativo.
- Nuclei necesita transporte con DNS fijado, validación de cada destino/redirección y política de egress aplicada fuera del proceso.
- OSV-Scanner y Grype necesitan preflight de presencia, esquema y vigencia de bases locales.
- pip-audit sigue bloqueado por política de red.
- Allowlist HMAC no resuelve identidad individual, custodia/rotación de claves ni TOCTOU.
- Plugins de proveedores/herramientas se ejecutan con privilegios del proceso; falta un límite de confianza operativo más fuerte.

**P1 — Conocimiento**
- Los 48 paquetes offline son una base editorial propia, no una enciclopedia ni corpus experto exhaustivo.
- Los compendios de profundización conservan patrones genéricos repetidos y deben desarrollarse con contenido específico por subtema.
- Las revisiones son M1/exploratorias; agendas y experimentos propuestos no son investigaciones ejecutadas.
- Las referencias externas están catalogadas, pero la licencia, lectura integral, extracción y validación siguen pendientes por artefacto.
- Falta corpus de preguntas y juicios de relevancia revisados por especialistas para medir recuperación real.
- OCR, parsers aislados y validación real de PDF/Office requieren trabajo adicional.

**P1 — Integración inteligente**
- DIRECTOR y selectores usan principalmente reglas léxicas; la búsqueda semántica no gobierna todavía la selección de especialista.
- El planificador relaciona dominios, herramientas y Skills, pero el mapeo no equivale a cobertura operativa.
- Falta evaluación de selección de agentes, abstención, confianza, desambiguación, recuperación y calidad de respuestas con modelos reales.
- La simulación multiagente valida contratos y transferencia de contexto, no razonamiento ni coordinación semántica real.

**P1 — Gobierno y operación institucional**
- RBAC/IdP/MFA y separación de funciones end-to-end no están demostrados.
- KMS/HSM o firmante externo, revocación y doble aprobación pendientes.
- Checkpoints externos firmados/WORM, backups cifrados off-host y restauración/DR con RPO/RTO aprobados pendientes.
- Carga, concurrencia, soak, disco lleno, pérdida de host, recuperación y monitoreo/alertas pendientes.
- Revisión independiente del threat model, privacidad, retención, licencias y riesgos pendientes.

**P2 — Portabilidad**
- Linux es el objetivo de ejecución documentado.
- Windows continúa aplazado por decisión anterior; no debe declararse compatible mientras no se implemente y valide el soporte de locks, permisos, procesos, rutas y ACL.

## 3. Plan de acción priorizado

### Fase 0 — Establecer una única verdad del proyecto (P0)

**Trabajo**
1. Crear y mantener este plan como hoja de ruta canónica.
2. Actualizar README, PROJECT_STATUS, IMPLEMENTATION_MATRIX, CONTEXT y TOOL_ECOSYSTEM para que los recuentos, estados y límites coincidan con el código y CI actuales.
3. Convertir auditorías antiguas en historial claramente fechado; no borrar evidencia histórica, pero separar diagnóstico vigente de cronología.
4. Corregir Markdown/tablas y enlaces rotos; comprobar todos los comandos publicados contra la CLI actual.
5. Crear un mapa de arquitectura que conecte entrada → política → planificación → conocimiento/Skills → proveedor → herramientas → validación → ledger/evidencia → informe.
6. Añadir una matriz de trazabilidad: requisito → módulo → consumidor → pruebas → estado operacional → evidencia/commit.

**Aceptación**
- No existen cifras contradictorias entre documentos canónicos.
- Cada módulo principal tiene un consumidor y contrato identificables.
- Los comandos documentados existen y sus argumentos corresponden al parser.
- La matriz no marca como cerrado nada que solo esté catalogado, simulado o pendiente de infraestructura.

### Fase 1 — Endurecer ejecución y fronteras de confianza (P1, bloquea piloto)

**Trabajo**
1. Diseñar un runner común aislado para herramientas locales: contenedor/VM desechable, filesystem mínimo, usuario no privilegiado, límites CPU/RAM/PIDs/tiempo/salida, mounts de solo lectura, sin socket Docker y sin red por defecto.
2. Mantener Nmap en un runner de red separado; aplicar allowlist de destinos y puertos con firewall/namespace de red obligatorio. El proceso debe fallar cerrado si el aislamiento no está activo.
3. Completar Nuclei con DNS pinning en el transporte real, protección frente a rebinding, control de redirecciones y egress allowlist. No habilitar dominios hasta superar pruebas negativas.
4. Implementar preflight OSV-Scanner/Grype que valide binario, versión, DB local, esquema, fecha y política de antigüedad; nunca descargar automáticamente durante un escaneo offline.
5. Resolver pip-audit mediante un modo offline/DB compatible o documentarlo como no disponible; no retirar la barrera de red sin una política explícita.
6. Mitigar TOCTOU de ejecutables mediante artefactos inmutables o ejecución por descriptor/imagen fijada, no solo hash antes/después.
7. Añadir política de límites común para adaptadores y herramientas personalizadas, con resultados tipados y estado de aislamiento comprobable.

**Aceptación**
- Pruebas de escape, acceso a rutas fuera del workspace, escritura del objetivo, acceso a secretos, egress, DNS rebinding, redirecciones, timeout y agotamiento de recursos.
- Una herramienta local no puede abrir red por defecto.
- Nmap/Nuclei no conectan fuera del alcance autorizado aunque el agente lo solicite.
- La evidencia registra imagen/binario, versión, hash, política aplicada, objetivo, duración, salida y estado de aislamiento.
- No se declara aislamiento si el control depende únicamente de flags del ejecutable.

### Fase 2 — Convertir la biblioteca en conocimiento evaluable (P1)

**Trabajo**
1. Auditar las 48 áreas por subtema, identificando contenido duplicado, genérico, superficial, obsoleto o sin evidencia.
2. Reescribir cada compendio con contenido específico: modelos, arquitectura, protocolos, técnicas, detecciones, mitigaciones, casos, errores frecuentes y límites.
3. Mapear cada dominio a resultados de NIST CSF 2.0 y, cuando aplique, MITRE ATT&CK/ATLAS, CWE/CVE, OWASP, CIS, NIST SP, ISO/IEC, IEC/OT y estándares del sector.
4. Revisar referencias una a una: URL canónica, emisor, edición, fecha, licencia, hash, páginas/secciones consultadas y fecha de revisión.
5. Priorizar fuentes oficiales, estándares y papers revisados por pares; separar borradores, blogs, advisories y opiniones.
6. Construir corpus local permitido y datasets sintéticos; no incorporar documentos protegidos o sin licencia.
7. Mejorar extracción: fixtures reales PDF/DOCX/XLSX/PPTX, OCR opcional aislado para escaneados, preservación de página/tabla/código y validación contra archivos malformados.
8. Crear benchmark de recuperación por dominio con consultas, documentos relevantes y juicios independientes; medir Recall@K, Precision@K, MRR, latencia y citas correctas.
9. Crear pruebas de contaminación de corpus, prompt injection documental, contenido contradictorio, obsoleto y aislamiento tenant.

**Aceptación**
- Cada área tiene mapa de subtemas, contenido específico y lagunas explícitas.
- Cada fuente consumida tiene procedencia y licencia revisadas; catálogo no equivale a ingestión.
- La recuperación encuentra los fragmentos esperados y cita documento/versión/página cuando corresponda.
- Umbrales de calidad definidos por dominio y publicados con el benchmark.
- No se declara L4/L5 sin investigación ejecutada, resultados, incertidumbre y revisión independiente.

### Fase 3 — Hacer la coordinación de IA robusta y agnóstica (P1)

**Trabajo**
1. Unificar contratos de chat, embeddings, herramientas y revisión; añadir pruebas de compatibilidad por proveedor.
2. Sustituir la selección puramente léxica de DIRECTOR por enrutamiento híbrido: reglas, metadatos, recuperación semántica, reranking y abstención.
3. Definir capacidades verificables por agente: dominio, herramientas permitidas, requisitos, límites, coste y contexto.
4. Hacer que el planificador construya un plan explicable con evidencia de selección, dependencias, autorización requerida, riesgos y condiciones de parada.
5. Probar flujos multiagente reales: transferencia, crítica, desacuerdo, revisión, timeout, caída de proveedor, respuesta malformada y presupuesto agotado.
6. Introducir evaluación de calidad por tarea y dominio; no aceptar formato correcto como prueba de exactitud.
7. Añadir timeouts, reintentos limitados, circuit breaker y fallback ante fallos transitorios sin confundirlos con fallback de capacidad.
8. Validar prompt injection en tareas, resultados de herramientas, documentos, memoria y Skills.

**Aceptación**
- Selección de agente y recuperación medidas en un dataset revisado.
- El sistema puede abstenerse cuando no tiene conocimiento/capacidad suficiente.
- Fallos de un proveedor no corrompen ledger ni duplican acciones.
- Ningún texto del modelo, documento o herramienta puede conceder permisos.
- Cada paso del flujo queda ligado al objetivo, política, modelo/versión y evidencia.

### Fase 4 — Cerrar el ciclo de aprendizaje (P1)

**Trabajo**
1. Formalizar esquema de evidencia para cada ejecución y revisión independiente.
2. Incorporar firmante externo/KMS-HSM con identidad, rotación, revocación, aprobación separada y doble control.
3. Mantener historial append-only, versiones, rollback y auditoría de Skills.
4. Construir dataset real de tareas/Skills por dominio y benchmark de regresión revisado por especialistas.
5. Detectar degradación, obsolescencia y contradicción de Skills; desactivar de forma segura.
6. Asegurar que una tarea fallida o no verificada nunca se convierta en conocimiento activo.

**Aceptación**
- Skill activa vinculada a ejecuciones reproducibles, evidencia con hash, revisor independiente y firma verificable.
- Recuperación solo incluye Skills compatibles, vigentes y aprobadas.
- Existe rollback probado y el historial alterado se rechaza.

### Fase 5 — Resiliencia, privacidad y operación (P1)

**Trabajo**
1. Definir modelo de identidad y roles para operador, analista, aprobador, administrador y auditor.
2. Añadir gestor de secretos, cifrado en reposo, rotación, revocación y política de retención.
3. Exportar checkpoints firmados a almacenamiento externo inmutable; separar administrador del runtime y custodio de evidencia.
4. Probar backup/restauración cifrados, corrupción, pérdida de host, pérdida de clave y recuperación.
5. Ejecutar pruebas de carga, concurrencia, soak, disco lleno, memoria, procesos colgados y apagado abrupto.
6. Incorporar logging estructurado, métricas, alertas, trazas y redacción de secretos/PII.
7. Definir RPO/RTO, respuesta a incidentes del propio CYBER_AI y procedimiento de actualización/rollback.

**Aceptación**
- Restauración completa demostrada en entorno limpio.
- Checkpoints verificables fuera del host.
- Roles y separación de funciones probados.
- Límites y alertas medidos en infraestructura objetivo.

### Fase 6 — Validación operacional y release controlado (P1/P2)

**Trabajo**
1. Ejecutar preflight y `verify.sh` desde checkout limpio.
2. Instalar y validar proveedores reales, empezando por un proveedor local y uno remoto opcional.
3. Ejecutar herramientas reales con fixtures y objetivos de laboratorio controlados.
4. Ejecutar laboratorios reproducibles por dominios prioritarios; registrar falsos positivos/negativos.
5. Revisar el threat model con una persona independiente y resolver hallazgos críticos/altos.
6. Activar branch protection, required checks, revisión de dependencias, SBOM, licencias y firma de release.
7. Producir una versión etiquetada con manifiesto de componentes, compatibilidad, riesgos aceptados y guía de actualización.

**Aceptación**
- Gates A–E de `docs/RELEASE_GATES.md` satisfechos o excepciones aceptadas por escrito con responsable y vencimiento.
- Evidencia asociada al SHA exacto de release.
- No quedan vulnerabilidades críticas/altas sin tratamiento o aceptación formal.
- El sistema se instala, ejecuta, observa y recupera en un entorno limpio.

### Fase 7 — Portabilidad Windows (P2, aplazada)

Solo iniciar después de cerrar el objetivo Linux y confirmar la prioridad. Sustituir dependencias POSIX, implementar ACL/DACL, locks, procesos y rutas nativas, runner de aislamiento equivalente y CI Windows completo. No anunciar soporte por pasar únicamente tests de configuración.

## 4. Orden de ejecución y dependencias

| Orden | Fase | Prioridad | Puede avanzarse solo con código | Requiere entorno/decisión |
|---|---|---|---|---|
| 1 | Fase 0: coherencia | P0 | Sí | No |
| 2 | Fase 1: seguridad de ejecución | P1 | Contratos, preflight, pruebas y runner | Firewall/VM, validación hostil real |
| 3 | Fase 2: conocimiento | P1 | Auditoría, redacción, benchmark y pipeline | Licencias, corpus y revisión experta |
| 4 | Fase 3: coordinación IA | P1 | Contratos, enrutamiento y pruebas simuladas | Cuentas/modelos y evaluación semántica |
| 5 | Fase 4: aprendizaje | P1 | Contratos, auditoría y benchmark | KMS/HSM, aprobadores y revisión |
| 6 | Fase 5: operación | P1 | Interfaces, políticas y pruebas | IdP, gestor secretos, WORM, infraestructura |
| 7 | Fase 6: release | P1 | CI, documentación y automatización | Pruebas reales, revisión y aceptación de riesgos |
| 8 | Fase 7: Windows | P2 | Parcial | Runner Windows y validación local |

## 5. Métricas que se publicarán

No publicar un porcentaje único que mezcle código, conocimiento y operación. Mantener cinco indicadores separados:

- **Implementación:** requisitos con código integrado / requisitos de código definidos.
- **Integración:** capacidades con consumidor real y contrato probado / capacidades que el producto promete.
- **Conocimiento:** subtemas con contenido revisado y fuentes verificadas / subtemas definidos; publicar aparte descargado, ingerido, indexado y recuperable.
- **Verificación:** requisitos con pruebas aprobadas sobre el SHA actual / requisitos verificables.
- **Operación:** escenarios reales superados con evidencia / escenarios operacionales definidos.

Cada indicador debe tener denominador, fecha de corte, evidencia y exclusiones. Una simulación no cuenta como prueba real; CI no cuenta como validación de modelo o herramienta real.

## 6. Riesgos de alcance y decisiones

- La meta no es instalar todas las herramientas existentes, sino cubrir capacidades necesarias con herramientas mantenidas, verificadas y aisladas.
- No se debe descargar indiscriminadamente conocimiento: licencias, privacidad, procedencia, coste y vigencia son criterios obligatorios.
- No se debe habilitar ejecución irrestricta para mejorar comodidad. El objetivo es capacidad amplia dentro de límites explícitos y autorizados.
- La cobertura profunda de todas las especialidades es un programa continuo de investigación y mantenimiento; el cierre del producto inicial exige un conjunto priorizado de dominios con calidad medida y una arquitectura extensible para el resto.
- Windows sigue aplazado hasta una decisión expresa.

## 7. Próximo bloque de trabajo

Empezar por **Fase 0** y corregir las contradicciones documentales; en paralelo, preparar el diseño y los contratos de aislamiento de la Fase 1. Después implementar las brechas de seguridad que bloquean cualquier piloto con herramientas reales. No aumentar el catálogo de herramientas ni declarar más dominios como expertos antes de cerrar las brechas de integración, evidencia y validación.
