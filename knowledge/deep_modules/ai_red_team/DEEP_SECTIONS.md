# Secciones de profundización — Red team de IA

## Modelo de amenazas
Mapear aplicación, modelo, prompts de sistema/desarrollador, herramientas, conectores, RAG, corpus, memoria, filtros, logs y usuarios. Amenazas: prompt injection directa/indirecta, exfiltración, abuso de herramientas, escalada entre tenants, poisoning, extracción, jailbreak y DoS. Tratar contenido recuperado y outputs externos como datos no confiables, no instrucciones privilegiadas.

## Detección
Instrumentar origen de contexto, retrieval, decisión de política, invocación de herramienta, permisos, argumentos, salida y consumo. Detectar instrucciones indirectas, intentos de acceso cruzado, llamadas fuera de allowlist, volumen anómalo y cambios de corpus. No confiar solo en clasificadores de prompt; combinar autorización determinista y auditoría.

## Respuesta a incidentes
Deshabilitar herramienta o conector, revocar credenciales, aislar documento/corpus comprometido, preservar trazas y evaluar datos expuestos. Rotar secretos, reconstruir índice desde fuente verificada y revisar memoria/cachés. Reactivar solo tras pruebas adversariales y revisión de permisos; no considerar una negativa textual del modelo como control suficiente.

## Casos prácticos
Documento malicioso en RAG pide al agente leer un secreto sintético y enviarlo a una herramienta. Verificar que el agente no obedece instrucciones del documento, que la herramienta aplica permisos independientes y que las citas conservan procedencia. Repetir con intento de lectura de otro tenant y con conector de solo lectura.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para OWASP Top 10 for LLM Applications, NIST AI RMF, MITRE ATLAS y documentación de proveedor. Fijar modelo, versión, herramientas y corpus.


## Arquitectura de enforcement y separación de autoridad
El modelo produce propuestas; el servidor decide si la operación está permitida. El principal procede de una sesión autenticada y no de argumentos del modelo. El broker debe comprobar usuario, tenant, recurso, acción, finalidad, estado y aprobación en cada llamada. Los permisos deben limitar función, recurso, duración y volumen. Las herramientas de solo lectura también requieren ACL por objeto y tenant.

## Procedencia y propagación de contexto
Cada fragmento recuperado debe conservar origen, tenant, hash, versión, etiqueta de integridad, ACL y fecha. La procedencia debe sobrevivir chunking, resumen, memoria, caché y salida de herramienta. Si un resumen pierde la etiqueta de origen, el sistema no puede asumir que el contenido es confiable. La invalidación debe abarcar embeddings, caches, memoria y resúmenes derivados.

## Diseño de pruebas adversariales
Definir caso, precondición, fixture, acción, efecto esperado, telemetría, criterio de fallo y limpieza. Probar rutas completas (entrada→contexto→decisión→herramienta→efecto), no solo la respuesta del modelo. Incluir negativos, controles benignos, regresión y repetición con versiones fijadas.

## Métricas y validez
Separar attack success rate, unauthorized action rate, leakage rate, cross-tenant leakage, invalid-output acceptance, false refusal, utilidad, latencia y coste. Publicar denominadores por clase, severidad y configuración. No agregar fallos críticos a un promedio que los oculte. Informar muestra, intervalos, exclusiones y contaminación del dataset.

## Contención y recuperación
La respuesta debe poder revocar identidad y tokens, deshabilitar herramientas, aislar documentos/índices, invalidar memoria derivada, bloquear egress, preservar trazas y reconstruir desde fuentes verificadas. La reactivación exige pruebas de regresión y revisión de permisos; una respuesta textual segura no demuestra que el estado interno esté limpio.
