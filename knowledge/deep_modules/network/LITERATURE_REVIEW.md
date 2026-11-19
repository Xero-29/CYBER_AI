# Revisión de literatura exploratoria — Seguridad de redes

**Corte:** 2026-11-17  
**Madurez:** M1 (mapa temático y referencia institucional localizada); **no M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Cómo validar segmentación, filtrado y telemetría frente a movimiento lateral sin degradar servicios?

## Síntesis

Red integra routing, firewall, DNS, VPN, TLS, Wi-Fi, NAC e IDS. NIST SP 800-41 aporta principios firewall y SP 800-94 IDPS histórico. Segmentación nominal no prueba aislamiento; probar rutas, fallos fail-open/fail-closed y observabilidad.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

Lateral movement; routing leaks; firewall bypass; DNS abuse; downgrade; spoofing; tunnel abuse; IDS evasion.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

Topología virtual segmentada con servicios sintéticos; introducir reglas/rutas erróneas y fallos sensores.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Reachability no autorizada; cobertura zonas; latencia; detección; falsos positivos; drift.

## Amenazas a la validez y límites

- **Externa:** un laboratorio no representa automáticamente otros proveedores, arquitecturas o sectores.
- **Interna:** controlar versiones, instrumentación, selección de muestras y variables de confusión.
- **Constructo:** distinguir alertas, cobertura y puntuaciones de resultados reales de seguridad.
- **Reproducibilidad:** conservar scripts, hashes, datos sintéticos, versiones y pasos.
- **Ética:** autorización, minimización, alcance, parada y divulgación coordinada.

## Brechas y trabajo siguiente

1. Leer íntegramente las referencias primarias y registrar edición, fecha, hash, páginas revisadas y licencia.
2. Incorporar artículos revisados por pares con criterios de inclusión/exclusión reproducibles.
3. Contrastar la síntesis con especialistas y documentar desacuerdos.
4. Ejecutar el protocolo en laboratorio autorizado y publicar resultados negativos y análisis de incertidumbre.
5. No elevar a M4 sin experimento ejecutado y analizado; no elevar a M5 sin revisión independiente y reproducción externa.

## Referencias y procedencia

| ID | Referencia | Estado |
|---|---|---|
| `RESEARCH-NETWORK` | NIST SP 800-41 Rev. 1 Firewalls and Firewall Policy | Localizada; texto íntegro pendiente |

## Identificadores del registro de fuentes

- `RESEARCH-NETWORK`


## Actualización crítica de fuentes y límites
Se localizaron páginas oficiales de NIST para SP 800-41 Rev. 1 (publicación final de septiembre de 2009) y SP 800-94 (publicación final de febrero de 2007). NIST indica que el borrador SP 800-94 Rev. 1 de 2012 fue retirado y nunca se convirtió en publicación final; no debe citarse como estándar vigente. También se localizó la guía NSA de marzo de 2024 sobre madurez Zero Trust para el pilar de red/entorno, y la guía técnica ENISA de junio de 2025 con recomendaciones de segmentación y evidencia.

La antigüedad de NIST SP 800-41 y SP 800-94 obliga a tratarlos como referencias históricas/fundacionales, no como descripción exhaustiva de SDN, cloud-native networking, SASE, service mesh, QUIC o telemetría moderna. La revisión actual sigue siendo exploratoria: se inspeccionaron metadatos, abstracts y páginas de emisor; no se declara lectura integral de todos los documentos, revisión sistemática ni validación empírica.

## Fuentes localizadas para registrar
- NIST SP 800-41 Rev. 1: https://csrc.nist.gov/pubs/sp/800/41/r1/final
- NIST SP 800-94: https://csrc.nist.gov/pubs/sp/800/94/final
- NSA Zero Trust Network and Environment Pillar (2024): https://media.defense.gov/2024/Mar/05/2003405462/-1/-1/0/CSI-ZERO-TRUST-NETWORK-ENVIRONMENT-PILLAR.PDF
- ENISA Technical Implementation Guidance v1.0 (2025): https://www.enisa.europa.eu/sites/default/files/2025-06/ENISA_Technical_implementation_guidance_on_cybersecurity_risk_management_measures_version_1.0.pdf

## Madurez y puertas
- M1: mapa temático y fuentes localizadas.
- M2: contenido técnico ampliado en el compendio; requiere revisión de exactitud y contraste por tema.
- G1/G3: en progreso; G2 parcial; G4 parcialmente diseñado; G5–G8 pendientes.
- No M3/M4/M5. Los laboratorios siguen sin ejecución y no hay revisión independiente ni reproducción.
