# Revisión de literatura inicial — DevSecOps y cadena de suministro

**Corte:** 2026-11-17  
**Madurez:** M1 documental; no M3/M4.  
**Alcance:** SDLC, CI/CD, runners, secretos, SAST/SCA/DAST, SBOM, procedencia y releases.

## Pregunta

¿Qué controles verificables reducen el riesgo de manipulación de código, credenciales, dependencias, runners y artefactos durante el ciclo de vida de software?

## Síntesis de fuentes primarias

- **NIST SSDF 1.1 (SP 800-218):** marco de prácticas de desarrollo seguro agrupadas en preparar la organización, proteger el software, producir software bien asegurado y responder a vulnerabilidades. Es una base de prácticas, no una certificación automática.
- **NIST DevSecOps Practices (borrador inicial publicado 2026-03-24):** documento vivo/preliminar que muestra enfoques para implementar SSDF mediante pipelines modernos. Se debe marcar como borrador, no norma final.
- **SLSA v1.1:** define requisitos de niveles de build y procedencia. La procedencia debe identificar el artefacto por digest y describir cómo se produjo; sus propiedades se analizan como completitud, autenticidad y exactitud. Emitir un archivo de provenance no demuestra automáticamente que el builder sea confiable.

## Modelo de amenazas de cadena de suministro

Activos: repositorios, ramas, workflows, tokens, secretos, runners, dependencias, caches, artefactos, registries, firmantes y consumidores.

Amenazas principales:
1. modificación no autorizada de código o workflow;
2. robo/reutilización de secretos;
3. dependencia comprometida o typosquatting;
4. runner persistente o compartido contaminado;
5. manipulación de artefactos/caches;
6. provenance falsa o incompleta;
7. publicación de artefacto distinto al probado;
8. compromiso de identidad del publicador.

Controles deben ser encadenados: protección de ramas y revisión, permisos mínimos por job, secretos efímeros, aislamiento/limpieza de runners, dependencias fijadas y verificadas, SBOM, provenance firmada, verificación del consumidor y respuesta de supply chain.

## Hipótesis investigables

- H1: la verificación de digest y provenance en el consumidor detecta más alteraciones del artefacto que confiar únicamente en el nombre/tag del paquete.
- H0: no existe diferencia bajo el banco definido.
- H2: runners efímeros y permisos mínimos reducen persistencia/alcance de compromiso frente a runners reutilizados, con coste medible de tiempo/recursos.

## Experimento propuesto (no ejecutado)

- **Banco:** repositorio de juguete, runner aislado y registry local; artefactos benignos sintéticos.
- **Escenarios:** tag mutable, artefacto sustituido, dependencia alterada, token con permisos excesivos, provenance ausente/malformada.
- **Comparadores:** pipeline básico frente a pipeline con digest pinning, permisos mínimos, runner efímero, SBOM y provenance verificada.
- **Métricas:** detección de manipulación, falsos positivos, cobertura de amenazas, latencia por build, coste de CPU/almacenamiento, secretos expuestos en logs y reproducibilidad.
- **Controles:** misma aplicación, commits y hardware; fijar versiones y semilla; repetir; registrar logs y hashes.
- **Criterio:** no declarar nivel SLSA solo por producir un attestation; mapear cada requisito de la especificación a evidencia real del builder.

## Aplicación al repositorio CYBER_AI

Brechas visibles en el estado canónico:
- Los runners locales generales y herramientas personalizadas no tienen aislamiento de red/sistema obligatorio.
- La evidencia de integridad no prueba la verdad semántica de un resultado.
- Falta evidencia de provenance verificable de releases y de verificación por consumidor.
- El CI debe reportarse por SHA exacto; un workflow cancelado o sin checks no equivale a verde.

Prioridad de implementación:
1. permisos mínimos por workflow/job y protección de ramas;
2. runners efímeros o aislamiento reforzado;
3. secretos de corta duración y rotación externa;
4. SBOM de dependencias y artefactos;
5. provenance firmada y verificada por digest;
6. política de publicación y rollback;
7. pruebas de supply-chain adversarial en entorno local.

## Brechas

Revisar requisitos SLSA por nivel, verificar builder y provenance en un consumidor independiente, y ejecutar los escenarios de manipulación descritos. La evidencia actual es documental; no se han ejecutado pipelines experimentales.

## Referencias

- NIST, SP 800-218 SSDF 1.1. https://doi.org/10.6028/NIST.SP.800-218
- NIST NCCoE, DevSecOps Practices, initial preliminary draft, 2026-03-24. https://csrc.nist.gov/pubs/other/2026/03/24/devsecops-practices/iprd
- SLSA, Specification v1.1. https://slsa.dev/spec/v1.1/
- SLSA, Provenance. https://slsa.dev/spec/v1.1/provenance


## Identificadores del registro de fuentes

- `NIST-SP-800-218`
- `NIST-DEVSECOPS-IPD-2026`
- `SLSA-v1.1`
