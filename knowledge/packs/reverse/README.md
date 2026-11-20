# Ingeniería inversa — Guía de dominio

**ID:** `reverse` · **Versión:** 2.0.0 · **Idioma:** español · **Distribución:** contenido editorial propio incluido offline.

## Propósito y límites
Analiza software compilado, firmware y protocolos para comprender comportamiento, compatibilidad, vulnerabilidades y procedencia. La ingeniería inversa puede ser legítima para defensa, interoperabilidad o investigación, pero requiere autorización y respeto a licencias, propiedad intelectual y privacidad.

## Superficie y artefactos
Cubrir PE, ELF, Mach-O, bytecode, firmware, librerías, símbolos, tablas de importación, strings, recursos, formatos y protocolos. Distinguir análisis estático, dinámico, emulación y depuración. Los binarios desconocidos se tratan como hostiles y no se ejecutan en el host.

## Competencias específicas
- Identificar arquitectura, formato, ABI y dependencias.
- Analizar headers, secciones, imports, símbolos y strings.
- Reconstruir flujo de control, funciones y estructuras.
- Usar desensamblado/decompilación sin asumir que el pseudocódigo es fuente original.
- Reconocer packing, ofuscación, anti-debugging y checks de integridad.
- Analizar firmware, particiones, boot chain y actualizaciones.
- Crear pruebas de comportamiento en emulador o sandbox.
- Documentar hallazgos con offsets, hashes y evidencia reproducible.

## Controles y límites
- Confirmar propiedad/autorización y objetivo de análisis.
- Preservar hash del binario y copia original inmutable.
- No ejecutar muestras desconocidas fuera de VM desechable.
- No conectar muestras a Internet real; simular DNS/HTTP cuando sea necesario.
- Limitar CPU, memoria, disco y tiempo.
- Separar herramientas de análisis del entorno productivo.
- No publicar claves, secretos ni datos personales hallados en binarios.
- Respetar licencias y no redistribuir código propietario.

## Metodología
1. Registrar autorización, origen, hash y contexto.
2. Identificar formato y arquitectura.
3. Realizar triage estático y extraer metadatos.
4. Construir hipótesis sobre funciones y flujo.
5. Seleccionar emulación/depuración aislada si es imprescindible.
6. Comparar comportamiento observado con hipótesis.
7. Validar hallazgos en fixture mínimo.
8. Preparar informe con offsets, referencias y limitaciones.
9. Preservar artefactos y limpiar entorno.

## Laboratorio seguro
Usar binarios de código abierto compilados localmente, crackmes educativos y firmware de demostración. Analizar funciones y formatos sin evadir licencias ni modificar dispositivos reales.

## Evaluación
Hashes y cadena de custodia, hipótesis comprobables, evidencia por offset, reproducción controlada y separación entre observación e inferencia.

## Referencias y herramientas
Ghidra, radare2, Binary Ninja, Capstone, QEMU, Binwalk, LLVM docs y formatos PE/ELF/Mach-O.

## Instrucciones para agentes IA
No ejecutes binarios desconocidos. No generes instrucciones de explotación de dispositivos ajenos. Usa muestras sintéticas o código abierto y explica límites de la decompilación.

## Biblioteca técnica e agenda de investigación

- [Compendio técnico específico](../../deep_modules/reverse/TECHNICAL_COMPENDIUM.md)
- [Agenda de investigación y protocolos](../../deep_modules/reverse/RESEARCH_AGENDA.md)
- [Revisión exploratoria de literatura](../../deep_modules/reverse/LITERATURE_REVIEW.md)
- [Seguimiento global de madurez y evidencia](../../EXPERT_LIBRARY_COMPLETION_TRACKER.md)

**Estado:** desarrollo editorial M2; las fuentes integrales, laboratorios ejecutados y revisión independiente siguen pendientes. No interpretar laboratorios diseñados como pruebas ejecutadas.
