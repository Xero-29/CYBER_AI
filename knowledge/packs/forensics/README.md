# Forense digital — Guía de dominio

**ID:** `forensics` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Preserva, adquiere, analiza y comunica evidencia digital de forma reproducible y proporcional. La evidencia puede proceder de endpoints, memoria, discos, móviles, red, cloud, aplicaciones y SaaS. La validez depende de autorización, cadena de custodia, integridad, sincronización temporal y documentación.

## Fuentes y riesgos
Identificar discos, RAM, logs, eventos, artefactos de navegador, registro, filesystem, correo, nube, contenedores, snapshots, backups y capturas de red. Riesgos: modificar evidencia al adquirirla, perder volatilidad, relojes desincronizados, logs rotados, herramientas no validadas, datos personales excesivos y acceso fuera de jurisdicción.

## Competencias específicas
- Definir alcance, autoridad legal, custodio y objetivo probatorio.
- Adquirir imágenes bit a bit cuando proceda y verificar hashes.
- Preservar memoria y artefactos volátiles con prioridad temporal.
- Analizar sistemas de archivos, logs, timelines y metadatos.
- Normalizar zona horaria, drift y fuentes de tiempo.
- Correlacionar endpoint, red, identidad y cloud.
- Separar hechos, inferencias, hipótesis y opinión.
- Redactar informes reproducibles con limitaciones y cadena de custodia.

## Controles de evidencia
- Registrar quién, cuándo, cómo, dónde y bajo qué autoridad.
- Usar bloqueadores de escritura para medios físicos cuando aplique.
- Crear copia maestra y trabajar sobre copias verificadas.
- Calcular SHA-256 en adquisición y cada transferencia.
- Mantener logs de herramientas, versiones y parámetros.
- Limitar acceso y cifrar repositorios de evidencia.
- Documentar relojes, zona horaria, formato y desfase.
- Aplicar retención y minimización de datos personales.
- No alterar originales; preservar exportaciones nativas y metadatos.

## Metodología
1. Activar plan de preservación y definir alcance.
2. Priorizar evidencia volátil antes de apagar o aislar equipos.
3. Capturar datos con herramientas aprobadas y registrar parámetros.
4. Verificar integridad y cadena de custodia.
5. Analizar copias, construir timeline y correlacionar fuentes.
6. Validar hipótesis con artefactos independientes.
7. Documentar lagunas, limitaciones y posibles explicaciones alternativas.
8. Revisar el informe por un analista independiente.
9. Conservar evidencias conforme a retención y jurisdicción.

## Laboratorio seguro
Crear una VM con logs sintéticos, archivos de prueba y una línea temporal conocida. Practicar adquisición de imagen virtual, hash, extracción de logs y reconstrucción de eventos. No usar dispositivos de terceros ni datos personales reales.

## Evaluación
Integridad verificada, cadena de custodia completa, timeline trazable, conclusiones respaldadas, limitaciones explícitas y reproducibilidad independiente.

## Referencias y herramientas
NIST SP 800-86, ISO/IEC 27037, RFC 3227, SWGDE Best Practices, Autopsy, Sleuth Kit, Volatility 3, Plaso y Timesketch.

## Instrucciones para agentes IA
No afirmes causalidad a partir de un único artefacto. No modifiques evidencia original. Señala incertidumbre y preserva datos sensibles; no conviertas hipótesis en hechos.

## Biblioteca técnica e agenda de investigación

- [Compendio técnico específico](../../deep_modules/forensics/TECHNICAL_COMPENDIUM.md)
- [Agenda de investigación y protocolos](../../deep_modules/forensics/RESEARCH_AGENDA.md)
- [Revisión exploratoria de literatura](../../deep_modules/forensics/LITERATURE_REVIEW.md)
- [Seguimiento global de madurez y evidencia](../../EXPERT_LIBRARY_COMPLETION_TRACKER.md)

**Estado:** desarrollo editorial M2; las fuentes integrales, laboratorios ejecutados y revisión independiente siguen pendientes. No interpretar laboratorios diseñados como pruebas ejecutadas.
