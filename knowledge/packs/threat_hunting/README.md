# Threat hunting — Paquete especializado

**ID:** `threat_hunting` · **Versión:** 1.1.0 · **Idioma:** español · **Estado:** contenido editorial propio, offline.

## Propósito y límites
Hunting basado en hipótesis, análisis de comportamiento, telemetría y consultas reproducibles.

Este módulo ofrece orientación y ejercicios sintéticos. No implica que CYBER_AI disponga de una plataforma especializada instalada ni concede permisos. Toda actividad activa requiere propietario, autorización, alcance, ventana y plan de parada.

## Competencias específicas
- Comprender arquitectura, actores, protocolos, flujos y límites de confianza.
- Inventariar activos, superficies, dependencias y datos sensibles.
- Mapear amenazas, debilidades y controles preventivos, detectivos y correctivos.
- Definir telemetría y evidencia adecuada al contexto.
- Evaluar disponibilidad, seguridad, privacidad y efectos operativos.
- Convertir hallazgos en mitigaciones, pruebas de regresión y riesgo residual.

## Amenazas y fallos prioritarios
Sesgo de confirmación, datos incompletos, hipótesis no falsables y confusión entre anomalía y ataque.

## Metodología
1. Documentar propietario, criticidad, contexto y autorización.
2. Crear diagrama de arquitectura, inventario y flujos de datos.
3. Definir escenarios de amenaza y criterios de éxito/fracaso.
4. Revisar configuración y evidencia de solo lectura primero.
5. Elegir pruebas con el mínimo impacto posible.
6. Validar resultados mediante segunda fuente o revisión independiente.
7. Priorizar impacto real, exposición, probabilidad e incertidumbre.
8. Recomendar controles con responsable, plazo y prueba de cierre.
9. Preservar evidencias y documentar limitaciones.

## Laboratorio de referencia
Definir hipótesis ATT&CK, consultar dataset sintético y registrar hallazgos, falsos positivos e hipótesis descartadas.

## Criterios de evaluación
- Identifica activos, flujos y límites de confianza.
- Distingue evidencia de inferencia y registra incertidumbre.
- Reconoce riesgos del dominio y controles.
- Completa el ejercicio sin salir del alcance autorizado.
- Produce informe reproducible con evidencias, hashes y retest.

## Referencias externas
Las fuentes específicas están en `data/knowledge_sources/knowledge_catalog.json`. Siguen pendientes de validación de licencia y procedencia; no son corpus descargado ni ingerido.

## Instrucciones para agentes IA
Consulta este módulo y Skills verificadas pertinentes. No inventes cobertura ni ejecuciones. Prefiere análisis pasivo, datos sintéticos y laboratorios. Si la acción puede afectar personas, disponibilidad, privacidad o activos físicos, detente y exige autorización explícita.