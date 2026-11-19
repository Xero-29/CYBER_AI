# Revisión de literatura exploratoria — Seguridad de APIs

**Corte:** 2026-11-17  
**Madurez:** M1 (mapa temático y referencia institucional localizada); **no M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Qué pruebas verifican autorización, límites, inventario y protección de datos en APIs?

## Síntesis

OWASP API Top 10 2023 separa BOLA, BOPLA, BFLA, consumo irrestricto, abuso de flujos, SSRF, configuración, inventario y consumo inseguro. Gateway y OpenAPI no prueban que el backend aplique controles contextuales.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

BOLA/BFLA/BOPLA; autenticación rota; SSRF; mass assignment; abuso de negocio; shadow APIs; agotamiento.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

API local con dos tenants/roles sintéticos. Comparar pruebas funcionales, contractuales y matriz negativa de autorización.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Recall/precision; cobertura de operaciones/roles; defectos escapados; falsos positivos; coste.

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
| `RESEARCH-API` | OWASP API Security Top 10 2023 | Localizada; texto íntegro pendiente |

## Identificadores del registro de fuentes

- `RESEARCH-API`


## Fuentes primarias adicionales inspeccionadas el 2026-11-19

| ID | Fuente | Qué se inspeccionó | Límite |
|---|---|---|---|
| `IETF-RFC9700` | RFC 9700 / BCP 240, OAuth 2.0 Security Best Current Practice (enero 2025) | RFC oficial y recomendaciones principales sobre redirect URI exacta, PKCE, CSRF/mix-up y sender-constrained tokens | No se declara lectura integral ni auditoría de todas las implementaciones |
| `OPENAPI-OAS-3.2.1` | OpenAPI Specification 3.2.1 | Índice oficial de versiones y advertencia sobre límites de validación de esquemas | Texto completo pendiente; la especificación no demuestra conformidad del servicio |
| `GRPC-AUTH-GUIDE` | gRPC Authentication | Guía oficial sobre credenciales y TLS | Validación de detalles por lenguaje/versión pendiente |

### Síntesis crítica

RFC 9700 es una Best Current Practice de IETF que actualiza el modelo de amenazas de OAuth y desaconseja modos de operación inseguros. La guía de API debe fijar la versión del protocolo y evaluar compatibilidad antes de cambiar flujos. OpenAPI define contratos, pero un schema validator no detecta todas las violaciones posibles y un contrato correcto no demuestra que el backend aplique autorización. La autenticación TLS/mTLS de gRPC protege el canal y puede autenticar el workload; no concede automáticamente autorización de negocio.

La lista OWASP API Top 10 2023 se utiliza como taxonomía de riesgos, no como medida de prevalencia universal. Las conclusiones se mantienen proporcionales a las páginas oficiales inspeccionadas.

## Límite de madurez empírica

**Límite explícito: no M3/M4/M5.** Este dossier permanece en M1 exploratorio. Las fuentes fueron localizadas y sus páginas oficiales inspeccionadas; la lectura integral, revisión sistemática, ejecución de laboratorios, análisis experimental, revisión independiente y reproducción externa siguen pendientes. Las hipótesis y protocolos son propuestas, no resultados.

- `IETF-RFC9700`

- `OPENAPI-OAS-3.2.1`

- `GRPC-AUTH-GUIDE`
