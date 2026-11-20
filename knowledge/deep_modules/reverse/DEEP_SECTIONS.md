# Secciones de profundización — Ingeniería inversa

## Modelo de amenazas
Definir autorización, origen y objetivo del binario/firmware; considerar malware, software propietario, componentes vulnerables y artefactos de cadena de suministro. Amenazas al laboratorio: ejecución accidental, escape de sandbox, egress, contaminación de muestras y exposición de secretos. Registrar arquitectura, formato, compilador cuando se conozca, empaquetado y límites legales.

## Detección
Correlacionar indicadores estáticos (imports, strings, secciones, entropía, firmas) y dinámicos (syscalls, procesos, memoria, archivos, red). Detectar anti-debugging, anti-VM, inyección y cambios de comportamiento entre entornos. Mantener reglas y firmas con corpus benigno y muestras etiquetadas; medir cobertura y falsos positivos.

## Respuesta a incidentes
Preservar binario original, hashes, metadatos y entorno; trabajar sobre copias. Si la ingeniería inversa identifica vulnerabilidad o implante, coordinar divulgación, aislar artefacto y buscar componentes relacionados en inventario. No distribuir muestras ejecutables ni publicar secretos; registrar conclusiones reproducibles y nivel de confianza.

## Casos prácticos
Analizar un ejecutable de laboratorio compilado desde código conocido: identificar funciones de autenticación, flujo de datos y llamadas de red; comparar símbolos y desensamblado; instrumentar ejecución controlada y validar hipótesis con pruebas unitarias. Repetir con optimización y símbolos eliminados para documentar límites de inferencia.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para Ghidra, LLVM, documentación de formatos PE/ELF, MITRE ATT&CK y guías de análisis. Registrar versión de herramientas y arquitectura.
