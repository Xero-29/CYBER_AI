# Revisión de literatura inicial — Respuesta a incidentes

**Corte:** 2026-11-17  
**Madurez:** M1/M2 documental inicial; no M3/M4.  
**Alcance:** preparación, detección, análisis, contención, recuperación y mejora continua.

## Pregunta

¿Cómo medir la eficacia y seguridad de un proceso de respuesta a incidentes alineado con NIST CSF 2.0, considerando tiempos, calidad de evidencia, impacto operacional y recuperación?

## Síntesis primaria

NIST SP 800-61 Rev. 3 (abril de 2025) sustituye a Rev. 2 (2012) y sitúa la respuesta a incidentes dentro de la gestión del riesgo del CSF 2.0. No es correcto modelar IR únicamente como una secuencia aislada de «preparar, detectar, contener»: las funciones Govern, Identify y Protect ayudan a prevenir/preparar y mejorar, mientras Detect, Respond y Recover soportan descubrimiento, gestión, contención, erradicación y recuperación. El documento también advierte que sus ejemplos de equipos/productos no constituyen aval de proveedores.

**Implicación para CYBER_AI:** el orquestador debe tratar un incidente como proceso con estado, autoridad, alcance, evidencia y decisiones humanas; no como una orden libre de ejecutar herramientas. Cada acción debe conservar autorización, actor, timestamp, hash de evidencia, justificación, resultado y rollback cuando proceda.

## Fuente primaria revisada

- **NIST-SP-800-61r3:** https://doi.org/10.6028/NIST.SP.800-61r3  
  PDF oficial consultado. Se verificaron portada, fecha, autoridad y supersesión; la síntesis funcional se limita a las secciones ejecutivas consultadas. No se afirma lectura exhaustiva de 1876 líneas/páginas del documento.
- **NIST CSF 2.0:** https://doi.org/10.6028/NIST.CSWP.29  
  Referencia del marco; sus resultados no prescriben por sí solos procedimientos operativos.

## Modelo operacional

1. **Govern:** mandato, autoridad, roles, obligaciones, severidad, comunicación y riesgo aceptado.
2. **Identify:** inventario, criticidad, dependencias, telemetría y contexto del activo.
3. **Protect:** controles preventivos, preparación, backups, accesos de emergencia y ejercicios.
4. **Detect:** fuentes de telemetría, calidad de señal, correlación, triage y validación.
5. **Respond:** decisión, coordinación, contención proporcional, preservación y comunicación.
6. **Recover:** restauración verificada, monitorización reforzada, validación de integridad y retorno controlado.
7. **Mejora continua:** revisión post-incidente, acciones correctivas con propietario, fecha y prueba de eficacia.

## Hipótesis y protocolo experimental

- **H1:** un playbook con puertas explícitas de autorización y preservación reduce acciones irreversibles no justificadas respecto de una lista de pasos sin puertas.
- **H0:** no hay diferencia bajo las condiciones controladas.
- **Laboratorio:** simulación tabletop y telemetría sintética; escenarios de ransomware simulado, credencial comprometida y exfiltración ficticia; sin malware real ni red externa.
- **Comparadores:** playbook lineal frente a playbook con gates de autorización, cadena de custodia y validación de recuperación.
- **Métricas:** tiempo de detección/triage/contención/recuperación; porcentaje de evidencia con hash y metadatos; decisiones fuera de alcance; falsos positivos; tiempo de interrupción simulado; porcentaje de acciones reversibles; cumplimiento de comunicaciones.
- **Repetición:** mismos escenarios, operadores con experiencia comparable, rúbrica previa y registro de diferencias.
- **Análisis:** mediana y dispersión de tiempos, proporciones con intervalos de confianza y análisis cualitativo de errores. No inferir causalidad con muestras pequeñas.

## Requisitos de evidencia y seguridad

- Captura con fuente, reloj sincronizado, identidad del operador, método, hash y almacenamiento restringido.
- Separar evidencia original de copias de trabajo; documentar cadena de custodia.
- No borrar, aislar o reiniciar activos sin autoridad y evaluación de impacto, salvo procedimiento de emergencia aprobado.
- Las acciones automatizadas deben tener límites, precondiciones, modo simulación y mecanismo de parada.
- No inferir atribución de actor a partir de un IOC aislado.

## Brechas

- Lectura sistemática completa de NIST SP 800-61r3 y mapeo sección→control→evidencia.
- Integrar guías sectoriales y obligaciones legales por jurisdicción.
- Crear dataset sintético de incidentes y rúbrica de evaluación.
- Ejecutar tabletop con observadores independientes y reproducir resultados.
- Diseñar playbooks concretos para cloud, identidad, endpoint, OT y ransomware; no reutilizar uno genérico.

## Referencias

- Nelson et al., NIST SP 800-61 Rev. 3, abril 2025. https://doi.org/10.6028/NIST.SP.800-61r3
- NIST, Cybersecurity Framework 2.0, febrero 2024. https://doi.org/10.6028/NIST.CSWP.29
