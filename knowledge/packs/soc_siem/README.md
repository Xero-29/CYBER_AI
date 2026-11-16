# SOC, SIEM y SOAR — Guía de dominio

**ID:** `soc_siem` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio offline.

## Propósito y alcance
Diseña y opera capacidades de detección, triage, respuesta y mejora continua. El SOC debe convertir telemetría en decisiones y acciones verificables, no maximizar alertas. Definir servicios, cobertura horaria, severidades, propietarios, escalamiento y límites de autoridad.

## Arquitectura y fuentes
Inventariar SIEM, EDR/XDR, NDR, identidad, cloud, firewall, DNS, proxy, correo, aplicaciones, bases, OT y proveedores. Documentar agentes, colectores, colas, parsers, normalización, almacenamiento, retención, reglas, casos y SOAR. Medir pérdida, retraso, duplicación, cardinalidad, coste y sincronización temporal por fuente.

## Competencias
- Normalizar eventos con ECS, OCSF u otro esquema gobernado.
- Diseñar casos de uso ATT&CK con hipótesis y fuentes necesarias.
- Crear reglas con lógica, ventanas, umbrales, excepciones y test fixtures.
- Distinguir alertas, incidentes, eventos informativos y falsos positivos.
- Diseñar playbooks SOAR idempotentes, reversibles y con aprobación.
- Gestionar casos, evidencias, SLA, escalamiento y handoff.
- Medir MTTD, MTTA, MTTR, precisión, cobertura y coste por detección.

## Controles
- Acceso RBAC y segregación entre administración, analistas y respuesta.
- Protección de logs contra borrado, alteración y acceso excesivo.
- Redacción de secretos y PII; retención definida por finalidad.
- Sincronización NTP y normalización UTC.
- Reglas versionadas con pruebas positivas y negativas.
- SOAR con allowlist, permisos mínimos, idempotencia y kill switch.
- Cambios en reglas revisados, desplegados gradualmente y con rollback.

## Metodología
1. Definir activos críticos, amenazas prioritarias y requisitos de detección.
2. Medir telemetría disponible y lagunas de cobertura.
3. Construir hipótesis y mapearlas a ATT&CK.
4. Crear fixtures representativos y validar parser/correlación.
5. Medir falsos positivos con muestras reales anonimizadas o sintéticas.
6. Ejecutar en modo observación antes de automatizar respuesta.
7. Aprobar acciones sensibles con operador y registrar resultado.
8. Revisar eficacia, drift, coste y obsolescencia mensualmente.

## Laboratorio
SIEM local con Sysmon/Linux audit logs, eventos cloud sintéticos y alertas simuladas. Crear detecciones de inicio anómalo, cambio de privilegios y ejecución inusual; comprobar ventanas, exclusiones y escalamiento sin tocar endpoints productivos.

## Evaluación
Cada caso tiene hipótesis, fuentes, cobertura ATT&CK, datos de prueba, propietario, precisión, SLA y procedimiento de respuesta. SOAR demuestra idempotencia, reversión y registro.

## Referencias
MITRE ATT&CK, Sigma, OCSF, Elastic Common Schema, NIST SP 800-61 Rev. 3, FIRST CSIRT Framework y CISA logging guidance.

## Instrucciones IA
No automatices aislamiento, borrado o bloqueo de identidades sin autorización. Expón evidencia y confianza; no presentes una alerta como incidente confirmado.