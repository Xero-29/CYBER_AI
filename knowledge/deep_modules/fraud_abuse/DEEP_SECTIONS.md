# Secciones de profundización — Fraude y abuso

## Modelo de amenazas
Modelar usuario, dispositivo, identidad, canal, comercio, transacción, motor de reglas/modelos, pagos, reembolsos y revisión humana. Amenazas: account takeover, synthetic identity, abuso de promociones, card testing, collusion, chargeback fraud, bot automation y abuso interno. Considerar adversario adaptativo y coste de falsos positivos.

## Detección
Combinar señales de dispositivo, sesión, velocidad, geografía, grafo de relaciones, historial y comportamiento transaccional. Medir precision/recall por segmento, fraude evitado, falsos positivos, latencia y drift. Evitar variables proxy discriminatorias; explicar decisiones y mantener revisión humana para casos de alto impacto.

## Respuesta a incidentes
Limitar temporalmente transacciones o cuentas sospechosas, preservar eventos y grafo, verificar identidad por canal seguro y escalar a fraude/pagos/legal. Revertir bloqueos falsos positivos con proceso de apelación. Rotar credenciales si hay account takeover y revisar reglas/modelos para evitar que el atacante se adapte.

## Casos prácticos
Dataset sintético simula card testing con múltiples intentos de bajo valor desde dispositivos relacionados. Construir baseline, detectar velocidad y grafo, ajustar umbral y medir falsos positivos. Repetir con campaña legítima de promociones para evaluar sesgo y coste de bloqueo.

## Referencias
Ver [RESEARCH_STUDY.md](RESEARCH_STUDY.md#fuentes) para FATF, PCI DSS, NIST AI RMF y literatura de detección de fraude. La normativa depende de jurisdicción y tipo de servicio financiero.
