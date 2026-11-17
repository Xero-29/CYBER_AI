# Revisión de literatura exploratoria — Ingeniería inversa

**Corte:** 2026-11-17  
**Madurez:** M1 (mapa temático y referencia institucional localizada); **no M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Cómo caracterizar binarios y firmware de forma reproducible y con límites claros de inferencia?

## Síntesis

Análisis estático/dinámico, desensamblado, decompilación, emulación y diffing generan hipótesis, no fuente original. Ghidra es plataforma NSA; muestras deben ejecutarse aisladas, sin red por defecto, con hashes y límites.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

Packing; obfuscation; anti-analysis; payload; firmware extraction; protocol reverse engineering; unsafe parsers.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

Muestras benignas propias en sandbox sin red y snapshots; comparar análisis manual e instrumentado.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Funciones identificadas; cobertura; tiempo; reproducibilidad; falsos positivos; aislamiento.

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
| `RESEARCH-REVERSE` | Ghidra Software Reverse Engineering Framework | Localizada; texto íntegro pendiente |

## Identificadores del registro de fuentes

- `RESEARCH-REVERSE`
