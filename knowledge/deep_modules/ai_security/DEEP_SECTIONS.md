# Secciones de profundización — Seguridad de sistemas de IA

## Modelo de amenazas
Modelar datos de entrenamiento, pesos, tokenizer, runtime, prompts, herramientas, conectores, RAG, memoria, usuarios, proveedores y evaluación. Amenazas: poisoning, prompt injection, fuga de datos, extracción de modelo, abuso de herramientas, jailbreak, denegación de servicio, supply chain y evaluación contaminada. Distinguir instrucciones confiables de contenido externo no confiable.

## Detección
Registrar llamadas a herramientas, origen de documentos, permisos, decisiones de política, consumo de tokens, rechazos, retrieval scores y salidas sensibles. Detectar patrones de exfiltración, acceso fuera de alcance, instrucciones indirectas, cambios de corpus/modelo y abuso de cuota. Evitar almacenar prompts o datos personales sin finalidad y retención justificadas.

## Respuesta a incidentes
Deshabilitar temporalmente herramienta/conector afectado, revocar credenciales, aislar corpus o versión de modelo, preservar trazas y artefactos, evaluar datos expuestos y reconstruir índice/modelo desde fuentes verificadas. No confiar en una respuesta del modelo como prueba de incidente. Rotar secretos y revalidar permisos antes de reactivar.

## Casos prácticos
Crear RAG de laboratorio con documento malicioso que instruye al agente a revelar un secreto sintético. Medir si el sistema trata el documento como dato, limita herramientas y filtra salida; probar aislamiento por tenant, citas y recuperación. Repetir con poisoning del corpus y con herramienta de lectura/escritura limitada.

## Referencias
Consultar [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes-primarias) para NIST AI RMF, OWASP Top 10 for LLM Applications, MITRE ATLAS y documentación de proveedores. Registrar modelo, versión, configuración y dataset evaluado.
