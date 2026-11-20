# Compendio técnico: Correo, DNS y dominios

ID: `email_dns_security` · Versión 0.1.0 · Cuaderno de desarrollo, no validación experta.

## Alcance
Currículo técnico de Correo, DNS y dominios; adaptar a arquitectura, criticidad, contexto y jurisdicción del entorno.

Ruta de desarrollo técnico; no declara cobertura exhaustiva ni fuentes leídas íntegramente. Operar solo con autorización explícita, datos sintéticos y laboratorios aislados. En infraestructuras físicas o críticas, usar simulación/bancos de pruebas y no intervenir producción.

## Desarrollo por subtema
### 1. SPF, DKIM y DMARC

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 2. DNSSEC y delegación

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 3. TLS, MTA-STS y DANE

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 4. phishing y BEC

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 5. dominios y certificados

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 6. reputación y detección

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

### 7. recuperación de cuentas

- **Modelo y contexto:** detallar arquitectura, componentes, estados, interfaces, identidades, flujos de datos y límites de confianza.
- **Amenazas:** describir abuso, fallos, configuración insegura, dependencias y condiciones previas; distinguir amenaza teórica de evidencia observada.
- **Controles:** mapear prevención, detección, respuesta y recuperación; justificar eficacia y riesgo residual.
- **Validación:** preparar pruebas positivas/negativas/de borde/regresión con datos sintéticos, resultado esperado, telemetría y criterio de parada.
- **Investigación:** revisar enfoques alternativos, resultados contradictorios, sesgos y límites de generalización.
- **Entregable:** análisis original, diagrama/modelo, matriz amenaza→control→evidencia, procedimiento reproducible y limitaciones.

## Laboratorio
Entorno: Laboratorio local o cuenta de pruebas aislada, sin datos reales ni objetivos de terceros.
Escenarios:
1. establecer baseline seguro y recoger evidencia
2. introducir un fallo/configuración sintética
3. detectar y analizar con procedimiento documentado
4. remediar de forma reversible y ejecutar regresión
Salvaguardas: Solo activos propios o expresamente autorizados; privilegios mínimos, límites de recursos, snapshots y reglas de parada.

| ID | Prueba | Evidencia |
|---|---|---|
| email_dns_security-LAB-01 | Baseline | Versiones, configuración, hashes y salida |
| email_dns_security-LAB-02 | Evento/fallo sintético | Entrada, precondiciones, logs y resultado |
| email_dns_security-LAB-03 | Detección/diagnóstico | Señal, cobertura, precisión y límites |
| email_dns_security-LAB-04 | Mitigación/recuperación | Diff, resultado antes/después y retest |

Diseño propuesto; no ejecutado.

## Métricas
Definir métricas acordes al caso: cobertura, eficacia del control/detección, falsos positivos/negativos, latencia, disponibilidad, impacto, recuperación y repetibilidad. Publicar unidad de análisis, muestra, baseline, versiones, repeticiones e incertidumbre.

## Método de investigación
- Búsqueda reproducible: bases, consultas, fechas, idiomas e inclusión/exclusión.
- Fuentes: estándares, especificaciones, documentación primaria, advisories y artículos revisados por pares.
- Texto completo solo se marca revisado tras inspección real.
- Extraer método, población, resultados, limitaciones, sesgos y amenazas a validez.
- Contrastar resultados y separar evidencia, inferencia e hipótesis.
- Registrar versión, licencia, URL canónica, fecha y hash cuando sea legal archivar.

## Preguntas candidatas
1. ¿Qué controles mejoran la eficacia frente a un baseline y en qué condiciones?
2. ¿Qué factores explican divergencias entre el estado del arte y las pruebas reproducidas?
3. ¿Qué señales permiten detectar antes sin elevar falsos positivos o impacto operacional?

Cada estudio debe definir H0/H1, variables, muestra, comparadores, refutación, análisis, ética y limitaciones.

## Artefactos exigibles
- [ ] Arquitectura y límites de confianza.
- [ ] Inventario de activos, datos, identidades, versiones y dependencias.
- [ ] Modelo de amenazas.
- [ ] Matriz amenaza→control→responsable→evidencia.
- [ ] Procedimientos reproducibles con rollback y parada.
- [ ] Laboratorio y casos con resultados medidos.
- [ ] Caso práctico con impacto, mitigación y retest.
- [ ] Evaluación con rúbrica.
- [ ] Fuentes, licencia, edición, fecha y hashes.
- [ ] Incertidumbre, sesgos y amenazas a validez.
- [ ] Revisión independiente y reproducción externa para M5.

## Madurez
M0/M1 estructural. No prueba profundidad ni madurez M3/M4/M5. Avanzar exige lectura crítica, artefactos específicos, experimentos ejecutados y evidencia auditable.


## Profundización técnica específica: Seguridad de correo y DNS

### Correo: arquitectura y autenticación
Modelar MTA, MDA, MUA, gateways, relay, SPF, DKIM, DMARC, ARC, TLS, MTA-STS y DANE según soporte. SPF autoriza hosts emisores, DKIM firma contenido/headers y DMARC alinea dominio visible con SPF/DKIM; ninguno elimina phishing ni abuso de cuentas válidas. Revisar subdominios, forwarding, mailing services y reportes agregados/forenses.

### Protección de identidad y contenido
Implementar MFA resistente a phishing, OAuth para acceso, bloqueo de autenticación legacy, protección de sesión, mailbox audit y alertas de reglas/forwarding. Revisar BEC, display-name spoofing, homoglyphs, QR phishing, adjuntos, URLs, macros y HTML remoto. Safe links/attachments requieren análisis de falsos positivos y bypass.

### DNS como plano de confianza
Revisar registrar, DNS provider, delegación, glue, DNSSEC, CAA, MX, SPF, DKIM selectors, DMARC, subdomain takeover y cambios no autorizados. Proteger cuentas de registrador con MFA, lock y separación de roles. DNSSEC autentica respuestas, no valida contenido de aplicación ni elimina compromiso de registrador.

### Telemetría y respuesta
Correlacionar message trace, headers, auth logs, DNS, URL click, endpoint, identity sign-ins y mailbox audit. Preservar headers completos, IDs, timestamps y hashes de adjuntos. Responder revocando sesiones, reglas maliciosas, forwarding, credenciales y tokens; buscar mensajes similares y destinatarios.

### Laboratorios
Dominios sintéticos con SPF/DKIM/DMARC; mensajes de phishing benignos controlados; detección de forwarding/reglas y simulación de BEC. Medir delivery, alignment, spoof detection, false positives y tiempo de contención.

## Estado de validación de la ampliación
Contenido editorial específico incorporado; lectura integral de fuentes, revisión independiente y experimentos permanecen pendientes. No declarar M3/M4/M5 sin evidencia.