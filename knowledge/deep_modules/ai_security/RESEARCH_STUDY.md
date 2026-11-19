# Investigación técnica: Seguridad de IA, LLM, RAG y agentes

**ID:** ai_security · **Corte:** 2026-11-18 · **Madurez inicial:** M1/M2 en elaboración · **Evaluación adversarial independiente:** pendiente.

## Modelo del sistema
Un sistema de IA debe modelarse como cadena de componentes: datos de origen, preparación, entrenamiento/ajuste, pesos y tokenizer, runtime/inferencia, prompts privilegiados, memoria, recuperación RAG, herramientas, plugins, conectores, identidad, políticas, interfaz, observabilidad y proveedores externos. La frontera de seguridad no termina en el modelo: incluye todo el contexto que puede influir en sus decisiones y todas las acciones que puede provocar.

Clasificar activos: prompts e instrucciones privilegiadas, secretos, documentos, datos personales, pesos, embeddings, índices, credenciales de herramientas, outputs y logs. Dibujar flujos y trust boundaries entre usuario, modelo, fuentes recuperadas, herramientas, servicios y operadores.

## Taxonomía de riesgos y controles
### Prompt injection directa e indirecta
Contenido no confiable puede intentar alterar el comportamiento del modelo. La inyección indirecta puede venir en documentos, páginas, tickets, correos, repositorios, imágenes o resultados de herramientas. No existe una separación semántica perfecta entre instrucciones y datos en un LLM general.

Defensas: tratar contenido recuperado como dato no confiable; mantener autorización fuera del modelo y aplicarla en código determinista; no permitir que el modelo convierta texto no confiable en comandos sin validación; reducir privilegios y herramientas por tarea; separar lectura de escritura y plan de ejecución; aplicar validación de esquema y revisión humana para acciones de impacto; probar ataques multilingües, codificados, fragmentados y multimodales.

### Exceso de agencia y herramientas
La salida del modelo no es autorización. Cada operación debe pasar un punto de enforcement: identidad del solicitante, permiso, objetivo, alcance, riesgo, vigencia, límite de recursos y confirmación. Usar credenciales de workload con scopes mínimos, no secretos globales compartidos. Separar herramientas de consulta de herramientas que modifican estado. Requerir aprobación humana para escaneo activo, cambios, datos sensibles o acciones irreversibles. El agente debe poder abstenerse ante falta de permisos o evidencia.

### RAG y contaminación del corpus
Amenazas: documentos maliciosos, poisoning, datos obsoletos, ACL rotas, retrieval cross-tenant, citas inventadas, duplicados, ranking manipulado y fuga por embeddings/logs.

Controles: provenance con hash, editor, licencia, fecha, versión y parser; extracción en sandbox con límites de CPU/memoria/tiempo; ACL en retrieval y pruebas cross-tenant; fragmentos con referencia estable a página/sección; reranking medido; deduplicación y freshness; citas obligatorias; separar evidencia, inferencia e hipótesis. Nunca ejecutar instrucciones encontradas en documentos ni promover texto a Skill automáticamente.

### Datos, modelos y supply chain
Evaluar poisoning, backdoors, data leakage, memorization, membership inference, model extraction, artefactos manipulados, dependencias, tokenizer, datasets, adapters/LoRA y endpoints externos. Registrar hashes de pesos/config/tokenizer, origen, licencia, versión, SBOM/model BOM cuando proceda y evaluación previa al despliegue.

### Output handling y fuga
La salida puede ser incorrecta o peligrosa. Validar JSON/esquemas, escapar HTML/SQL/shell, parametrizar consultas y no concatenar output en comandos. Redactar secretos y PII en logs. El self-check del mismo modelo no es control suficiente.

### Disponibilidad y coste
Probar context flooding, loops de agentes, fan-out, herramientas lentas, retry storms, límites de tokens, rate limits y agotamiento de presupuesto. Aplicar timeouts, límites de pasos, cuotas, circuit breakers, idempotencia y kill switch.

## Arquitectura de referencia para agentes
1. Policy plane: reglas deterministas, identidad, permisos, scope y aprobación.
2. Planning plane: el modelo propone pasos, sin poder saltarse policy.
3. Execution plane: ejecutores aislados con interfaces tipadas y allowlists.
4. Knowledge plane: corpus versionado, provenance, ACL y filtros.
5. Evidence plane: logs append-only, correlación, redacción y hashes.
6. Human control plane: revisión, revocación, break-glass y parada de emergencia.

El modelo nunca debe poseer credenciales de administrador. Las herramientas reciben capacidades temporales y limitadas. Resultados de herramientas son datos no confiables: validar esquema, integridad, origen, timestamps y tamaño antes de pasarlos a otro agente.

## Evaluación de seguridad
Construir una matriz con ataque, precondición, componente, objetivo, severidad y comportamiento esperado. Incluir prompt directo/indirecto, retrieval poisoning, cross-tenant, secret exfiltration, tool misuse, privilege escalation, output injection, denial of wallet, loop y fallback. Añadir casos benignos similares para medir falsos positivos. Variar idioma, codificación, longitud, contexto, multimodalidad y orden de mensajes.

Métricas: attack success rate por clase, leakage rate, unauthorized action rate, policy bypass rate, citation precision, retrieval recall@k, false refusal, false acceptance, tool call correctness, coste, p95 latency y recuperación tras fallo. Reportar intervalos de confianza y no mezclar resultados de datasets/modelos distintos.

## Laboratorios seguros
- Corpus RAG sintético con documentos benignos y documentos con instrucciones hostiles; medir si se tratan como datos.
- Herramientas mock con operaciones read/write y permisos distintos; intentar exceder scope.
- Dataset sintético multitenant para probar ACL y aislamiento.
- Simulador de agente con límites de pasos, coste y timeout; probar loops y fallos de proveedor.
- Secretos canario sintéticos para evaluar exposición.
- Parsers/ingestión con archivos corruptos, grandes y comprimidos en sandbox.

No introducir secretos reales ni probar proveedores externos con datos sensibles sin contrato y autorización.

## Requisitos específicos para CYBER_AI
La autorización de objetivos y ejecución de herramientas debe estar en código determinista, no en el prompt. Documentos y salidas de herramientas deben marcarse como no confiables. Skillbook exige provenance, revisión y regresión; una conversación exitosa no basta para promover una Skill. Retrieval debe respetar ACL, versiones y estado editorial. Agentes deben citar fuentes, expresar incertidumbre y abstenerse ante evidencia insuficiente. CI debe incluir pruebas adversariales de prompt injection, tool misuse, RAG poisoning y cross-tenant.

## Fuentes primarias
- NIST AI RMF 1.0: https://doi.org/10.6028/NIST.AI.100-1
- NIST Generative AI Profile AI 600-1: https://doi.org/10.6028/NIST.AI.600-1
- OWASP Top 10 for LLM Applications: https://owasp.org/projects/top-10-for-large-language-model-applications
- MITRE ATLAS: https://atlas.mitre.org/
- NIST NICE Framework v2.2.0: https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220

**Estado de evidencia:** se revisaron páginas oficiales y resúmenes de proyectos/estándares. Las pruebas descritas son diseños de evaluación, no experimentos ejecutados ni certificación del sistema.
