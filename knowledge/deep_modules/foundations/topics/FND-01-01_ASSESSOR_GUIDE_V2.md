# Guía reservada del evaluador — FND-01.01 — V2

**Clasificación:** material exclusivo de evaluadores; no entregar al candidato antes ni durante la prueba.  
**Instrumento asociado:** `FND-01-01_COLD_ASSESSMENT_V2.md`.  
**Estado:** guía de calibración preparada; no administrada ni validada externamente.

## 1. Propósito y límites

Esta guía reduce la variabilidad de la calificación. No es una clave literal ni exige que el candidato reproduzca una arquitectura única. Debe premiarse el razonamiento contextual, la explicitación de supuestos, la evidencia, la identificación de límites y la capacidad de cambiar de decisión ante nuevos datos.

No debe usarse para inferir T4. La prueba evalúa una unidad y una muestra de tareas. Una calificación alta no sustituye revisión bibliográfica, evaluación curricular de las 102 subunidades ni revisión disciplinar independiente.

## 2. Evidencia mínima esperada por bloque

### A — Enseñar (15 puntos)

Una respuesta de nivel 3 debe:
- diferenciar confidencialidad de privacidad usando un ejemplo de tratamiento lícito/esperado frente a uno excesivo o inesperado, aun con controles de acceso;
- distinguir safety (peligros/daños inaceptables, incluidos fallos accidentales) de ciberseguridad (adversidad que afecta activos, funciones y misión);
- explicar resiliencia como anticipar, resistir/continuar, recuperar y adaptar, no como mera existencia de copias;
- distinguir confiabilidad de disponibilidad mediante función, condiciones, horizonte y criterio frente a accesibilidad durante una ventana;
- definir objetivos observables, secuencia, evaluación y transferencia.

Nivel 4 exige que la microlección provoque razonamiento y transferencia: contraejemplos, dependencias, tensiones entre propiedades y evaluación de comprensión, no solo claridad expositiva.

### B — Explicar (15 puntos)

Modelo causal mínimo:
- controlador local y sensores: plano funcional local;
- pasarela remota: frontera de entrada de consignas;
- IdP, DNS y plano administrativo: dependencias distintas, potencialmente compartidas;
- logs: datos de operadores, finalidades y retención.

Debe evitar inferir que la pérdida del IdP necesariamente detiene el control local: depende de dónde se aplica autenticación/autorización, cachés, sesiones, fail-safe, permisos locales y diseño del controlador. También debe evitar inferir que la continuidad local es segura sin validar integridad de consignas, estado de sensores, firmware y transiciones.

Debe explicar por qué dos regiones no son independientes si comparten IdP, DNS, plano de administración, claves, proveedor, configuración, energía o personal privilegiado. Debe proponer evidencia: arquitectura real, dependencias, pruebas de fallo, logs, configuración, versión y estados de control.

### C — Analizar (30 puntos)

La respuesta de nivel 3 debe separar explícitamente:
1. hechos dados;
2. hipótesis plausibles;
3. datos faltantes;
4. confianza y consecuencias de estar equivocado.

Debe distinguir:
- amenaza intencional (p. ej., actualización maliciosa o credenciales abusadas);
- fallo accidental (sensor, firmware, red, reloj);
- peligro de safety (condición capaz de causar daño);
- causa común (dependencia o cambio que afecta canales redundantes).

No se premia afirmar que la actualización reciente causó la divergencia: es una hipótesis que exige correlación temporal, versiones, integridad, logs y análisis independiente. La divergencia de sensores no autoriza a elegir uno sin criterio de ingeniería validado.

Debe comparar al menos tres alternativas con efectos en misión, personas, safety, privacidad y recuperación. Debe nombrar autoridad competente y criterios de parada. No debe inventar consignas físicas ni recomendar bypass de interlocks.

### D — Diseñar (30 puntos)

Un diseño de nivel 3 debe ser verificable y contextual:
- requisitos con identificador, condición, comportamiento y criterio de aceptación;
- zonas, límites de confianza y flujos;
- estados y transiciones con guardas;
- identidad nominal y privilegio mínimo;
- órdenes autenticadas, autorizadas, íntegras, frescas y secuenciadas;
- gestión de dependencias comunes;
- minimización, finalidad, retención y acceso a logs;
- recuperación de identidad, claves, configuración y estado;
- pruebas positivas, negativas, de fallo, rollback y evidencia;
- claims, argumentos, evidencia, supuestos y derrotadores.

Nivel 4 exige analizar trade-offs, independencia real, fallos correlacionados, incertidumbre, degradación y sensibilidad. No existe puntuación máxima por listar tecnologías o citar normas.

### E — Integrar y refutar (10 puntos)

Debe poder señalar una decisión propia que pueda resultar falsa. La evidencia refutadora debe ser observable y capaz de cambiar la arquitectura o la aceptación de riesgo. “Haría más pruebas” no basta: especificar qué prueba, qué resultado, bajo qué condiciones y qué decisión cambiaría.

## 3. Consideraciones específicas por variante

### Variante A — proceso de agua
- No asumir que toda planta, etapa o proceso tiene la misma criticidad o regulación.
- Distinguir agua para consumo humano de otros usos y etapas del tratamiento.
- Considerar calidad del agua, continuidad, exposición de operadores y población, integridad de medición y autoridad del responsable del proceso.
- La divergencia de sensores y la actualización reciente son señales para preservar evidencia y escalar, no una base suficiente para cambiar consignas.
- No aplicar automáticamente el Decreto 1575/2007 o la Resolución 2115/2007 sin confirmar ámbito material y actividad.

### Variante B — cadena de frío farmacéutica
- Diferenciar disponibilidad del sistema, integridad de mediciones, trazabilidad de lotes y aptitud del producto.
- No inventar umbrales de temperatura: identificar especificación validada, fabricante, calidad/regulatorio y responsable competente.
- Considerar cadena de custodia de datos, calibración, ubicación de sensores, reloj, firmware, excursiones y decisión de cuarentena/liberación por autoridad competente.
- Una cuenta de servicio común puede crear causa común y debilitar atribución.

### Variante C — infraestructura de edificios
- Separar seguridad física, HVAC, ocupación, privacidad y continuidad.
- Patrones de presencia pueden ser datos personales incluso si no contienen nombre visible; analizar reidentificación y contexto.
- No asumir que HVAC y control de acceso comparten criticidad ni que el modo local es seguro sin analizar interacciones.
- El plano compartido del integrador requiere límites, autorización, supervisión y salida del proveedor.

## 4. Rúbrica operacional de puntuación

Para cada bloque, asignar nivel entero 0–4 y documentar evidencia concreta:
- **0:** ausencia o error fundamental.
- **1:** términos/controles nominales sin razonamiento causal.
- **2:** solución parcial; omite dependencias, incertidumbre o validación.
- **3:** respuesta correcta, contextual, verificable y con límites.
- **4:** razonamiento experto para esta tarea, con alternativas, sensibilidad, contraejemplos y evidencia refutadora.

Conversión: puntos = nivel / 4 × peso del bloque. Pesos: 15, 15, 30, 30 y 10. Total exacto: 100. No redondear cada bloque; redondear solo el total a una cifra decimal.

Umbral: total ≥80, todos los bloques ≥3, cero fallas críticas y doble calificación. Registrar por separado los niveles y los puntos. No convertir la puntuación en T4.

## 5. Fallas críticas: interpretación y evidencia

Una falla crítica solo se marca cuando aparece en la respuesta original y se cita el fragmento o razonamiento que la demuestra. No inferir una falla por omisión ambigua sin pedir aclaración dentro de las reglas de administración.

| ID | Falla | Evidencia que la activa |
|---|---|---|
| CF-01 | Privacidad = cifrado/confidencialidad | afirma que el cifrado elimina por sí solo riesgo de privacidad |
| CF-02 | Safety = ciberseguridad | excluye fallos accidentales/peligros o los trata como amenazas informáticas únicamente |
| CF-03 | Backup = resiliencia | declara resiliencia por existencia de copias sin restauración/estado confiable/función |
| CF-04 | Independencia no demostrada | asume independencia pese a dependencia común identificada |
| CF-05 | Bypass inseguro | recomienda desactivar interlocks/controles sin autoridad ni análisis de peligros |
| CF-06 | Consigna física inventada | prescribe dosis, temperatura, velocidad, presión o setpoint no proporcionado/validado |
| CF-07 | Plan = ejecución | presenta protocolo como prueba ya ejecutada |
| CF-08 | Ausencia de incidentes = seguridad | usa ausencia de eventos reportados como demostración suficiente |
| CF-09 | Daño individual ignorado | descarta impactos de datos personales por no existir brecha de seguridad |
| CF-10 | Incertidumbre ocultada | presenta inferencias o hipótesis como hechos conocidos |

## 6. Proceso de doble evaluación y adjudicación

1. Verificar versión y hash del instrumento; asignar variante aleatoria y tiempo.
2. Mantener separado el material del candidato y el paquete reservado del evaluador.
3. Dos evaluadores cualificados, sin conflicto material y sin participación en la autoría, califican de forma independiente.
4. Cada evaluador registra nivel, puntos, fragmento probatorio y justificación por bloque.
5. Si difieren más de un nivel en cualquier bloque o más de 10 puntos en total, un tercer evaluador adjudica con evidencia.
6. Conservar respuestas originales, hojas individuales, conflictos, adjudicación y limitaciones con seudónimo.
7. Si falla, convertir cada discrepancia en acción correctiva; usar una variante distinta tras intervalo suficiente.

## 7. Plantilla de hoja individual

| Campo | Registro |
|---|---|
| Instrumento, versión y SHA-256 | |
| Variante y duración | |
| Evaluador y cualificación | |
| Conflicto de interés declarado | |
| Bloque A: nivel / puntos / evidencia | |
| Bloque B: nivel / puntos / evidencia | |
| Bloque C: nivel / puntos / evidencia | |
| Bloque D: nivel / puntos / evidencia | |
| Bloque E: nivel / puntos / evidencia | |
| Fallas críticas: ID y cita literal | |
| Total / decisión | |
| Límites y acciones correctivas | |

## 8. Estado y gate

La guía mejora la reproducibilidad de la corrección, pero no es validación psicométrica. Antes de usarla para una decisión de alto impacto se requiere pilotaje, revisión del contenido por especialistas, análisis de acuerdo interevaluador y ajuste de dificultad/tiempo. La auditoría permanece abierta hasta que se administre una evaluación válida con dos evaluadores independientes cualificados y se documenten respuestas y adjudicación.
