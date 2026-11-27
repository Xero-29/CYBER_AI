# Foundations — mapa curricular exhaustivo V2

**ID:** `foundations`  
**Estado:** mapa ampliado de trabajo; no equivale a cobertura desarrollada ni aprobada.  
**Propósito:** fijar el alcance disciplinar de Foundations antes de cerrar las capas de cada unidad.  
**Norma:** `knowledge/COLD_KNOWLEDGE_EXECUTION_PROTOCOL.md`.

## 1. Frontera disciplinar

Foundations enseña los modelos generales para razonar sobre seguridad de sistemas sociotécnicos y construir argumentos de confianza. No sustituye los módulos especializados. Debe proporcionar conceptos, métodos y criterios que permitan comprenderlos y conectarlos.

**Incluye:** propiedades de seguridad y confianza; modelado de sistemas y activos; límites de confianza; ingeniería de seguridad; amenazas y riesgo; identidad y autorización como conceptos transversales; criptografía y protección de datos como fundamentos; detección/respuesta/resiliencia; gobierno, assurance, medición e investigación.

**Deriva a especialidades:** configuración profunda de IAM/OIDC/SAML/PAM; protocolos de red; explotación y desarrollo seguro; ingeniería criptográfica y PKI avanzada; análisis de malware; forense especializado; SIEM/EDR; privacidad jurídica por jurisdicción; safety de sectores críticos; OT/ICS; seguridad cloud, móvil, hardware y AI. Foundations debe explicar el fundamento y los criterios de integración, no duplicar la especialidad.

## 2. Taxonomía jerárquica

### FND-01 — Propiedades, conceptos y modelos de seguridad
- FND-01.01 Seguridad, safety, privacidad, confiabilidad, disponibilidad y resiliencia: definiciones, diferencias y conflictos.
- FND-01.02 CIA y propiedades ampliadas: autenticidad, responsabilidad, trazabilidad, no repudio, integridad de origen y seguridad funcional.
- FND-01.03 Activo, sujeto, objeto, recurso, dato, proceso, servicio, misión y stakeholder.
- FND-01.04 Política, mecanismo, control, salvaguarda, requisito, garantía, evidencia y riesgo residual.
- FND-01.05 Modelos de control de acceso: DAC, MAC, RBAC, ABAC; modelo de referencia, límites y composición.
- FND-01.06 Modelos de confianza: perímetro, Zero Trust, confianza explícita, delegación y confianza transitoria.
- FND-01.07 Modelos de seguridad clásicos y formales: Bell-LaPadula, Biba, Clark-Wilson, Brewer-Nash; aplicabilidad y límites.
- FND-01.08 Principios de diseño: mínimo privilegio, mediación completa, fail-safe defaults, separación de funciones, economía de mecanismo, open design y defense in depth.
- FND-01.09 Propiedades emergentes, fallos comunes, dependencias y límites del razonamiento por componentes.
- FND-01.10 Ontología común, vocabulario controlado y errores conceptuales recurrentes.

### FND-02 — Sistemas, activos, contexto y ciclo de vida
- FND-02.01 Sistema de interés, contexto operacional, misión, objetivos y fronteras de análisis.
- FND-02.02 Inventario de hardware, software, firmware, identidades, datos, servicios, procesos y terceros.
- FND-02.03 Clasificación de activos y datos por sensibilidad, criticidad, impacto y obligaciones.
- FND-02.04 Propietario, custodio, operador, consumidor, proveedor y responsabilidad compartida.
- FND-02.05 Descubrimiento, reconciliación, resolución de entidades, procedencia y confianza de inventario.
- FND-02.06 Dependencias técnicas, organizativas, físicas, cloud y supply chain; concentración y puntos únicos de fallo.
- FND-02.07 Activos efímeros, shadow IT, BYOD, SaaS, serverless, recursos desconectados y activos no observables.
- FND-02.08 Gestión de configuración, baseline, drift, cambios y deuda técnica.
- FND-02.09 Adquisición, desarrollo, despliegue, operación, mantenimiento, transferencia, retiro y sanitización.
- FND-02.10 Inventario como grafo dinámico; cobertura, frescura, sesgo de observación y calidad de datos.

### FND-03 — Arquitectura, límites de confianza e ingeniería de seguridad
- FND-03.01 Descomposición de sistemas, arquitectura lógica/física y vistas de stakeholder.
- FND-03.02 Flujos de datos, flujos de autoridad, interfaces, estados y protocolos.
- FND-03.03 Límites de confianza, dominios administrativos, zonas, planos de control y datos.
- FND-03.04 Requisitos de seguridad derivados de misión, pérdidas temidas y escenarios.
- FND-03.05 Ingeniería de requisitos: trazabilidad, verificabilidad, completitud, consistencia y priorización.
- FND-03.06 Secure Systems Engineering, ciclo de vida, iteración, recursividad y assurance.
- FND-03.07 Arquitectura de referencia, patrones, separación, aislamiento y defensa en profundidad.
- FND-03.08 Verificación, validación, revisión, análisis, pruebas y evidencia: diferencias y relación.
- FND-03.09 Trade studies, análisis multicriterio, restricciones, coste, rendimiento y riesgo.
- FND-03.10 Modos degradados, resiliencia arquitectónica, recuperación y eliminación segura.

### FND-04 — Amenazas, vulnerabilidades y análisis de riesgo
- FND-04.01 Amenaza, actor, capacidad, intención, oportunidad, evento, vulnerabilidad, exposición, impacto y riesgo.
- FND-04.02 Adversarios intencionales, error humano, accidente, fallo técnico, desastre y dependencia.
- FND-04.03 Superficie de ataque técnica, humana, física, organizativa y de terceros.
- FND-04.04 STRIDE, misuse/abuse cases, árboles de ataque, DFD y modelado de amenazas.
- FND-04.05 Grafos de ataque, precondiciones, transiciones, rutas AND/OR y alcanzabilidad.
- FND-04.06 FMEA/FMECA, fault trees, bow-tie, análisis causal y causa raíz.
- FND-04.07 Riesgo contextual: horizonte, escenarios, probabilidad condicionada, impacto y decisión.
- FND-04.08 Incertidumbre aleatoria/epistémica, calidad de evidencia, sesgos y desacuerdo experto.
- FND-04.09 Sensibilidad, escenarios extremos plausibles, colas, dependencia y riesgo sistémico.
- FND-04.10 Priorización, tratamiento, aceptación, transferencia, evitación y riesgo residual.
- FND-04.11 Límites de CVSS, matrices ordinales, taxonomías y scores; no confundir puntuación con riesgo contextual.
- FND-04.12 Actualización del modelo ante cambios, incidentes, amenazas y nuevas dependencias.

### FND-05 — Identidad, autenticación, autorización y confianza
- FND-05.01 Identidades humanas, máquinas, servicios, workloads, dispositivos y agentes.
- FND-05.02 Identificación, autenticación, autorización, accounting y auditoría: separación conceptual.
- FND-05.03 Factores de autenticación, MFA, phishing resistance, passkeys y recuperación de cuenta.
- FND-05.04 Sesiones, tokens, claims, scopes, audiencia, expiración, replay y revocación.
- FND-05.05 Autorización centralizada/local, PDP/PEP, atributos, políticas y enforcement.
- FND-05.06 RBAC/ABAC/ReBAC/capability-based access: modelos, composición y trade-offs.
- FND-05.07 Federación, delegación, impersonation, confused deputy y cadena de confianza.
- FND-05.08 Identidades privilegiadas, separación de funciones y acceso de emergencia.
- FND-05.09 Ciclo de vida de identidades, alta/cambio/baja, cuentas huérfanas y permisos residuales.
- FND-05.10 Consistencia, caché, TOCTOU, revocación y fail-open/fail-closed.
- FND-05.11 Evidencia de identidad y auditoría con minimización de datos.
- FND-05.12 Límites del fundamento: protocolos e implementaciones detalladas se desarrollan en Identity.

### FND-06 — Criptografía y protección de información
- FND-06.01 Objetivos criptográficos: confidencialidad, integridad, autenticación, firma y establecimiento de claves.
- FND-06.02 Entropía, aleatoriedad, nonces, IV, semillas, generadores y errores de uso.
- FND-06.03 Cifrado simétrico, modos, AEAD y requisitos de nonce.
- FND-06.04 Criptografía asimétrica, firmas, KEM, intercambio de claves y PKI.
- FND-06.05 Hash, MAC, KDF, derivación, salting y compromisos.
- FND-06.06 Gestión de claves: generación, distribución, almacenamiento, uso, rotación, recuperación y destrucción.
- FND-06.07 Secretos, certificados, trust stores, HSM/KMS y separación de funciones.
- FND-06.08 Datos en reposo, tránsito y uso; cifrado, tokenización, seudonimización y minimización.
- FND-06.09 Criptoanálisis y fallos de implementación: side channels, downgrade, replay, nonce reuse y RNG.
- FND-06.10 Agilidad criptográfica, migración post-cuántica, inventario y dependencias.
- FND-06.11 Validación, estándares, módulos criptográficos y límites de claims de cumplimiento.
- FND-06.12 Límites del fundamento: pruebas de seguridad y protocolos avanzados se desarrollan en Crypto.

### FND-07 — Controles, detección, respuesta y resiliencia
- FND-07.01 Control preventivo, detectivo, correctivo, disuasivo, compensatorio y recuperación.
- FND-07.02 Diseño de controles, objetivos, owner, alcance, frecuencia, excepción y evidencia.
- FND-07.03 Observabilidad, telemetría, logs, eventos, métricas, trazas y procedencia.
- FND-07.04 Integridad, sincronización temporal, retención, privacidad y cadena de custodia.
- FND-07.05 Detección, hipótesis, correlación, tasa base, falsos positivos/negativos y triage.
- FND-07.06 Gestión de incidentes, severidad, escalamiento, comunicación y coordinación.
- FND-07.07 Contención, erradicación, recuperación, validación y prevención de recurrencia.
- FND-07.08 Continuidad, análisis de impacto, funciones críticas, RTO/RPO y dependencias.
- FND-07.09 Backup, restauración, identidad, claves, configuración y recuperación de proveedores.
- FND-07.10 Métricas operativas, MTTD/MTTA/MTTR, cobertura, completitud y límites interpretativos.
- FND-07.11 Control assurance: diseño, implementación, operación, eficacia y riesgo residual.
- FND-07.12 Automatización, supervisión humana, criterios de parada y rollback.

### FND-08 — Gobierno, privacidad, compliance y assurance
- FND-08.01 Gobierno, gestión, estrategia, apetito, tolerancia y autoridad de decisión.
- FND-08.02 Roles, accountability, tres líneas, independencia y conflictos de interés.
- FND-08.03 Políticas, estándares internos, procedimientos, excepciones y gestión de cambios.
- FND-08.04 Obligaciones legales, contractuales, regulatorias y sectoriales; jurisdicción y vigencia.
- FND-08.05 Privacidad: finalidad, minimización, proporcionalidad, derechos y ciclo de vida de datos.
- FND-08.06 Safety y análisis de peligros cuando exista impacto físico/ambiental.
- FND-08.07 Terceros, subprocesadores, cadena de suministro, concentración, continuidad y salida.
- FND-08.08 Gestión de riesgo empresarial y tecnológico, tratamiento y aceptación formal.
- FND-08.09 NIST CSF/RMF/800-53, ISO, CIS y otros marcos: alcance y no equivalencia.
- FND-08.10 Assurance cases: claims, argumentos, evidencia, supuestos y derrotadores.
- FND-08.11 Auditoría, evaluación independiente, certificación y límites de atestación.
- FND-08.12 Comunicación ejecutiva, reporte de riesgo, excepciones y mejora continua.

### FND-09 — Métodos cuantitativos, evaluación e investigación
- FND-09.01 Lógica, conjuntos, relaciones, predicados, invariantes y lógica temporal.
- FND-09.02 Grafos, árboles, redes, alcanzabilidad y análisis de dependencias.
- FND-09.03 Probabilidad, Bayes, dependencia, tasas base y calibración.
- FND-09.04 Estadística descriptiva/inferencial, muestreo, intervalos y tamaños de efecto.
- FND-09.05 Incertidumbre, sensibilidad, análisis de escenarios y valor de información.
- FND-09.06 Métricas, denominadores, prevalencia, sesgo, validez y comparabilidad.
- FND-09.07 Diseño experimental, variables, controles, baselines y amenazas a validez.
- FND-09.08 Benchmarks, ground truth, etiquetado, acuerdo interevaluador y contaminación.
- FND-09.09 Revisión sistemática, estrategia de búsqueda, inclusión/exclusión y síntesis crítica.
- FND-09.10 Hipótesis falsables, reproducibilidad, resultados negativos y límites de generalización.
- FND-09.11 Investigación aplicada: pregunta, método, datos, análisis, incertidumbre y conclusión.
- FND-09.12 Comunicación técnica y visualización sin falsa precisión.

## 3. Mapa de dependencias

- FND-01 es prerrequisito conceptual de todas las unidades.
- FND-02 y FND-03 alimentan FND-04 y FND-08.
- FND-04 define escenarios y requisitos para FND-05, FND-06 y FND-07.
- FND-05 y FND-06 implementan propiedades y límites derivados de FND-01/03/04.
- FND-07 usa activos, amenazas, controles y telemetría de FND-02/04/05/06.
- FND-08 gobierna decisiones, responsabilidades, obligaciones y assurance sobre todas las anteriores.
- FND-09 proporciona métodos de análisis y evaluación a todas las unidades; sus métodos deben usarse solo cuando sus supuestos sean adecuados.

## 4. Matriz de correspondencia con los siete temas base

| Tema base actual | Unidades curriculares principales |
|---|---|
| Modelos de seguridad y confianza | FND-01, FND-03, FND-05 |
| Inventario y clasificación de activos | FND-02 |
| Superficie de ataque y modelado de amenazas | FND-03, FND-04 |
| Identidad y control de acceso | FND-05 |
| Criptografía y protección de datos | FND-06 |
| Detección, respuesta y recuperación | FND-07 |
| Gobierno, riesgo y aseguramiento | FND-04, FND-08, FND-09 |

Los siete temas iniciales siguen siendo IDs estables de la matriz histórica. Esta taxonomía añade subunidades y cobertura transversal; no debe borrar ni renombrar los IDs existentes. En la siguiente iteración se descompondrán los siete temas en unidades/subtemas auditables y se vincularán a las doce capas y cuatro capacidades.

## 5. Brechas que este mapa hace visibles

- Formal methods y análisis de invariantes deben aparecer como currículo explícito, no solo como fórmulas dispersas.
- Ingeniería de requisitos, arquitectura y trade studies requieren mayor granularidad.
- La gestión de identidades no humanas, delegación y revocación necesita tratamiento más allá del IAM humano.
- La gestión de claves y la agilidad criptográfica deben distinguirse de la mera enumeración de algoritmos.
- Continuidad, restauración, dependencias críticas y recuperación de confianza deben estar conectadas.
- Privacidad, safety y obligaciones jurisdiccionales deben distinguirse de seguridad de la información.
- Gobierno de terceros, concentración y salida de proveedor necesitan subtemas propios.
- Métodos cuantitativos, calidad de benchmarks, sesgo y validez científica deben formar una base transversal explícita.
- Deben desarrollarse casos integradores que crucen arquitectura, riesgo, identidad, criptografía, detección y gobierno.

## 6. Condición de aceptación de G1

G1 permanece `in_progress` hasta que:
1. cada subunidad tenga alcance, prerrequisitos, objetivos y exclusiones;
2. se identifiquen temas faltantes por revisión de fuentes y comparación con dominios especializados;
3. el grafo de dependencias no tenga prerrequisitos circulares injustificados;
4. cada subunidad se vincule a las doce capas aplicables y a las cuatro capacidades;
5. se resuelvan duplicaciones con módulos especializados sin eliminar los fundamentos comunes;
6. un revisor disciplinar compruebe que el mapa cubre el dominio Foundations sin omisiones esenciales.

**Este mapa no marca ninguna celda como aprobada.** Su incorporación inicia el desarrollo curricular ampliado y la auditoría de contenido por subunidad.
