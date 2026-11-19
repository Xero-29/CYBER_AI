# Investigación técnica: Inteligencia de amenazas

**ID:** threat_intel · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Calidad de fuentes y scoring pendiente.

## Propósito
La inteligencia de amenazas transforma datos en decisiones contextualizadas. Separar strategic, operational, tactical y technical intelligence; no llamar inteligencia a una lista de indicadores sin contexto. Definir consumidor, pregunta, decisión y horizonte temporal.

## Ciclo
1. Requisitos priorizados por stakeholder.
2. Plan de recolección legal y proporcional.
3. Adquisición desde fuentes públicas, comerciales, sectoriales e internas.
4. Normalización, deduplicación, enriquecimiento y evaluación de confianza.
5. Análisis de hipótesis, vínculos, temporalidad y alternativas.
6. Difusión con caveats, TLP/compartición y necesidad de saber.
7. Feedback y medición de utilidad.

## Modelos y formatos
MITRE ATT&CK describe tácticas/técnicas/subtécnicas observadas o conocidas por plataforma; fijar versión y no inferir comportamiento solo por coincidencia textual. ATT&CK v18 deprecó Data Sources; para detección nueva priorizar Detection Strategies/Analytics y fuentes de telemetría actuales. STIX/TAXII pueden facilitar intercambio estructurado; validar esquema, identidad, timestamps, markings, revocación y procedencia.

## Indicadores y evaluación
Un IOC (hash, IP, dominio, URL, certificado) tiene vida útil, contexto y posibilidad de shared hosting/CDN. No bloquear solo por coincidencia sin medir impacto. Registrar first_seen, last_seen, confidence, source, sightings, malware/campaign context, TLP y expiration. Combinar IOC con TTPs, infraestructura, vulnerabilidades, targeting, sector, geografía y telemetría propia.

## Sesgos y falsos positivos
Evitar confirmation bias, circular reporting, vendor bias, over-attribution y base-rate neglect. Diferenciar source reliability de information credibility. Registrar contradicciones, hipótesis alternativas, confidence y condiciones de refutación.

## Métricas
Tiempo desde señal a decisión, freshness, porcentaje de inteligencia accionable, precision de IOC, false positive, cobertura por sector/tecnología, decisiones influenciadas y feedback del consumidor. No medir éxito por número de indicadores ingestados.

## Laboratorios
Feed STIX sintético, TAXII server de prueba, IOC expirado, IP compartida, dominio benigno, ATT&CK mapping y detección basada en TTP. Probar dedupe, revocation, marking, TTL y confianza.

## Fuentes
- MITRE ATT&CK: https://attack.mitre.org/
- ATT&CK Data Sources deprecation: https://attack.mitre.org/datasources/
- CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- FIRST EPSS: https://www.first.org/epss/

**Límite:** no se descarga ni valida un feed en esta síntesis; toda fuente externa requiere reputación, licencia, privacidad y control de envenenamiento.
