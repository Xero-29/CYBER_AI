# Skill candidata — Inventario de activos orientado a misión

**ID:** SKILL-FND-01-03-ASSET-MISSION-INVENTORY  
**Estado:** draft_candidate_not_registered  
**Área:** Foundations / FND-01.03  
**Tipo:** metodología; no activa ni ejecutable.

## Patrón
Construir o auditar un inventario de activos y un grafo de dependencias conectado a procesos, servicios, misión y stakeholders.

## Precondiciones
- Alcance autorizado y autoridad responsable.
- Fuentes de descubrimiento permitidas y su impacto conocido.
- En OT, métodos pasivos por defecto; escaneo activo solo con aprobación, ventana y stop conditions.
- Propietarios, operadores y restricciones legales identificados.
- No modificar activos ni bloquear tráfico.

## Entradas
CMDB, APIs cloud, EDR, DNS/DHCP, IAM, compras, SBOM, inspección física, diagramas, servicios, procesos, datos, proveedores y conocimiento de operadores.

## Método
1. Definir misión, frontera, alcance y exclusiones.
2. Normalizar tipos: activo, recurso, sujeto, objeto, dato, proceso, servicio, misión y stakeholder.
3. Descubrir desde fuentes autorizadas y registrar procedencia.
4. Resolver identidades, alias, duplicados y activos efímeros.
5. Mapear relaciones owns/operates/uses/processes/stores/transmits/depends_on/supports.
6. Asignar owner/custodian/operator y función.
7. Clasificar datos, privacidad, criticidad multidimensional y soporte.
8. Detectar huérfanos, stale records, dependencias desconocidas y puntos únicos de fallo.
9. Validar con responsables técnicos y de misión.
10. Emitir inventario versionado, grafo, brechas y plan de ciclo de vida.

## Salidas
- Inventario canónico;
- grafo activo-proceso-servicio-misión-stakeholder;
- taxonomía y clasificación;
- registro de dependencias;
- métricas de cobertura, frescura, ownership y confianza;
- riesgos y brechas;
- evidencia de fuentes y límites.

## Validación
- identificadores estables;
- fuente y fecha por registro;
- ownership y lifecycle state;
- criticidad justificada por dimensiones;
- dependencias mapeadas;
- privacidad y confidencialidad del inventario;
- no se usa escaneo activo no autorizado;
- falsos positivos/negativos y cobertura incierta declarados.

## Límites y promoción
No es una CMDB certificada ni una autorización para escanear OT. No promueve cambios. Requiere dos ejecuciones verificadas, ledger, evidencia íntegra y revisión independiente conforme a docs/SKILL_PROMOTION.md.
