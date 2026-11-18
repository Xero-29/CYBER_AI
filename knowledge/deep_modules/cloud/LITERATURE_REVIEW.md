# Revisión de literatura exploratoria — Seguridad cloud

**Corte:** 2026-11-17  
**Madurez:** M1 (mapa temático y referencia institucional localizada); **no M3/M4/M5**.  
**Alcance:** revisión exploratoria inicial y protocolo de investigación.  
**Procedencia:** la referencia nueva se localizó en el sitio del emisor, pero su texto completo no se declara leído. No es revisión sistemática ni validación empírica.

## Pregunta

¿Cómo demostrar aislamiento, identidad, configuración y trazabilidad de controles cloud?

## Síntesis

Responsabilidad compartida cambia por servicio. Separar plano de control/datos, identidad humana/workload, redes, secretos, almacenamiento y logging. NIST SP 800-144 y Zero Trust orientan diseño; IaC/escáneres no prueban permisos efectivos.

**Lectura crítica:** los marcos ordenan riesgos y requisitos, pero no prueban que un control esté desplegado o reduzca incidentes. Separar evidencia normativa, documentación de implementación, estudios empíricos y resultados del laboratorio. No atribuir a las fuentes contenido no examinado.

## Taxonomía técnica

IAM excesivo; storage público; metadata; secretos; APIs; tenant isolation; supply chain; drift.

## Hipótesis falsable

- **H1:** una evaluación estructurada y basada en escenarios del dominio detectará más fallos reproducibles que una revisión superficial basada solo en checklist.
- **H0:** la diferencia no es significativa bajo muestra y protocolo definidos.
- Son hipótesis propuestas, no resultados.

## Diseño experimental propuesto (no ejecutado)

Emulador/cuentas de prueba segregadas; roles, buckets y redes sintéticas; introducir misconfigurations.

Fijar versiones, commit, configuración, dataset, semillas y criterios antes de ejecutar; repetir; registrar desviaciones; conservar evidencia saneada. Usar solo activos propios o autorizados, con criterios de parada y rollback.

## Métricas

Exposiciones reproducibles; privilegios excesivos; cobertura; detección; falsos positivos; drift.

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
| `RESEARCH-CLOUD` | NIST Guidelines on Security and Privacy in Public Cloud Computing | Localizada; texto íntegro pendiente |

## Identificadores del registro de fuentes

- `RESEARCH-CLOUD`
