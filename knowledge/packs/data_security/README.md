# Seguridad de datos — Paquete base

**ID:** `data_security` · **Versión:** 1.0.0 · **Idioma:** español · **Estado:** contenido propio inicial, incluido offline.

## Propósito y límites
Seguridad de datos: Seguridad de datos y su arquitectura, amenazas, controles, metodología y validación. Esta guía es base metodológica, no certificación ni enciclopedia. No concede permisos. Toda actividad activa requiere autorización explícita, alcance, ventana y criterios de parada.

## Competencias
- Explicar arquitectura, componentes, flujos y límites de confianza.
- Identificar activos, amenazas, vulnerabilidades, controles e impactos.
- Diseñar prevención, detección, respuesta, recuperación y validación.
- Seleccionar herramientas por riesgo, evidencia, coste y mantenimiento.
- Documentar procedencia, versiones, incertidumbre y reproducibilidad.

## Metodología reproducible
1. Definir propietario, autorización, alcance y exclusiones.
2. Inventariar activos, datos, dependencias y límites de confianza.
3. Formular hipótesis, amenazas, controles y criterios de parada.
4. Recopilar evidencia permitida con procedencia, fecha y hash.
5. Elegir métodos de menor riesgo y registrar versiones/configuración.
6. Comenzar en modo pasivo/local; pruebas activas solo con autorización explícita.
7. Validar hallazgos de forma reproducible e independiente.
8. Priorizar impacto, exposición, explotabilidad e incertidumbre.
9. Recomendar controles verificables y retest.
10. Registrar evidencias, limitaciones y riesgo residual.

## Controles mínimos
- Mínimo privilegio y separación análisis/ejecución.
- Versiones exactas de herramientas, reglas, modelos y datasets.
- Secretos fuera de código, prompts y logs; redacción antes de IA remota.
- No confiar en una herramienta o modelo como prueba concluyente.
- Preservar originales y registrar SHA-256.
- Revisión humana antes de cambios o acciones activas.

## Laboratorio seguro
Usar datos sintéticos, fixtures, aplicaciones deliberadamente vulnerables o máquinas virtuales aisladas. Sin credenciales reales. Debe ser reiniciable y reproducible. No ejecutar pruebas destructivas fuera de laboratorio desechable autorizado.

## Evaluación
5 preguntas de fundamentos, 3 escenarios sintéticos, 2 ejercicios de evidencia/falsos positivos, 1 diseño de controles y 1 informe reproducible. Aprobación sugerida: ≥80%, sin errores críticos de alcance y con evidencia verificable.

## Entregables
Alcance y autorización; activos; método y versiones; evidencias con hashes; hallazgos con severidad/confianza; mitigaciones; retest y riesgo residual.

## Fuentes externas
Consultar `data/knowledge_sources/knowledge_catalog.json`. Las URLs catalogadas no implican descarga, licencia o ingestión. Verificar derechos, procedencia, versión, fecha, tamaño, hash y seguridad del extractor.

## Instrucciones para agentes IA
Lee este paquete antes de planificar tareas de esta especialidad. Reutiliza Skills verificadas con alcance coincidente. No inventes capacidades ni resultados. Si falta evidencia, dilo. No ejecutes acciones activas sin autorización. Cita fragmentos recuperados; no afirmes haber consultado contenido ausente.
