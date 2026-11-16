# Ingeniería de privacidad — Guía de dominio

**ID:** `privacy_engineering` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito
Integra privacidad en arquitectura, datos, producto, IA y operación. La protección no se limita a cifrar: incluye finalidad, minimización, transparencia, derechos, retención, compartición, inferencias y riesgo de reidentificación. Las obligaciones concretas dependen de jurisdicción y contexto.

## Modelo de datos
Inventariar datos personales, sensibles, telemetría, identificadores, inferencias, fuentes, destinatarios, transferencias, sistemas y subprocesadores. Mapear ciclo de vida: captura, uso, almacenamiento, acceso, compartición, retención, borrado y backup. Identificar sujetos, finalidades y base legal con asesoría competente.

## Competencias
- Crear data maps, registros de tratamiento y DPIA/PIA.
- Aplicar privacy by design/default y minimización.
- Diseñar consentimiento y preferencias cuando sean aplicables.
- Evaluar anonimización, seudonimización y reidentificación.
- Implementar derechos de acceso, rectificación, supresión y portabilidad.
- Controlar transferencias, proveedores y subprocesadores.
- Medir privacidad en telemetría, analytics y sistemas de IA.
- Gestionar incidentes de datos y retención.

## Controles
- Recoger solo datos necesarios y definir finalidad explícita.
- Separar identificadores de datos de actividad.
- Cifrar datos y restringir accesos con RBAC/ABAC.
- Redactar logs, prompts y evidencias.
- Aplicar retención automática y borrado verificable.
- Evitar datos personales en ambientes de prueba.
- Evaluar reidentificación y linkage attacks antes de publicar datasets.
- Registrar transferencias y cambios de finalidad.
- Diseñar mecanismos para solicitudes de titulares y auditoría.

## Metodología
1. Definir producto, jurisdicción, responsables y finalidades.
2. Inventariar flujos y categorías de datos.
3. Identificar riesgos a personas y derechos, no solo a sistemas.
4. Evaluar necesidad, proporcionalidad y alternativas.
5. Definir medidas técnicas, organizativas y retención.
6. Validar controles con datos sintéticos.
7. Probar solicitudes de titulares y borrado.
8. Revisar proveedores y transferencias.
9. Reevaluar ante cambios de finalidad, modelo o población.

## Laboratorio
Aplicación ficticia con eventos de telemetría. Implementar minimización, seudonimización, retención y borrado; probar reidentificación sobre datos sintéticos y documentar riesgo residual.

## Evaluación
Cada flujo tiene finalidad, base de tratamiento revisada, propietario, retención, acceso y mecanismo de derechos; las pruebas no usan PII real.

## Referencias
NIST Privacy Framework, ISO/IEC 27701, ISO/IEC 29100, GDPR cuando aplique, leyes locales aplicables y OWASP Privacy Risks.

## Instrucciones IA
No solicites datos personales reales si un ejemplo sintético basta. No declares cumplimiento legal. Diferencia privacidad, seguridad y anonimización; indica riesgos de inferencia y reidentificación.