# Red Team autorizado — Guía de dominio

**ID:** `red_team` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y límites
Evalúa de forma controlada la capacidad de prevenir, detectar y responder ante escenarios adversarios. El Red Team requiere autorización escrita, reglas de enfrentamiento, activos, ventanas, límites, canales de emergencia y plan de parada. No es una autorización genérica para atacar Internet o terceros.

## Competencias
- Planificar objetivos de emulación y criterios de éxito.
- Mapear TTP a MITRE ATT&CK y controles defensivos.
- Realizar reconocimiento y validación dentro del scope.
- Evaluar rutas de identidad, configuración, aplicaciones y cloud.
- Diseñar simulaciones de phishing solo con autorización específica.
- Coordinar Purple Team y medir detección/respuesta.
- Producir evidencia mínima y recomendaciones priorizadas.

## Controles de operación
- Rules of Engagement firmadas y lista de exclusiones.
- Cuentas, infraestructura y datos de prueba dedicados.
- Límites de tasa, impacto, persistencia y acceso.
- No DoS, ransomware, exfiltración real ni movimiento fuera del scope.
- Kill switch y contacto de emergencia.
- Registro de acciones, operador, herramienta, tiempo y resultado.
- Revisión legal/privacidad y coordinación con SOC.

## Metodología
1. Acordar objetivos, autorización, scope y stop conditions.
2. Construir hipótesis de amenaza y plan de emulación.
3. Validar alcance y controles antes de iniciar.
4. Ejecutar pruebas de mínimo impacto y detener al obtener evidencia.
5. Notificar hallazgos críticos según protocolo.
6. Correlacionar acciones con telemetría defensiva.
7. Realizar debrief con Blue Team y responsables.
8. Documentar rutas, evidencias y brechas.
9. Retestar controles y cerrar con lecciones.

## Laboratorio
Entorno AD/cloud/web desechable con usuarios sintéticos. Emular TTP benignas y verificar detecciones sin payload destructivo ni persistencia real.

## Evaluación
Autorización vigente, scope respetado, impacto controlado, trazabilidad completa, hallazgos reproducibles y mejora defensiva medida.

## Referencias
MITRE ATT&CK, PTES, NIST SP 800-115, CREST, OWASP Testing Guide y CISA Red Team guidance.

## Instrucciones para agentes IA
No asumas autorización. No generes payloads destructivos, persistencia, evasión ni robo de credenciales. Si scope o stop conditions faltan, limita el trabajo a planificación defensiva.

## Arquitectura
La operación se gobierna mediante patrocinador, reglas de engagement, equipo, infraestructura de pruebas, identidades/cuentas, objetivos autorizados, canal de mando, observadores defensivos y sistema de evidencias. Separar infraestructura de simulación de activos productivos; definir rutas de escalado, kill switch, límites de impacto y ventanas. Cada técnica se vincula a objetivo de control, precondición, autorización, señal detectable y evidencia; el resultado debe poder correlacionarse con telemetría defensiva sin convertir la operación en acceso persistente.
