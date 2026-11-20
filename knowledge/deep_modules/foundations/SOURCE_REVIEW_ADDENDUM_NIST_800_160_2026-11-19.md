# Revisión dirigida de fuentes primarias — FND-01.01 (ciclo 2026-11-19)

**Tipo de revisión:** inspección dirigida de secciones oficiales; NO lectura integral.  
**Alcance:** dos publicaciones NIST primarias relevantes para ingeniería de sistemas seguros y resiliencia cibernética.  
**Regla:** el estado de lectura del registro permanece `selected_sections_reviewed`; no se promueve a `full_text_reviewed`.

## 1. NIST SP 800-160 Vol. 1 Rev. 1 — Engineering Trustworthy Secure Systems

- Publicación final: 2022-11-16; 195 páginas; DOI https://doi.org/10.6028/NIST.SP.800-160v1r1.
- Fuente oficial: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf
- Secciones inspeccionadas:
  - Páginas impresas 31–32: actividades de ingeniería de seguridad y seguridad como propiedad emergente del sistema; el texto explicita que no existe seguridad absoluta y que el diseño implica trade-offs sujetos a misión, protección, coste, calendario y rendimiento.
  - Páginas impresas 35–36: contexto de trustworthiness y assurance case; claims, subclaims, argumentos, evidencia, supuestos y mantenimiento del caso.
  - Páginas impresas 87–88: rigor proporcional a la consecuencia adversa, confianza composicional y protección continua a través de estados y transiciones.
  - Páginas impresas 102–103: assurance como confianza justificada basada en evidencia objetiva; evidencia relevante, exacta, creíble y suficiente; requisitos de confianza verificables.

### Aplicación a FND-01.01

1. La seguridad, safety, resiliencia y confiabilidad deben analizarse también como propiedades emergentes del sistema, no inferirse sumando propiedades aisladas de componentes.
2. La confianza de una composición no se hereda automáticamente de las declaraciones de cada componente. Se debe evaluar el conjunto que implementa la función.
3. La protección debe persistir en modos normales, degradados, recuperación y transiciones; una política correcta en el modo normal no basta.
4. Las afirmaciones de seguridad/safety necesitan argumento y evidencia adecuados al nivel de assurance. Una afirmación sin evidencia no es un resultado.

## 2. NIST SP 800-160 Vol. 2 Rev. 1 — Developing Cyber-Resilient Systems

- Publicación final: 2021-12; 310 páginas; DOI https://doi.org/10.6028/NIST.SP.800-160v2r1.
- Fuente oficial: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v2r1.pdf
- Secciones inspeccionadas:
  - Páginas impresas 8–9, capítulo 2 §2.1: constructos de ingeniería de resiliencia: goals, objectives, techniques, implementation approaches y design principles; los objetivos permiten derivar medidas de efectividad.
  - Páginas impresas 10–11, §2.1.1: cuatro objetivos de resiliencia —anticipate, withstand, recover, adapt— y tratamiento de adversidad que incluye condiciones, estrés, ataques y compromisos.
  - Páginas impresas 136–137, Appendix D §D.7: resiliencia cibernética complementa CIA y funciones de ciberseguridad; su foco es sostener misión/funciones esenciales, incluso cuando el adversario ya está presente.

### Aplicación a FND-01.01

1. Resiliencia no es sinónimo de uptime ni de redundancia: el objeto de aceptación es la continuidad de misión/funciones esenciales ante adversidad y la capacidad de recuperación/adaptación.
2. Los objetivos de resiliencia deben traducirse a objetivos y métricas específicos del sistema; no se deben copiar constructos genéricos sin tailoring.
3. CIA y resiliencia son complementarias. Un servicio puede estar disponible y aun así no ser confiable para una misión si su estado está comprometido.
4. La recuperación debe evaluarse por estado confiable y capacidad de misión, no solo por tiempo hasta que el proceso vuelva a responder.

## 3. Límites y no conformidades

- Esta revisión fue dirigida a secciones seleccionadas, no lineal ni exhaustiva.
- No se revisaron todas las referencias citadas por NIST ni se descargaron/hasharon artefactos para archivo local.
- No reemplaza normas sectoriales de safety, evaluación de riesgos del proceso ni regulación colombiana.
- No se realizó revisión de especialista independiente.
- No se ejecutó laboratorio ni experimento.

**Impacto de auditoría:** se amplía el soporte primario de los argumentos de propiedad emergente, assurance, confianza composicional, protección continua y resiliencia. No se cierra NC-FND-01.01-01 ni NC-FND-01.01-05 porque ambas requieren revisión integral y contraste de fuentes; no se eleva T0/O0.
