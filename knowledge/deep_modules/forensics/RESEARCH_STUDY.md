# Investigación técnica: Forense digital y cadena de custodia

**ID:** forensics · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Reproducción forense pendiente.

## Principios
Preservar integridad, procedencia, reproducibilidad, minimización y legalidad. Diferenciar investigación interna de procedimiento penal; consultar asesoría legal y política de privacidad antes de adquirir datos. La evidencia debe ser suficiente para responder pregunta definida, no recolectarse indiscriminadamente.

## Fuentes y volatilidad
Ordenar adquisición por volatilidad y valor probatorio: memoria/estado de procesos cuando proceda, conexiones y sesiones, logs volátiles, disco, snapshots, backups, cloud audit logs, correo, navegador, móviles, red y aplicaciones. El orden depende del caso, riesgo y autoridad. Documentar por qué se omitió una fuente.

## Adquisición e integridad
Registrar caso, activo, custodio, fecha/hora y zona, operador, herramienta/versión, método, errores, hash de origen/copia, almacenamiento, transferencias y acceso. Preservar originales, trabajar sobre copias verificadas, usar write blockers cuando aplique y mantener bitácora. Hash acredita igualdad de bytes, no autenticidad de origen ni corrección de adquisición.

## Análisis
Filesystem timelines, artefactos OS, logs, registry/plist, browser, email, memory, PCAP, cloud control plane, containers, mobile backups y application data. Normalizar timezone y clock drift. Distinguir timestamps de creación/modificación/acceso, metadatos, logs y eventos. Evitar inferir usuario humano a partir de una cuenta compartida o atribuir intención desde un artefacto aislado.

## Cloud y entornos distribuidos
Preservar snapshots, audit logs, API events, object versions, identity events, flow logs, serverless traces, container image digests y provider request IDs. Coordinar con proveedor, residencia de datos, retención, export format y legal hold. La evidencia cloud puede expirar o depender de proveedor; preservar temprano.

## Reporte
Pregunta, alcance, autorización, método, herramientas, versiones, timeline, artefactos, hashes, hallazgos, hipótesis, incertidumbre, limitaciones, anexos y cadena de custodia. Separar observación, inferencia y opinión. Reproducir hallazgos con un segundo analista.

## Laboratorios
Imagen de disco sintética, memoria de VM de prueba, PCAP sintético y logs con timestamps desfasados; comprobar hashes, adquisición duplicada, timeline y parser. Validar que las herramientas no modifican evidencia y que el reporte puede reproducirse.

## Fuentes
- NIST SP 800-86: https://doi.org/10.6028/NIST.SP.800-86
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3
- NIST SP 800-101 Rev. 1 (mobile forensics): https://doi.org/10.6028/NIST.SP.800-101r1

**Límite:** SP 800-86 es de 2006 y no es guía integral ni asesoría legal; complementar con normas actuales, jurisdicción y herramientas específicas.
