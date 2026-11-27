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
