# Foundations — ingeniería del riesgo y assurance V1

**ID:** `foundations` · **Versión:** 1.0.0 · **Estado:** desarrollo técnico específico; no aprobado como experto.  
**Alcance:** FND-04.01–FND-04.12 del currículo. Complementa, no reemplaza, el compendio general de Foundations.

## 1. Objetivos y frontera

Al terminar este bloque, el estudiante debe poder construir un argumento de riesgo reproducible: delimitar el sistema y la misión, formular escenarios de pérdida, identificar actores y causas, estimar incertidumbre, evaluar controles, comparar tratamientos y explicar el riesgo residual a quien tiene autoridad para aceptarlo.

No se pretende convertir riesgo en una cifra universal. El resultado depende de contexto, horizonte, datos, supuestos y tolerancia de la organización. Una matriz 5×5 no convierte categorías ordinales en probabilidades ni elimina incertidumbre.

Distinguir:

- **Amenaza:** circunstancia o actor con capacidad de causar daño.
- **Evento:** ocurrencia observable o hipotética dentro de un escenario.
- **Vulnerabilidad:** debilidad que puede contribuir a un evento.
- **Exposición:** condición que permite que una amenaza alcance el activo.
- **Consecuencia/impacto:** efecto sobre misión, personas, datos, operación, obligaciones o terceros.
- **Riesgo:** combinación contextual de posibilidad e impacto de escenarios, considerando controles e incertidumbre.
- **Control:** medida que modifica probabilidad, impacto, detectabilidad o recuperación.
- **Riesgo residual:** riesgo que permanece tras controles y tratamiento, no el riesgo que queda después de restar una puntuación.

## 2. Modelo de escenario de pérdida

Representar un escenario como:

`S = (M, A, X, P, E, C, K, U)`

Donde M es misión/objetivo; A activo o servicio; X actor o causa; P precondiciones; E secuencia de eventos; C consecuencias; K controles y su estado; U incertidumbre y supuestos.

Una descripción útil es falsable y contiene:
1. activo y propietario del riesgo;
2. objetivo que puede perderse;
3. actor/capacidad o causa accidental;
4. acceso inicial y precondiciones;
5. ruta técnica/organizativa/física;
6. evento iniciador y controles que deberían interrumpirlo;
7. consecuencia y población afectada;
8. evidencia disponible y lagunas;
9. horizonte temporal;
10. condición de revisión o retirada del escenario.

**Contraejemplo:** “un atacante puede comprometer la empresa” no es un escenario evaluable. “Una credencial de automatización con permiso de escritura en el repositorio de despliegue es reutilizada desde un runner persistente; el cambio no requiere segunda aprobación y puede publicar una imagen alterada” sí permite identificar precondiciones, controles, telemetría y pruebas.

## 3. Estimación: cuantitativa, ordinal y mixta

### 3.1 Cuantificación condicionada

Si se dispone de escenarios mutuamente excluyentes y suficientemente caracterizados, la pérdida esperada puede expresarse como:

`E[L] = \sum_i P(S_i \mid contexto, controles) \times L_i`

La expresión no autoriza a inventar probabilidades. Si los escenarios se solapan, faltan categorías o las dependencias no se conocen, la suma puede contar dos veces o subestimar pérdidas. Documentar el árbol de eventos y las dependencias.

Para eventos recurrentes, una aproximación de pérdida anual esperada puede ser:

`ALE = frecuencia anual estimada × magnitud media condicionada`

Solo es defendible si la frecuencia, la distribución de magnitudes, el periodo y los supuestos están declarados. No ocultar colas, pérdidas correlacionadas, eventos extremos ni cambios de régimen detrás de una media.

### 3.2 Escalas ordinales

Una escala cualitativa (p. ej. raro/posible/probable y moderado/alto/crítico) sirve para facilitar conversación y priorización. No debe multiplicarse como si “4×5” fuese una cantidad física. La categoría debe tener criterios observables, horizonte y reglas de calibración. Si dos escenarios caen en la misma celda, eso no demuestra equivalencia.

### 3.3 Incertidumbre

Separar:
- **Aleatoria:** variabilidad inherente del proceso.
- **Epistémica:** falta de conocimiento, cobertura o datos.
- **De modelo:** simplificaciones o supuestos estructurales.
- **De medición:** sensores, muestreo, atribución y calidad del registro.
- **De juicio:** desacuerdo entre evaluadores y sesgo de disponibilidad.

Registrar rango, confianza, fuente, sensibilidad y qué dato cambiaría la decisión. “No sabemos” es un resultado válido; no sustituirlo por un decimal inventado.

### 3.4 CVSS y severidad técnica

CVSS describe severidad técnica de vulnerabilidades bajo su metodología y versión; no es por sí solo riesgo de negocio, probabilidad de explotación en una organización, prioridad de parche ni impacto operacional. Complementar con exposición real, explotación observada, criticidad del activo, controles compensatorios, dependencias, ventana de exposición y consecuencia.

## 4. Análisis de controles y assurance

Un control solo reduce riesgo si está diseñado, desplegado, operado y medido dentro del alcance relevante. Distinguir:
- **Diseño:** ¿el control aborda el escenario y sus precondiciones?
- **Implementación:** ¿está presente en todos los componentes aplicables?
- **Operación:** ¿funcionó en el periodo y bajo las condiciones evaluadas?
- **Cobertura:** ¿qué activos, identidades, rutas y excepciones incluye?
- **Independencia:** ¿comparte causa común, credencial, proveedor, plano de control o punto de fallo?
- **Evidencia:** ¿el artefacto es íntegro, reciente, atribuible y suficiente?
- **Efecto adverso:** ¿afecta disponibilidad, privacidad, seguridad física o recuperación?

Ejemplo: “MFA habilitado” no demuestra que las cuentas de servicio, tokens de larga duración, recuperación, sesiones existentes y cuentas break-glass estén protegidas. “EDR instalado” no demuestra que todos los endpoints reporten, que la política esté activa, que el sensor no esté degradado ni que una alerta se atienda.

### 4.1 Matriz mínima de trazabilidad

| Escenario | Control | Propiedad | Prueba | Evidencia | Limitación |
|---|---|---|---|---|---|
| Token de CI reutilizado | identidad de workload efímera y scope mínimo | autoridad/integridad | intentar acceso desde principal no autorizado | decisión del PEP, claims, audit log | no cubre proveedor comprometido |
| Cambio de artefacto | firma y verificación de provenance | integridad | alterar artefacto después de firma | hashes y resultado de verificación | firma válida no prueba que el build sea benigno |
| Exfiltración por API | autorización por objeto y rate limits | confidencialidad | consultar recurso de otro principal | respuesta denegada y log correlacionado | no cubre canal lateral no instrumentado |

## 5. Tratamiento y aceptación

Las opciones típicas son evitar, reducir, compartir/transferir o aceptar el riesgo. Transferir contrato o seguro no elimina el daño técnico ni la responsabilidad de supervisión. La aceptación debe indicar quién tiene autoridad, alcance, vigencia, condiciones, evidencia revisada, excepciones y fecha de reevaluación.

No aceptar un riesgo por silencio, porque el control “existe”, porque la puntuación bajó o porque un modelo generó una recomendación. Los escenarios de seguridad de personas, privacidad, obligaciones regulatorias o impacto a terceros pueden requerir autoridad y revisión especial.

## 6. Ejemplo resuelto — cuenta de servicio de despliegue

**Contexto hipotético:** un equipo usa un runner de CI para publicar imágenes en un registro privado. La identidad del runner puede escribir en el repositorio de producción. El entorno de laboratorio usa repositorio y secretos sintéticos.

**Escenario:** un cambio no autorizado en pipeline o dependencia obtiene el contexto de la cuenta de servicio y publica una imagen alterada que después despliega el proceso de entrega.

**Supuestos que deben validarse:** el runner tiene acceso al secreto; la credencial sobrevive más allá de un job; el registro acepta el principal; la aprobación del despliegue no verifica digest/provenance. Si un supuesto no se confirma, se revisa la ruta.

**Controles a evaluar:** runner efímero; identidad federada de corta duración; permisos por repositorio/ambiente; separación entre build y deploy; aprobación independiente; pinning por digest; firma y verificación de artefactos; registro de auditoría; rollback probado.

**Pruebas negativas:**
1. Un job de un repositorio no autorizado intenta obtener identidad de producción: debe denegarse.
2. Un token expirado o con audiencia incorrecta intenta publicar: debe denegarse.
3. Un artefacto cuyo digest no coincide con el manifiesto aprobado intenta desplegarse: debe bloquearse.
4. Un aprobador que también modificó el pipeline intenta aprobar su propio cambio: debe activarse la regla de separación de funciones, si la política la exige.
5. Un runner reutilizado intenta leer el entorno del job anterior: no debe encontrar secretos ni estado residual.

**Evidencia:** manifiestos de permisos, claims del token sintético, logs del punto de enforcement, hashes de artefacto, decisión de aprobación, salida de pruebas y configuración versionada. La evidencia se etiqueta con commit, entorno y fecha.

**Conclusión admisible:** solo se puede afirmar que las pruebas definidas fueron bloqueadas en el harness concreto. No se puede concluir que toda la cadena de suministro esté segura, que el proveedor sea invulnerable o que la probabilidad de compromiso sea cero.

## 7. Diseño de evaluación y sensibilidad

Para cada estimación registrar:
- unidad de análisis y denominador;
- población/activos incluidos y excluidos;
- periodo de observación;
- fuente de frecuencia e impacto;
- tratamiento de incidentes no observados;
- controles realmente verificados;
- rango y confianza;
- dependencias y escenarios correlacionados;
- umbral de decisión y propietario.

Realizar sensibilidad: variar un supuesto a la vez y luego escenarios combinados plausibles. Si la decisión cambia con una pequeña variación, señalar fragilidad y priorizar obtener datos. No presentar análisis Monte Carlo sin distribuciones justificadas, dependencia modelada y semilla/protocolo reproducibles.

## 8. Artefactos exigibles

1. Diagrama de contexto y fronteras de confianza.
2. Inventario con propietario, criticidad, dependencias y frescura.
3. Registro de escenarios con precondiciones y consecuencias.
4. Registro de supuestos, fuentes y nivel de confianza.
5. Método de estimación y justificación de escalas.
6. Matriz control→prueba→evidencia→limitación.
7. Decisión de tratamiento/aceptación con autoridad.
8. Plan de monitorización y disparadores de reevaluación.
9. Resultados de pruebas, hashes, versiones y rollback.
10. Revisión independiente y desacuerdos documentados.

## 9. Preguntas de examen en frío

- ¿Por qué una matriz ordinal no permite inferir una probabilidad cardinal?
- ¿Qué condición hace inválida la suma de pérdidas esperadas de varios escenarios?
- ¿Cómo cambia la estimación si dos controles dependen de la misma identidad o proveedor?
- ¿Por qué CVSS alto no implica automáticamente máxima prioridad de negocio?
- ¿Qué evidencia distingue control diseñado, implementado y operado?
- ¿Cuándo una aceptación de riesgo es inválida por falta de autoridad o alcance?
- Construya un escenario de pérdida y proponga una prueba que pueda refutarlo.

## 10. Fuentes y límites

Referencias primarias para consulta y contraste:
- NIST SP 800-30 Rev. 1, *Guide for Conducting Risk Assessments*: https://doi.org/10.6028/NIST.SP.800-30r1
- NIST Cybersecurity Framework 2.0: https://doi.org/10.6028/NIST.CSWP.29
- NIST SP 800-53 Rev. 5, *Security and Privacy Controls for Information Systems and Organizations*: https://doi.org/10.6028/NIST.SP.800-53r5
- FIRST Common Vulnerability Scoring System (CVSS): https://www.first.org/cvss/

**Estado de fuentes:** referencias registradas; no se declara lectura integral en esta entrega. Deben anotarse edición, erratas, localizador exacto, licencia y extractos antes de respaldar claims individuales.  
**Estado de laboratorio:** el ejemplo es un protocolo propuesto para un harness sintético; no se declara ejecutado por esta documentación.


## 11. Ejemplo cuantitativo reproducible — pérdida anual esperada

El runner `labs/risk_engineering.py` implementa un ejemplo sintético para el escenario de publicación no autorizada de un artefacto de producción. Ejecutar desde la raíz:

```bash
python3 knowledge/deep_modules/foundations/labs/risk_engineering.py
python3 -m unittest tests.test_foundations_risk_lab -v
```

**Supuestos hipotéticos, no observaciones de CYBER_AI ni de una empresa real:**

- Frecuencia basal: 0,40 eventos/año.
- Pérdida condicional media por evento: USD 120.000.
- Frecuencia residual estimada tras controles: 0,15 eventos/año.
- Pérdida condicional residual: USD 80.000.
- Coste anual de controles: USD 15.000.

[
EAL_{base}=0,40\times 120.000=USD\ 48.000/año
]

[
EAL_{residual}=0,15\times 80.000=USD\ 12.000/año
]

[
Pérdida\ evitada=48.000-12.000=USD\ 36.000/año
]

[
Beneficio\ neto\ modelado=36.000-15.000=USD\ 21.000/año
]

El coste anual de equilibrio es USD 36.000 bajo estos supuestos. No significa que el control deba comprarse automáticamente: faltan incertidumbre estadística, distribución de pérdidas, colas, correlaciones, efectos secundarios, coste de implementación, coste de oportunidad y apetito/autoridad de riesgo.

**Sensibilidad:** se conserva la eficacia relativa asumida para los controles (frecuencia residual = 37,5 % de la basal; impacto residual = 66,7 % de la basal).

| Escenario | EAL basal | EAL residual | Pérdida evitada | Neto tras USD 15.000 |
|---|---:|---:|---:|---:|
| Bajo: 0,20 × USD 80.000 | USD 16.000 | USD 4.000 | USD 12.000 | -USD 3.000 |
| Base: 0,40 × USD 120.000 | USD 48.000 | USD 12.000 | USD 36.000 | USD 21.000 |
| Alto: 0,60 × USD 160.000 | USD 96.000 | USD 24.000 | USD 72.000 | USD 57.000 |

La decisión económica cambia en el escenario bajo: el beneficio modelado no cubre el coste. Esto muestra por qué no se debe publicar una cifra puntual sin rango ni declarar que el tratamiento es rentable con evidencia débil.

**Límites de inferencia:** la multiplicación frecuencia × pérdida condicional solo es interpretable para el mismo escenario, población y horizonte. No sumar escenarios solapados como si fueran mutuamente excluyentes. Las cifras de eficacia son supuestos y deben sustituirse por evidencia local, con intervalos y procedencia. El runner prueba aritmética y sensibilidad; no valida los supuestos ni la eficacia de controles reales.
