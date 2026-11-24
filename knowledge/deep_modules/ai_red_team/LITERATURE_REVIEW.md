# Revisión de literatura exploratoria — Red teaming de IA

**Corte:** 2026-11-24  
**Madurez:** M1 (mapa temático y referencia institucional localizada); **no M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Qué escenarios revelan rutas de impacto en modelos y agentes conectados?

## Síntesis

Evaluar sistema completo: modelo, instrucciones, RAG, herramientas, permisos, memoria, conectores y supervisión. Los prompts aislados no representan rutas end-to-end. NIST AML, MITRE ATLAS y OWASP LLM Top 10 son taxonomías complementarias; medir impacto bloqueado, no solo rechazos textuales.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

Prompt injection; fuga; tool abuse; confused deputy; exceso de agencia; poisoning; extracción; DoS.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

Modelo local, documentos sintéticos y herramientas señuelo. Comparar prompts estáticos con escenarios completos; sin conectores productivos.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Éxito por escenario; impacto; fuga de canarios; acciones no autorizadas; falsos positivos; latencia.

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
| `RESEARCH-AI-RED-TEAM` | MITRE ATLAS | Localizada; texto íntegro pendiente |

## Referencias y procedencia

| ID | Referencia | Estado al corte |
|---|---|---|
| `RESEARCH-AI-RED-TEAM` | MITRE ATLAS | Localizada; lectura integral pendiente |
| `OWASP-LLM-TOP10-2026` | OWASP Top 10 for LLM Applications 2026 | Página oficial consultada; lectura integral pendiente |
| `OWASP-GENAI-REDTEAM-GUIDE` | OWASP GenAI Red Teaming Guide | Página oficial consultada; manual completo pendiente |
| `NIST-AI-200-3-ARIA` | NIST AI 200-3 ARIA Evaluation Planning Manual | Ficha oficial consultada; lectura integral pendiente |
| `NIST-AI-600-1` | NIST AI 600-1 Generative AI Profile | Referencia oficial registrada; lectura integral pendiente |

## Identificadores del registro de fuentes

- `RESEARCH-AI-RED-TEAM`
- `OWASP-LLM-TOP10-2026`
- `OWASP-GENAI-REDTEAM-GUIDE`
- `NIST-AI-200-3-ARIA`
- `NIST-AI-600-1`
