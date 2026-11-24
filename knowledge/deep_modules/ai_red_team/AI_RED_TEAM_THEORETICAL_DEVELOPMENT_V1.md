# Desarrollo teórico profundo V1 — Red Team de IA y agentes

**ID:** `ai_red_team`  
**Versión:** 1.0.0  
**Etapa:** capacidades en frío.  
**Madurez declarada:** borrador técnico profundo en desarrollo; no T4, no validación operativa.  
**Fuentes:** véase `knowledge/research/domain_investigations/AI_RED_TEAM_GAP_RESEARCH_2026-11-19.md` y el registro de fuentes.  
**Seguridad:** todos los ejemplos de abuso se limitan a modelos, datos, herramientas y entornos propios o expresamente autorizados. Los ejemplos usan secretos canary y datos sintéticos; no se incluyen objetivos externos ni credenciales reales.

## 0. Perfil disciplinar y modelo unificador

El Red Team de IA evalúa la seguridad del sistema sociotécnico completo que incorpora modelos predictivos o generativos, aplicaciones, prompts, recuperación, memoria, herramientas, agentes, identidad, infraestructura, datos, personas y gobierno. No equivale a probar únicamente si un modelo produce una respuesta prohibida.

### 0.1 Activos y propiedades de seguridad

- **Confidencialidad:** prompts privados, datos recuperados, secretos, credenciales, datos personales, parámetros/modelos y resultados.
- **Integridad:** corpus, índices, memoria, configuración, instrucciones de sistema, herramientas, resultados y decisiones.
- **Disponibilidad:** inferencia, retrieval, herramientas, colas, cuotas, presupuesto y servicios dependientes.
- **Autoridad:** identidad del usuario, identidad del agente, permisos delegados, scopes, sesiones, credenciales y aprobaciones.
- **Trazabilidad:** procedencia de documentos, llamadas, decisiones, cambios, evidencias y responsables.
- **Seguridad de acciones:** que ninguna salida textual pueda convertirse en una acción privilegiada sin autorización independiente.

### 0.2 Componentes y límites de confianza

Modelo base → capa de orquestación → ensamblador de contexto → recuperación/memoria → planificador → broker de herramientas → identidad/autorización → herramientas/servicios → almacenamiento/logging.

Cada flecha es un flujo de datos o autoridad que debe caracterizarse. Los límites críticos suelen estar entre:
1. instrucciones privilegiadas y contenido no confiable;
2. usuario y agente;
3. agente y broker de herramientas;
4. tenant y corpus/índice compartido;
5. contexto recuperado y memoria persistente;
6. herramienta y sistema operativo/servicio externo;
7. ejecución y registro de evidencia.

### 0.3 Modelo formal de amenaza

Representar un sistema como (S=(A,D,I,P,T,L)), donde:
- (A): activos;
- (D): datos y sus etiquetas de integridad/confidencialidad;
- (I): identidades y sujetos;
- (P): políticas y permisos;
- (T): transformaciones, herramientas y transiciones;
- (L): logs, procedencia y evidencias.

Una amenaza es una tupla (h=(actor,capacidad,entrada,precondición,transición,activo,impacto)). Una ruta de ataque es una secuencia de transiciones permitidas por la arquitectura real; una cadena imaginada sin precondiciones demostrables se conserva como hipótesis, no como hallazgo.

Para cada ruta se documentan: actor, acceso, conocimiento, objetivo, precondiciones, trust boundaries, pasos, control esperado, evidencia necesaria, impacto, probabilidad contextual, incertidumbre y regla de parada.

### 0.4 Regla central de evaluación

La respuesta del modelo no es el resultado de seguridad. La unidad de evaluación es el efecto observable en el sistema: ¿se accedió a un dato?, ¿se cruzó un tenant?, ¿se invocó una herramienta?, ¿se modificó estado?, ¿se realizó una acción no autorizada?, ¿se generó un coste o indisponibilidad? Una negativa textual no demuestra bloqueo si la herramienta ya se ejecutó.

---

# Tema 1. Plan de pruebas y threat model

## L1. Fundamentos teóricos
El threat model identifica qué debe protegerse, frente a quién, bajo qué capacidades y con qué consecuencias. Diferenciar activo, amenaza, vulnerabilidad, exposición, evento, impacto, riesgo, control y evidencia. Distinguir red team (validar rutas de impacto), blue team (detección/defensa), purple team (aprendizaje coordinado) y evaluación de seguridad del modelo (propiedades del modelo). No reducir el alcance a prompt injection: incluir identidad, infraestructura, supply chain, datos y procesos humanos.

## L2. Fundamentos matemáticos y formales
Modelar componentes como grafo dirigido (G=(V,E)), donde nodos representan activos/identidades/servicios y aristas flujos de datos o autoridad. Las rutas críticas son caminos desde una entrada controlable por adversario hasta un activo/acción sensible. Usar probabilidad condicionada con cautela: (P(impacto|ruta, controles, contexto)), no multiplicar puntuaciones ordinales como si fueran probabilidades independientes. El riesgo requiere impacto, probabilidad, exposición, controles y confianza de la estimación. Aplicar STRIDE, árboles de ataque, grafos de ataque o análisis de flujo de información según el problema; explicar la elección.

## L3. Arquitectura y funcionamiento interno
Inventariar modelo/version, system/developer prompts, plantillas, parsers, RAG, almacenes vectoriales, memoria, agentes, herramientas, conectores, APIs, IAM, redes, secretos, colas, logs, CI/CD, datasets, evaluadores y proveedores. Diagramar secuencia de llamada, flujo de datos, flujo de autoridad y persistencia. Identificar qué componente valida cada transición y qué componente puede ejecutar efectos secundarios.

## L4. Estándares y metodologías
Usar NIST AI RMF y NIST AI 600-1 como gestión de riesgo de IA; MITRE ATLAS como conocimiento adversario vivo; OWASP GenAI LLM Top 10 2026 para riesgos de aplicaciones LLM; OWASP Top 10 for Agentic Applications 2026 para riesgos de agentes; ATT&CK/CWE cuando correspondan a infraestructura/software. Son taxonomías y marcos con propósitos distintos, no certificaciones ni equivalentes. Versionar los snapshots porque ATLAS y catálogos vivos cambian.

## L5. Implementación técnica
El paquete de evaluación debe definir manifiesto de alcance, inventario, grafo de activos, matriz de actores/capacidades, casos, etiquetas de datos, política de autorización, telemetría y formato de evidencia. Cada caso contiene ID, objetivo, precondiciones, pasos, resultado esperado, criterio de éxito/fallo, limpieza y rollback. Revisar estáticamente que ningún caso pueda salir del entorno autorizado.

## L6. Análisis avanzado
Incluir amenazas combinadas: inyección indirecta que altera memoria y luego invoca herramienta; compromiso de dependencia que introduce instrucciones; fuga a través de logs; permisos residuales tras cambio de usuario; cache compartida entre tenants; fallos de aprobación humana; retries que duplican acciones; y diferencias entre sandbox y producción. Evaluar rutas alternativas y fallos de controles en cascada.

## L7. Perspectiva de seguridad
Definir reglas de alcance, autorización escrita, límites de red, presupuesto, datos sintéticos, cuentas de prueba, mínimos privilegios, snapshots, supervisión, kill switch y criterios de parada. Prever respuesta, preservación de evidencia, contención, limpieza y notificación. Una prueba no autorizada o fuera de alcance es un fallo de proceso, aunque revele una vulnerabilidad.

## L8. Investigación científica
Pregunta ejemplo: «¿Qué límites de confianza y controles arquitectónicos reducen acciones no autorizadas en agentes conectados a RAG y herramientas?». Separar revisión conceptual de hipótesis empírica. Predefinir unidad de análisis, arquitectura, escenarios, comparadores, variables, método de muestreo, criterio de éxito y amenazas a validez. No inferir causalidad de un único caso.

## L9. Laboratorios y datasets
Diseñar una aplicación local ficticia con dos tenants, documentos sintéticos, agente, broker mock y herramientas sin efectos externos. Dataset debe incluir ground truth, clase de amenaza, severidad esperada, control esperado y etiqueta de tenant. Guardar versión, licencia, esquema, hash y particiones. Estado actual: diseño especificado; ejecución de este nuevo protocolo pendiente.

## L10. Evaluación y benchmarks
Medir cobertura de activos/rutas, proporción de casos con resultado verificable, tasa de acciones no autorizadas, fuga de canary, falsos positivos, tiempo de detección y riesgo residual. Publicar denominadores, intervalos, casos no aplicables y exclusiones. No usar una única puntuación agregada para ocultar fallos críticos.

## L11. Conocimiento operativo y Skills
Especificar Skill de scoping y modelado: entradas (autorización, arquitectura, inventario), salidas (scope manifest, DFD, threat model), validaciones, permisos de solo lectura por defecto, prohibiciones, parada y rollback. No promover como Skill ejecutable hasta probarla y revisarla.

## L12. Trazabilidad y mantenimiento
Registrar propietario, alcance, fecha, versión del sistema, modelo, proveedores, dependencias, hash de manifiestos, fuentes, analista, decisiones, exclusiones, evidencia, hallazgos y revisión. Reabrir el modelo ante cambios de modelo, prompts, herramientas, permisos, corpus o infraestructura.

---

# Tema 2. Prompt injection directa, indirecta, persistente y multimodal

## L1. Fundamentos teóricos
Prompt injection ocurre cuando contenido controlado por un adversario influye en la interpretación o conducta del sistema de IA de forma que altera objetivos, políticas o flujo de control. La directa llega desde la entrada del usuario; la indirecta se introduce por documentos, páginas, correos, imágenes, audio, resultados de herramientas o contenido recuperado. Diferenciarla de jailbreak: el jailbreak suele buscar cambiar el comportamiento de contenido/política del modelo; la inyección puede comprometer el control de una aplicación conectada a datos o acciones. Pueden coexistir.

## L2. Fundamentos matemáticos y formales
Tratar instrucciones y datos como etiquetas de integridad distintas. Un modelo recibe secuencia (x) que combina instrucciones privilegiadas (i) y contexto no confiable (u); la arquitectura debe evitar que (u) adquiera autoridad por aparecer en el mismo contexto. El flujo de información puede modelarse como taint/provenance: cada fragmento conserva origen, tenant, integridad y permisos. No existe un clasificador perfecto de intención semántica que garantice separar instrucciones y datos en todos los casos.

## L3. Arquitectura y funcionamiento interno
Analizar ensamblado de prompts, delimitadores, serialización, tool outputs, retrieval, memoria, resúmenes, historial multi-turn, entradas multimodales, OCR, transcripción, parser y salida estructurada. Un payload puede atravesar ingestión → chunking → embedding → retrieval → resumen → memoria → prompt futuro. La persistencia y propagación deben formar parte del modelo, no solo la interacción de una vuelta.

## L4. Estándares y metodologías
Mapear LLM01:2026 Prompt Injection, LLM08:2026 Hidden Context Exposure, LLM09:2026 Vector and Embedding Weaknesses y LLM10:2026 Improper Output Handling de OWASP 2026; complementar con técnicas y mitigaciones pertinentes de MITRE ATLAS y riesgos de agente de OWASP ASI. Los números y nombres deben fijarse a la edición consultada. NIST AI 600-1 aporta gestión de riesgos, no una lista de payloads ni una garantía de mitigación.

## L5. Implementación técnica
Diseñar controles en capas: separar datos de instrucciones en arquitectura; conservar provenance; reducir contexto al mínimo; escapar/serializar datos según formato; validar salidas como datos no confiables; prohibir que el texto del modelo cambie permisos; validar acciones en servidor; usar allowlists y schemas estrictos; aplicar aprobación humana a acciones de alto impacto. El filtrado de texto es defensa auxiliar, no frontera de seguridad. Ejemplo de revisión estática: verificar que los argumentos de herramienta se validen fuera del modelo y que una instrucción en un documento no pueda cambiar el principal autorizado.

## L6. Análisis avanzado
Estudiar indirect injection, multi-turn, delayed trigger, payload splitting, encoded/obfuscated content, multimodal OCR/steganographic cues, prompt leaking, context confusion, retrieval hijacking, memory poisoning y tool output injection. Considerar que sanitización puede destruir contenido benigno, que reglas léxicas tienen bypass y que modelos distintos interpretan igual contexto de forma diferente. Documentar false refusal y degradación de utilidad.

## L7. Perspectiva de seguridad
Controles: origen y confianza por fragmento; aislamiento de contexto; permisos mínimos; egress restringido; secret isolation; validación de acciones; revisión humana; logs con hashes; borrado de memoria contaminada; revocación de tokens; respuesta y retest. La regla es que el contenido externo nunca otorga autoridad ni cambia ACL.

## L8. Investigación científica
Pregunta: ¿qué controles reducen el éxito de inyección indirecta y persistente sin bloquear tareas benignas? Hipótesis deben separar ataque directo/indirecto, modalidad, persistencia, arquitectura y agente. Revisar literatura con protocolo explícito, separar estudios de modelos aislados de estudios end-to-end y evaluar calidad, corpus, modelos, prompts, número de intentos y reproducibilidad.

## L9. Laboratorios y datasets
Diseñar corpus sintético con instrucciones benignas, payloads directos e indirectos, documentos, HTML/Markdown, JSON/XML, imágenes con texto, transcripciones, cadenas multi-turn y contenido recuperado. Incluir casos negativos difíciles, canaries y ground truth. Separar train/dev/test y evitar que variantes casi idénticas filtren entre particiones. Ejecución pendiente.

## L10. Evaluación y benchmarks
Métricas: attack success rate por categoría, acción no autorizada, leakage rate, false refusal rate, utility retention, robustez ante variaciones, persistencia, detección y coste. Definir éxito por efecto real, no por respuesta textual. Reportar intervalo de confianza y resultados por modalidad/arquitectura.

## L11. Conocimiento operativo y Skills
Skill de evaluación de prompt injection: verifica alcance, usa corpus sintético, ejecuta únicamente en harness aislado, clasifica resultado, preserva evidencia saneada y limpia memoria/índices de prueba. La Skill no puede enviar payloads a servicios de terceros ni cambiar controles de producción sin autorización explícita.

## L12. Trazabilidad y mantenimiento
Registrar modelo y versión, system prompt/configuración, plantilla, parser, herramientas, corpus/hash, modalidad, número de turnos, semillas cuando apliquen, fecha, resultado bruto, criterio de éxito y cambios de mitigación. Revalidar tras cambios de modelo, OCR, retrieval, prompt assembly o memoria.

---

# Tema 3. Abuso de herramientas, agencia y autoridad delegada

## L1. Fundamentos teóricos
La agencia añade capacidad de planificar y ejecutar transiciones con efectos secundarios. El riesgo no es solo generar instrucciones incorrectas, sino que el sistema actúe con autoridad mayor que la intención o permiso del usuario. Distinguir agente, herramienta, plugin/conector, broker, principal, identidad de workload, credencial, capability, scope y aprobación. El modelo no es un principal de seguridad confiable por sí mismo.

## L2. Fundamentos matemáticos y formales
Modelar autorización como función (allow(subject, action, resource, context)). El sujeto debe ser identidad verificable; el modelo no debe poder autoasignarse roles. Aplicar mínimo privilegio, separación de funciones, capabilities de alcance estrecho, expiración y revocación. Analizar confused deputy cuando un componente con privilegios usa su autoridad en beneficio de una entrada menos privilegiada. Para acciones, definir invariantes: no superar permisos, no cruzar tenant, no ejecutar sin aprobación exigida, no duplicar operaciones no idempotentes.

## L3. Arquitectura y funcionamiento interno
Separar planner/LLM, tool router, policy enforcement point, policy decision point, credential broker y ejecutor. El broker debe validar identidad, scope, recurso, argumentos, estado y aprobación. Las herramientas deben tener contratos explícitos, esquema tipado, timeout, cuota, idempotency key, límites de salida y registro de auditoría. Las credenciales no deben estar en el prompt ni ser devueltas al modelo.

## L4. Estándares y metodologías
Mapear OWASP Agentic Top 10 (goal hijack, tool misuse, identity/privilege abuse, supply chain, unexpected code execution, memory/context poisoning y otras categorías según edición) y OWASP LLM Top 10 2026 Excessive Agency. Complementar con OAuth/OIDC, IAM, capability security, zero trust y controles de software seguro. No tratar una taxonomía como prueba de que un producto cumple.

## L5. Implementación técnica
Patrón seguro: el modelo propone una acción declarativa; un componente determinista valida schema, identidad y política; el ejecutor obtiene credencial limitada; acciones sensibles requieren aprobación vinculada a hash de argumentos; el resultado se sanea antes de volver al contexto. Denegar por defecto. Bloquear comandos arbitrarios; preferir operaciones de alto nivel. Añadir límites de volumen, destino, tiempo y coste.

## L6. Análisis avanzado
Analizar confused deputy, confused user, scope escalation, token substitution, confused identity, replay, race conditions, TOCTOU, retries, idempotencia, aprobación obsoleta, tool poisoning, MCP/A2A supply chain, inter-agent trust, memory-driven actions y cascading failures. Revisar qué pasa si el modelo cambia argumentos después de aprobación o si el recurso cambia entre validación y ejecución.

## L7. Perspectiva de seguridad
Separación de credenciales, allowlist de herramientas, scopes por tarea, aprobación de dos fases, límites de egress, sandbox, auditoría, kill switch, revocación, compensación/rollback y alertas por desviación. Una aprobación debe identificar usuario, acción exacta, recurso, argumentos y vigencia; no aprobar una intención vaga.

## L8. Investigación científica
Pregunta: ¿qué diseño de broker reduce acciones fuera de política en agentes sin degradar excesivamente utilidad/latencia? Comparar ejecución directa del modelo con broker policy-enforced. Medir acciones permitidas/bloqueadas, bypass, errores de autorización, duplicados, coste y tiempo. Distinguir pruebas de diseño de resultados reales.

## L9. Laboratorios y datasets
Diseñar herramientas mock (lectura, escritura reversible, envío simulado), identidades de dos niveles, recursos multi-tenant y acciones con diferentes impactos. Incluir casos de permiso insuficiente, argumento alterado, token expirado, replay, doble ejecución, aprobación obsoleta y herramienta comprometida simulada. No usar APIs productivas.

## L10. Evaluación y benchmarks
Métricas: tasa de acciones no autorizadas, tasa de denegación correcta, falsa denegación, ejecución duplicada, violación de scope, acciones sin aprobación, tiempo de revocación, latencia del broker y utilidad de tareas legítimas. El denominador debe ser el total de intentos/acciones por categoría.

## L11. Conocimiento operativo y Skills
Skill de invocación segura: validar permiso y alcance antes de llamar; presentar acción y argumentos exactos para aprobación; ejecutar una sola vez; verificar estado final; registrar evidencia; revertir si es seguro. Las Skills deben declarar herramientas permitidas, recursos, límites, efectos secundarios y fallback seguro.

## L12. Trazabilidad y mantenimiento
Registrar identidad del usuario y workload, policy version, tool ID/version/hash, scope, argumentos saneados, aprobación, idempotency key, resultado, código de salida, timestamps, revocación y correlación. Rotar/revocar ante incidente y revisar cada cambio de herramienta o proveedor.

---

# Tema 4. RAG poisoning, debilidades vectoriales y aislamiento multi-tenant

## L1. Fundamentos teóricos
RAG combina recuperación externa con generación. La seguridad depende de ingestión, extracción, chunking, embedding, indexación, ACL, búsqueda, reranking, contexto, generación y caché. Poisoning busca alterar qué contenido se recupera o cómo se interpreta; cross-tenant es exposición o interferencia entre dominios de autorización. Un vector similar no equivale a permiso para leer.

## L2. Fundamentos matemáticos y formales
Embeddings representan contenido en espacios vectoriales; similitud coseno o distancia L2 miden proximidad geométrica, no confiabilidad, verdad ni autorización. La búsqueda top-k tiene sesgos por chunking, modelo embedding, normalización, dimensionalidad y distribución del corpus. ACL debe ser una condición lógica de elegibilidad, no un filtro posterior confiado al LLM. La propiedad deseada: para consulta del sujeto s, todo fragmento retornado cumple (authorized(s, fragment)).

## L3. Arquitectura y funcionamiento interno
Describir conectores de ingestión, parser, OCR, normalizador, chunker, embedding model, vector DB, metadata store, retriever, reranker, cache, memoria y LLM. Marcar tenant, propietario, clasificación, origen, timestamp, firma/procedencia y política en metadata inmutable. Verificar que filtros se aplican antes de exponer contenido al modelo y también en cache, reranker, logs y resúmenes.

## L4. Estándares y metodologías
OWASP LLM Top 10 2026 incluye riesgos de data/model poisoning y vector/embedding weaknesses; MITRE ATLAS incluye RAG poisoning y técnicas de manipulación de artefactos; NIST AI RMF/AI 600-1 aporta gobierno y gestión del ciclo de vida. Las taxonomías deben mapearse a controles concretos de ingestión, procedencia, acceso y borrado.

## L5. Implementación técnica
Pipeline seguro: validar fuente y MIME; analizar contenido en sandbox; asignar provenance/tenant; escanear malware y contenido activo; registrar hash; chunking determinista versionado; embedding identificado; metadata ACL; query con filtro tenant/ACL obligatorio; revalidar antes de pasar al modelo; cache key incluye tenant y política; output y logs saneados. El LLM no debe decidir si el usuario puede acceder a un documento.

## L6. Análisis avanzado
Considerar poisoning de corpus, index poisoning, embedding collision/near-neighbor manipulation, chunk boundary attacks, metadata spoofing, stale ACL, cache poisoning, deletion inconsistency, retriever/reranker disagreement, summary contamination, document version rollback y cross-tenant side channels. Analizar borrado: retirar fuente no siempre elimina vectores, cachés, backups o resúmenes.

## L7. Perspectiva de seguridad
Controles: allowlist de fuentes, firma/procedencia, revisión de documentos sensibles, separación física/lógica de tenant, filtros server-side, cifrado, logging, detección de drift, quarantine, revocación, purge verificado y controles de acceso a índices. Riesgo residual: un documento autorizado puede ser falso o malicioso; procedencia no equivale a veracidad.

## L8. Investigación científica
Pregunta: ¿qué combinación de ACL, provenance y aislamiento reduce recuperación cross-tenant y poisoning sin empeorar recall legítimo? Comparar baseline sin filtros, ACL server-side, namespaces separados y controles de procedencia. Medir precision/recall de recuperación, leakage, contaminación, false block y latencia.

## L9. Laboratorios y datasets
Diseñar dos o más tenants con corpus sintéticos etiquetados, documentos benignos/maliciosos, duplicados, near-duplicates, ACL, cambios de permiso, borrado y caché. Ground truth por usuario/fragmento y consulta. Incluir consultas con permisos parciales y cambios de estado. Ejecución pendiente.

## L10. Evaluación y benchmarks
Medir cross-tenant leakage rate, unauthorized retrieval rate, poisoning success rate, retrieval precision/recall, source attribution accuracy, stale data exposure, deletion completeness, false denial, latency y costo. Separar retrieval correctness de answer correctness.

## L11. Conocimiento operativo y Skills
Skill de ingesta segura: valida procedencia, tenant, permisos, hash, contenido y parser; rechaza fuentes sin metadatos mínimos; registra cuarentena; exige purge y reindex controlados. Skill de consulta: verifica autorización server-side antes de retornar fragmentos y no delega ACL al modelo.

## L12. Trazabilidad y mantenimiento
Registrar dataset y licencia, origen, hash, tenant, parser/chunker/embedding versions, índice, ACL version, query, IDs de fragmento, cache hit, reranker, documento eliminado y evidencia de purge. Reprocesar/reindexar cuando cambien modelos, esquema o políticas.

---

# Tema 5. Exfiltración, divulgación sensible y extracción de modelos/datos

## L1. Fundamentos teóricos
Separar divulgación accidental, exfiltración deliberada, extracción de entrenamiento, extracción de modelo, membership inference, model inversion, inferencia de atributos, fuga de contexto oculto y fuga por herramientas/logs. El objetivo y el activo son distintos: recuperar un secreto no es lo mismo que inferir si un registro participó en entrenamiento o aproximar parámetros/función del modelo.

## L2. Fundamentos matemáticos y formales
Confidencialidad puede expresarse como restricción de flujo: datos de alta sensibilidad no deben alcanzar salidas de menor confianza sin una política de declassificación. Membership inference estima (P(recordin training|observations)); model inversion infiere propiedades/entradas a partir de salidas; extracción intenta reconstruir datos o comportamiento. Las métricas dependen del baseline, tasa base, balance y umbral; accuracy aislada puede ser engañosa.

## L3. Arquitectura y funcionamiento interno
Mapear secretos en prompts, contexto, RAG, memoria, logs, traces, embeddings, checkpoints, caches, tool outputs, analytics y backups. Identificar egress por UI, API, correo, almacenamiento, herramientas, plugins, A2A/MCP y telemetría. Distinguir datos en tránsito, reposo y uso.

## L4. Estándares y metodologías
OWASP LLM Top 10 2026 Sensitive Information Disclosure y Hidden Context Exposure; NIST AI RMF/AI 600-1 para privacidad/gobierno; guías de privacidad y controles de datos aplicables según jurisdicción. MITRE ATLAS ayuda a organizar técnicas de recolección/exfiltración, pero debe mapearse a sistemas y evidencia concretos.

## L5. Implementación técnica
Minimizar contexto; no insertar secretos innecesarios; tokenizar/seudonimizar; aplicar DLP y clasificación en puntos de salida; separar logs de datos sensibles; controlar egress; usar secret manager; limitar consultas y cuotas; filtrar campos; aplicar output schema; usar canaries sintéticos para detección. Los filtros de salida no sustituyen la minimización y control de acceso en origen.

## L6. Análisis avanzado
Estudiar extracción por repetición, prompts adaptativos, side channels de longitud/tiempo, error messages, embeddings, cachés, logs, memoria, herramientas y salidas multimodales. Analizar riesgos de over-redaction, pérdida de utilidad, fuga por correlación y ataques de baja tasa que evaden umbrales. Diferenciar extracción de modelo de simple imitación de unas pocas salidas.

## L7. Perspectiva de seguridad
Controles: clasificación, mínimo privilegio, retención limitada, encryption, egress policies, cuotas, monitoreo, detección de canaries, rotación de secretos, respuesta de privacidad, notificación y borrado. Diseñar minimización y acceso por propósito. No almacenar datos personales reales en laboratorios.

## L8. Investigación científica
Pregunta: ¿qué controles reducen la fuga de secretos y datos de entrenamiento manteniendo utilidad legítima? Definir activos sintéticos, atacante, presupuesto de consultas, acceso, conocimiento auxiliar y criterio de extracción. Comparar controles y medir privacidad/utility trade-off; declarar limitaciones de generalización.

## L9. Laboratorios y datasets
Dataset sintético con secretos canary únicos por tenant, datos públicos y privados ficticios, ejemplos de entrenamiento sintético y consultas benignas. Crear etiquetas de sensibilidad y ground truth de exposición. No usar corpus personales, secretos reales ni intentar extraer datos de modelos de terceros.

## L10. Evaluación y benchmarks
Métricas: canary exposure rate, sensitive disclosure rate, membership inference AUC/advantage con baseline de tasa base, extraction precision/recall, query budget, utility retention, false positive/negative y tiempo de detección. Informar tamaño de muestra y distribución.

## L11. Conocimiento operativo y Skills
Skill de revisión de salida: clasifica sensibilidad, valida destinatario y propósito, aplica política de egress, bloquea salida de secreto, registra evento y ofrece respuesta segura. Skill de respuesta: preservar evidencia saneada, revocar credenciales, rotar secretos, identificar alcance y verificar purge.

## L12. Trazabilidad y mantenimiento
Registrar clasificación, origen, consentimiento/licencia, retención, transformaciones, destinos, controles, logs saneados, canaries, versiones de modelo y políticas, y evidencia de borrado/rotación. Mantener cadena de custodia cuando el caso sea forense.

---

# Tema 6. Evaluación adversarial, benchmarks y calidad de evidencia

## L1. Fundamentos teóricos
Evaluar significa operacionalizar una propiedad y medirla bajo un protocolo. Un benchmark es una muestra finita de escenarios, no la totalidad del espacio de amenazas. Diferenciar validez de constructo, interna, externa y ecológica; confiabilidad, reproducibilidad, robustez y utilidad. El resultado debe corresponder a un efecto de seguridad definido.

## L2. Fundamentos matemáticos y formales
Para tasa de éxito (ASR=x/n), informar numerador, denominador e intervalo de confianza; con muestras pequeñas usar intervalos binomiales adecuados (por ejemplo Wilson o exactos), no solo aproximación normal. Precision (TP/(TP+FP)), recall (TP/(TP+FN)), FPR (FP/(FP+TN)). Medir por categoría y severidad. Para comparación emparejada, preservar el mismo conjunto de casos y reportar diferencias con incertidumbre. No tratar prompts correlacionados como observaciones independientes.

## L3. Arquitectura y funcionamiento interno
Separar generador de casos, runner, orquestador, modelo, herramientas, instrumentación, oracle/ground truth, evaluador y agregador. Registrar cada etapa. Un fallo del logger no debe confundirse con éxito de defensa. El evaluador no debe usar la misma heurística que la defensa sin auditoría de sesgo.

## L4. Estándares y metodologías
Contrastar NIST AI RMF/AI 600-1, OWASP 2026, MITRE ATLAS, protocolos de evaluación adversarial y marcos de reporte de investigación. Registrar qué requisito es normativo, guía comunitaria, taxonomía, benchmark o método académico. No sumar listas de riesgos incompatibles sin normalizar conceptos.

## L5. Implementación técnica
Definir manifiesto de experimento, esquema de caso, runner determinista cuando sea posible, normalización de salidas, oracle explícito, logging, versionado, seeds y generación de reporte. Separar scoring automático y revisión humana; calibrar evaluadores y resolver desacuerdos con reglas previas.

## L6. Análisis avanzado
Controlar contaminación de benchmark, prompt leakage, overfitting de defensa, selección adversarial de muestras, drift de modelo, variabilidad estocástica, sesgo de publicación, survivorship bias, distribución fuera de dominio y efectos de retries. Reportar negativos, casos ambiguos y exclusiones. No comparar modelos con context windows, herramientas o presupuestos distintos sin normalización.

## L7. Perspectiva de seguridad
Proteger dataset, runner y resultados; evitar que los payloads se ejecuten fuera del sandbox; fijar límites de coste y llamadas; sanear logs; mantener separación de test y datos de entrenamiento; auditar supply chain de herramientas y modelos.

## L8. Investigación científica
Pregunta ejemplo: «¿La defensa arquitectónica reduce la acción no autorizada frente a defensa solo por prompt bajo casos directos e indirectos?». Pre-registro de hipótesis, variables, muestra, criterios, baseline y análisis. Documentar desviaciones del protocolo y separar exploratorio de confirmatorio.

## L9. Laboratorios y datasets
Crear corpus versionado con etiquetas, severidad, modality, tenant, actor, preconditions, expected effect, control under test y ground truth. Mantener train/dev/test separados; publicar licencias y hashes; guardar casos difíciles y negativos. No exponer payloads que permitan atacar sistemas reales fuera del contexto de prueba.

## L10. Evaluación y benchmarks
Métricas principales: ASR por impacto, unauthorized action rate, leakage rate, false refusal, utility retention, precision/recall de detección, cobertura, latencia y coste. Incluir intervalos, tamaños de efecto, análisis por subgrupo y robustez a variantes. Definir umbrales antes de ver resultados y justificar el costo de falsos positivos/negativos.

## L11. Conocimiento operativo y Skills
Skill de benchmark: valida versiones y hashes, carga casos autorizados, verifica aislamiento, ejecuta con límites, evalúa mediante oracle, conserva resultados brutos y genera informe con incertidumbre. Debe abortar si falta ground truth, alcance o integridad de dataset.

## L12. Trazabilidad y mantenimiento
Guardar protocolo, preregistro, commit, entorno, modelo, prompt, herramientas, dataset hash, semilla, muestras, exclusiones, resultados brutos, análisis, scripts, revisores y desviaciones. Versionar cada benchmark; no sobrescribir resultados anteriores.

---

# Tema 7. Retest, severidad, reporte y cierre de hallazgos

## L1. Fundamentos teóricos
Un hallazgo es una afirmación respaldada sobre una condición, ruta y efecto dentro de un alcance. Separar observación, inferencia, causa raíz, impacto potencial y riesgo residual. El retest verifica si una corrección cambió la condición bajo las mismas precondiciones y si introdujo regresiones.

## L2. Fundamentos matemáticos y formales
La severidad debe considerar impacto, alcance, facilidad, privilegio, exposición, repetibilidad y confianza de evidencia. CVSS puede ser útil para vulnerabilidades técnicas compatibles, pero no captura por sí solo impacto de negocio, privacidad, autonomía o contexto de IA. Definir reglas de scoring transparentes y no presentar ordinales como probabilidades. En retest, comparar antes/después con mismas entradas y condiciones; distinguir no reproducible de corregido.

## L3. Arquitectura y funcionamiento interno
El reporte debe enlazar activo, versión, ruta, identidad, dato, herramienta, política, evento, log, evidencia y control. Mantener IDs estables para hallazgo, caso, artefacto y retest. Proteger datos sensibles y evitar que el informe mismo se convierta en canal de exfiltración.

## L4. Estándares y metodologías
Alinear el formato con prácticas de divulgación responsable, gestión de vulnerabilidades y respuesta a incidentes; usar taxonomías de severidad adecuadas al dominio. Mapear a OWASP/MITRE/NIST como referencia, no como prueba automática de severidad.

## L5. Implementación técnica
Estructura mínima: resumen ejecutivo; alcance y exclusiones; arquitectura/versión; precondiciones; pasos reproducibles; evidencia mínima; resultado esperado/observado; impacto; probabilidad contextual; limitaciones; causa raíz; mitigación; riesgo residual; retest; anexos saneados. Incluir comandos solo para el entorno autorizado y evitar secretos o datos personales.

## L6. Análisis avanzado
Considerar falsos positivos, falsos negativos, hallazgos duplicados, causalidad múltiple, explotabilidad condicionada, mitigación parcial, bypass alternativo, regresión, cambio de modelo y drift. Un retest que pasa un caso no demuestra que la clase completa esté corregida; requiere cobertura de variantes y regresión.

## L7. Perspectiva de seguridad
Aplicar divulgación responsable, control de acceso al informe, cifrado, minimización, cadena de custodia, retención y notificación. Definir escalamiento para impacto crítico y regla de no explotación destructiva. Cerrar exposición temporal (tokens, URLs, canaries) al finalizar.

## L8. Investigación científica
Estudiar consistencia entre evaluadores, validez de severidad, reproducibilidad de hallazgos y tasa de regresión. Diseñar protocolo con evaluadores independientes, muestra, rúbrica y análisis de acuerdo (por ejemplo kappa cuando aplique), evitando tratarlo como medida universal de calidad.

## L9. Laboratorios y datasets
Dataset sintético de hallazgos con evidencias, severidad esperada, corrección, retest positivo/negativo y casos ambiguos. Incluir cambios que arreglan la causa raíz y cambios que solo bloquean un payload. Ejecución pendiente.

## L10. Evaluación y benchmarks
Métricas: reproducibility rate, precision de hallazgos, acuerdo interevaluador, tiempo de triage, retest pass rate, regression rate, porcentaje de hallazgos con evidencia suficiente y porcentaje de cierres con riesgo residual explícito.

## L11. Conocimiento operativo y Skills
Skill de reporte: verifica alcance y saneamiento, genera hallazgo con evidencia, propone remediación y define retest. Skill de cierre: exige evidencia posterior, valida variante/regresión y deja estado abierto si solo se probó un payload o falta evidencia. No puede cerrar automáticamente hallazgos críticos sin aprobación humana.

## L12. Trazabilidad y mantenimiento
Conservar IDs, timestamps, versión, hashes, evidencia saneada, decisiones, aprobaciones, remediación, retest y responsables. Registrar desacuerdos y reaperturas; mantener changelog y revisión periódica.

---

## 8. Síntesis crítica transversal

1. **No existe defensa basada exclusivamente en prompts que deba asumirse suficiente.** La autoridad de acciones debe imponerse fuera del modelo mediante identidad, política y controles deterministas.
2. **La seguridad del modelo no equivale a seguridad de la aplicación.** El wrapper, RAG, herramientas, memoria, conectores e infraestructura alteran el riesgo.
3. **La procedencia no equivale a veracidad; similitud vectorial no equivale a autorización; negativa textual no equivale a bloqueo de acción.**
4. **Las métricas deben medir consecuencias.** ASR sin definición de éxito, tasa sin denominador o benchmark sin ground truth no permite concluir eficacia.
5. **Los controles tienen trade-offs.** Sanitización, filtros y aprobaciones pueden degradar utilidad, crear latencia y falsos positivos; la evaluación debe medir ambos lados.
6. **El contexto cambia el riesgo.** Un mismo modelo puede ser seguro en chat aislado y peligroso con credenciales, RAG y herramientas privilegiadas.
7. **La evidencia debe ser reproducible y acotada.** No extrapolar resultados de una versión, modalidad, benchmark o proveedor a todos los sistemas.

## 9. Ejemplos resueltos de razonamiento (frío)

### Caso A — negativa textual con acción ejecutada
Un agente responde «no puedo borrar el recurso», pero el log del broker muestra una llamada DELETE aceptada antes de generar la respuesta. **Conclusión:** el control falló. El criterio es el efecto del sistema, no la prosa. Evidencia mínima: identidad, recurso, argumento, decisión de política, timestamp y resultado del ejecutor.

### Caso B — retrieval con tenant equivocado
Un usuario del tenant A consulta un documento y el retriever retorna un fragmento etiquetado B; el modelo no lo cita en la respuesta. **Conclusión:** ya ocurrió exposición en el límite de retrieval, aunque la salida final no revele el texto. Debe bloquearse antes del contexto y revisar logs, cache, reranker y memoria.

### Caso C — aprobación obsoleta
Un humano aprueba una transferencia de 10 unidades a la cuenta X. Después, el agente cambia el argumento a 1000 unidades y la herramienta ejecuta. **Conclusión:** la aprobación no estaba ligada a la acción exacta. Debe firmarse o hashearse el conjunto de argumentos y validarse de nuevo inmediatamente antes de ejecutar.

### Caso D — benchmark contaminado
Una defensa se ajusta repetidamente a un conjunto público de prompts y obtiene 99% de bloqueo en ese conjunto, pero cae en variantes semánticas no vistas. **Conclusión:** hay sobreajuste/contaminación; no hay evidencia de generalización. Separar test oculto, variantes, modelo/versiones y medición de utilidad.

### Caso E — documento confiable malicioso
Un PDF proviene de un repositorio aprobado y tiene firma válida, pero contiene instrucciones maliciosas destinadas al agente. **Conclusión:** la autenticidad de origen no garantiza benignidad ni autoridad de instrucción. Conservar provenance, tratar contenido como dato no confiable y bloquear cambios de política.

## 10. Evaluación en frío del módulo

La evaluación debe incluir al menos:
- 14 preguntas de conocimiento y discriminación conceptual;
- 7 problemas de modelado/diagnóstico (uno por tema);
- 7 ejercicios de diseño de controles;
- 7 ejercicios de lectura crítica de evidencia;
- 3 escenarios integradores RAG + herramientas + identidad;
- 1 diseño de benchmark con métricas y análisis de incertidumbre;
- rúbrica con exactitud, razonamiento, aplicación, evidencia, límites y seguridad.

La clave y las respuestas deben almacenarse separadas del instrumento. El umbral se calibra con evaluadores; no declarar administración a personas hasta que ocurra.

## 11. Plan de laboratorio y evaluación caliente (diseño solamente)

| ID | Propósito | Sistema sintético | Evidencia esperada |
|---|---|---|---|
| ART-L01 | Threat model y rutas | App local de agente | Grafo, activos, rutas y cobertura |
| ART-L02 | Prompt injection directa/indirecta | Harness local + documentos sintéticos | Acción/flujo observado y clasificación |
| ART-L03 | Tool misuse y autoridad | Broker mock + identidades | Decisión de política, argumentos y resultado |
| ART-L04 | RAG poisoning/cross-tenant | Vector store local + dos tenants | ACL, retrieval, cache y leakage |
| ART-L05 | Canary leakage | Dataset sintético | Tasa de exposición y controles |
| ART-L06 | Benchmark adversarial | Corpus versionado | Métricas, intervalos y resultados brutos |
| ART-L07 | Retest y reporte | Hallazgos sintéticos | Evidencia antes/después y regresión |

**Estado:** diseños de prueba; no ejecutados en esta entrega. No hay resultados empíricos ni validación de integraciones.

## 12. Registro de fuentes y límites de lectura

Fuentes prioritarias para el desarrollo:
- NIST AI 600-1, *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* (2024): perfil transversal del AI RMF para GenAI. La página oficial y metadatos fueron revisados; el PDF completo requiere lectura y extracción por secciones.
- MITRE ATLAS: base viva de tácticas/técnicas contra sistemas de IA, con plataformas predictiva, generativa y agéntica. Se inspeccionó la página oficial; el snapshot STIX y cada técnica deben revisarse por tema.
- OWASP GenAI LLM Top 10 2026: edición vigente consultada en la página oficial; el repositorio canónico y los diez riesgos deben revisarse por entrada.
- OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10): marco específico para riesgos de sistemas autónomos; revisar entradas, amenazas y mitigaciones. https://genai.owasp.org/top-10-for-agentic-applications-2026/
- Tang et al., *Security of LLM-based agents regarding attacks, defenses, and applications*, Information Fusion 127 (2026), artículo 103941: resumen/metadatos consultados; texto completo y método pendientes.
- Geng et al., *Prompt Injection Attacks on Large Language Models: A Survey of Attack Methods, Root Causes, and Defense Strategies*, Computers, Materials & Continua 87(1) (2026), DOI 10.32604/cmc.2025.074081: resumen/metadatos consultados; verificar texto completo, método Kitchenham, corpus y evaluación de calidad.
- Duarte et al., *A Systematic Review of Prompt Injection Attacks on Large Language Models: Trends, Taxonomy, Evaluation, Defenses, and Opportunities*, IEEE Access 14 (2026), DOI 10.1109/ACCESS.2026.3656849: resumen/metadatos consultados; texto completo pendiente.
- *A Systematic Survey of Prompt Injection Attacks and Defenses in LLM-Integrated Applications and Agentic Systems*, BigDIA 2026, DOI 10.1109/BigDIA71496.2026.11684636: resumen/metadatos consultados; texto completo pendiente.
- *Prompt-to-API-Call injection: Systematic attack generation and semantic defense in LLM agents*, Journal of Systems and Software (online 27 Oct 2026), DOI 10.1016/j.jss.2026.113164: resumen/metadatos consultados; texto completo pendiente.

**Disciplina de lectura:** ninguna de estas menciones implica por sí sola lectura integral, evaluación de calidad ni reproducción. Registrar páginas/secciones realmente leídas en `source_registry.json`. No copiar cifras de resúmenes como evidencia de eficacia general.

## 13. Brechas abiertas y condición de cierre teórico

- [ ] Leer textos completos prioritarios y registrar alcance, páginas, fecha, licencia y hash cuando se archive legalmente.
- [ ] Verificar cada entrada de OWASP 2026 y snapshot de MITRE ATLAS; construir matriz riesgo/técnica → componente → control → evidencia.
- [ ] Completar un inventario curricular ampliado: subtemas no cubiertos por los siete temas iniciales, supply chain, multi-agent, MCP/A2A, evaluación de modelos, privacidad, governance y seguridad de infraestructura.
- [ ] Añadir derivaciones y ejercicios matemáticos completos donde apliquen.
- [ ] Añadir bibliografía primaria y síntesis crítica con criterios de inclusión/exclusión.
- [ ] Construir clave y rúbrica de evaluación en frío.
- [ ] Auditoría adversarial documental de cada una de las 84 celdas tema×capa.
- [ ] Revisión independiente para aspirar a T4.
- [ ] Ejecución de los siete laboratorios en etapa caliente posterior.

**Salida actual:** desarrollo teórico V1 sustancial para los siete temas base; no se declara completitud del currículo, T4, G1–G8 aprobadas, ejecución de laboratorio ni eficacia operativa. La siguiente iteración debe cerrar las brechas documentales de este módulo antes de pasar al siguiente.
