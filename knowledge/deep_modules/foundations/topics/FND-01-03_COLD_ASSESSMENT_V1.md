# FND-01.03 — Instrumento de evaluación en frío V1

**Estado:** preparado, no administrado.  
**Tiempo sugerido:** 100–120 minutos.  
**Tipo:** teoría, modelado y diseño; sin escaneo real ni cambios en sistemas.

## Preguntas

1. Diferencie activo, recurso, sujeto, objeto, dato, proceso, servicio, misión y stakeholder.
2. Explique por qué una misma entidad puede ser sujeto y objeto según la operación.
3. Defina una frontera de sistema y explique por qué no coincide necesariamente con la frontera de red, contrato o autorización.
4. Diseñe una ontología tipada con al menos ocho tipos de nodo y diez relaciones.
5. Proponga un identificador canónico para un activo cloud efímero y explique por qué IP/hostname no bastan.
6. Diseñe un esquema de inventario que incluya owner, custodian, función, criticidad, dependencia, soporte y procedencia.
7. Explique cómo clasificar un PLC sin soporte que soporta una función crítica.
8. Describa cómo reconciliar CMDB, EDR, APIs cloud, compras, inspección física y conocimiento del operador.
9. Identifique riesgos de privacidad y seguridad de un inventario detallado.
10. Diferencie criticidad de activo y severidad de una vulnerabilidad.
11. Diseñe una métrica de cobertura/frescura y explique el problema del denominador desconocido.
12. Modele un servicio SaaS con datos, proveedor, identidad, API, backups y misión.
13. Defina un procedimiento seguro para identificar activos OT sin escaneo activo no autorizado.
14. Seleccione y compare NIST CSF 2.0, SP 800-53 5.2.0, SP 800-37 Rev. 2, NISTIR 8286A Rev. 1, CISA OT Asset Inventory Guide e ISO/IEC/IEEE 15288.
15. Construya un plan de ciclo de vida para alta, cambio, revisión y retiro de activos.

## Rúbrica — 100 puntos

| Dimensión | Puntos |
|---|---:|
| Precisión conceptual y ontología | 20 |
| Frontera, arquitectura y dependencias | 20 |
| Esquema de inventario e identidad canónica | 20 |
| Criticidad, riesgo, privacidad y seguridad | 20 |
| Fuentes, trazabilidad, métricas y límites | 20 |

## Fallos críticos

- tratar IP como identificador estable;
- confundir owner con operador/custodian;
- ignorar SaaS, identidad, datos o dependencias externas;
- asignar criticidad solo por valor financiero;
- proponer escaneo activo OT sin autorización y análisis de safety;
- declarar 100 % de cobertura sin denominador defendible;
- exponer el inventario sin controles de acceso;
- usar una fuente retirada como vigente.

No asignar nivel individual sin respuestas originales, puntuación, segundo evaluador y adjudicación.
