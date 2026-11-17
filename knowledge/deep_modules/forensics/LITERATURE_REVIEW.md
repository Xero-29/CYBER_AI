# Revisión de literatura inicial — Forense digital

**Corte:** 2026-11-17 · **Madurez:** M1 documental; no M3/M4.

## Pregunta
¿Cómo preservar y analizar evidencia digital de forma repetible, proporcional y legalmente defendible, distinguiendo adquisición, análisis e inferencia?

## Síntesis
NIST SP 800-86 (2006) aporta orientación de forense de computación y redes desde una perspectiva de TI/IR, cubriendo archivos, sistemas operativos, tráfico y aplicaciones. El propio documento indica que no es una guía exhaustiva paso a paso ni asesoría legal y recomienda consultar gestión y asesoría jurídica para cumplir la legislación aplicable. Debe complementarse con requisitos locales, políticas de evidencia, cadena de custodia y técnicas actuales para cloud, móviles y memoria.

## Método de evidencia
1. Autoridad, alcance, objetivo y reglas de privacidad.
2. Identificación y priorización de fuentes volátiles/no volátiles.
3. Preservación y adquisición con herramienta/versión documentada.
4. Hash criptográfico antes/después y copias de trabajo verificadas.
5. Registro de operador, UTC, reloj, método, dispositivo, errores y transferencias.
6. Análisis sobre copia, herramientas validadas y procedimientos reproducibles.
7. Separar hechos observados, inferencias, hipótesis y atribución.
8. Informe con limitaciones, falsos positivos, cadena de custodia y anexos.

## Hipótesis / experimento (no ejecutado)
H1: una plantilla automatizada de cadena de custodia y verificación de hashes reduce omisiones de metadatos frente a un registro manual libre. H0: sin diferencia.
Banco: imágenes forenses sintéticas y archivos benignos; dos métodos de documentación, múltiples operadores. Métricas: campos obligatorios completos, coincidencia de hash, reproducibilidad de hallazgos, tiempo y errores de transcripción. No usar evidencia real ni datos personales.

## Brechas
Actualizar prácticas para cloud snapshots, contenedores, móviles, memoria y SaaS; contrastar herramientas independientes; revisar legislación colombiana y jurisdicciones de operación con asesoría competente; probar formatos de exportación y preservación.

## Fuentes
- NIST SP 800-86: https://doi.org/10.6028/NIST.SP.800-86
- NIST SP 800-61 Rev. 3: https://doi.org/10.6028/NIST.SP.800-61r3

## Identificadores del registro de fuentes
- `NIST-SP-800-86`
- `NIST-SP-800-61r3`


## Identificadores del registro de fuentes

- `NIST-SP-800-86`
- `NIST-SP-800-61r3`
