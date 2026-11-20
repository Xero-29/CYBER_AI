# Skills candidatas de CYBER_AI

Esta carpeta contiene especificaciones metodológicas candidatas, no Skills activas ni ejecutables.

## Separación obligatoria

- La indexación de estos documentos permite que los agentes conozcan procedimientos propuestos.
- No aparecen en la búsqueda de Skills activas de skillbook.py.
- No se registran en la base SQLite ni se promueven por añadir el archivo.
- La activación requiere el flujo de ledger, dos ejecuciones independientes exitosas, revisión conforme por rol distinto, evidencia SHA-256 y aprobación HMAC VERITAS descritos en docs/SKILL_PROMOTION.md.
- HMAC demuestra posesión de la clave, no independencia real del revisor. Para producción se requiere aprobador separado, KMS/HSM y doble control.

## Estados

- draft_candidate_not_registered: solo especificación documental.
- candidate: propuesta derivada de ejecuciones verificadas en ledger.
- active: promoción aprobada con evidencia y firma.
- deprecated/rejected: ciclo de vida gestionado por skillbook.

No ejecutar una candidata ni afirmar que el agente la ha aprendido hasta que exista promoción verificable.
