# Skill candidata — Evaluación de CIA y propiedades extendidas

**ID:** SKILL-FND-01-02-CIA-PROPERTY-ASSESSMENT  
**Estado:** draft_candidate_not_registered  
**Área:** Foundations / FND-01.02  
**Tipo:** metodología de clasificación y revisión; no ejecutable ni activa.

## Patrón de tarea
Evaluar requisitos y evidencia de confidencialidad, integridad y disponibilidad, distinguiéndolos de autenticidad, autorización, accountability, non-repudiation, provenance, freshness, privacidad, safety, confiabilidad y resiliencia.

## Precondiciones
- Objeto de información, servicio, actor, contexto y ventana temporal definidos.
- Modelo de identidad, autoridad y trust anchors descrito.
- Flujos de datos y finalidad declarados.
- Fuentes primarias y versiones identificadas.
- No usar la clasificación CIA como sustituto de un análisis de privacidad o safety.

## Entradas
Requisitos; arquitectura; datos; identidades; protocolos; controles; logs; firmas; hashes; métricas de servicio; amenazas; escenarios de uso y abuso.

## Método
1. Definir C, I y A para el objeto/servicio y actor autorizados.
2. Descomponer integridad en estructura, consistencia, frescura, procedencia y exactitud semántica.
3. Separar autenticación, autenticidad de mensaje, autorización y atestación.
4. Evaluar accountability y non-repudiation con identidad, custodia de claves, tiempo, logs y contexto.
5. Analizar privacidad por acciones de datos, finalidad, minimización, retención, inferencia y personas afectadas.
6. Analizar safety, reliability y resilience como dimensiones separadas.
7. Seleccionar controles y evidencia por propiedad.
8. Construir contraejemplos: firma válida pero software inseguro; hash válido pero dato falso; cifrado con uso secundario; uptime sin recuperación confiable.
9. Registrar supuestos, incertidumbre, limitaciones y criterios de rechazo.
10. Emitir matriz CIA/extendida con claims y evidencias pendientes.

## Salidas
- Matriz CIA y propiedades relacionadas.
- Mapa de identidad, autorización, autenticidad y confianza.
- Evidencia de integridad/procedencia/freshness.
- Análisis de privacidad y límites de logging.
- Métricas de disponibilidad, confiabilidad y resiliencia.
- Claims y brechas de assurance.

## Validación
- No afirma que una firma pruebe intención o corrección.
- No afirma que hash válido pruebe verdad.
- No afirma que ausencia de fuga pruebe privacidad.
- No afirma que disponibilidad pruebe resilience.
- No afirma que controles de seguridad prueben safety.
- Toda métrica incluye definición, horizonte y supuestos.

## Límites y promoción
No es certificación, auditoría legal ni verificación criptográfica de producción. Permanece como especificación candidata hasta que ledger, evidencia SHA-256, dos ejecuciones, revisión independiente y aprobación HMAC VERITAS cumplan docs/SKILL_PROMOTION.md.
