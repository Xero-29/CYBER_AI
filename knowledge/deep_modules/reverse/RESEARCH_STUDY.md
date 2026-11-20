# Investigación técnica: Ingeniería inversa y análisis de binarios

**ID:** reverse · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Análisis de muestras controladas pendiente.

## Alcance
Ingeniería inversa estudia estructura y comportamiento de software/binarios para interoperabilidad, auditoría, debugging, forense y seguridad. Confirmar autorización, licencia y límites legales antes de desensamblar, eludir controles o estudiar firmware propietario.

## Fundamentos
Dominar arquitecturas x86-64, ARM/AArch64, calling conventions, ABI, stack/heap, virtual memory, syscalls, ELF/PE/Mach-O, relocations, dynamic linking, symbols, exceptions, compiler optimization y debugging. Diferenciar código fuente, assembly, IR, bytecode, metadata y runtime behavior.

## Método estático/dinámico
Estático: identificar formato/arquitectura, hashes, imports/exports, strings, sections, control-flow, symbols, dependencies, signatures y anomalías. Dinámico: ejecución controlada, debugger, breakpoints, syscall/API tracing, memory snapshots, file/network diff y emulación. Las conclusiones deben indicar qué se observó directamente y qué se infirió.

## Anti-analysis y ofuscación
Packers, obfuscation, control-flow flattening, anti-debugging, anti-VM, dynamic API resolution y encrypted configuration complican análisis. Documentar límites y no tratar indicador de anti-analysis como prueba de malware. No usar bypasses contra software real sin autorización.

## Firmware
Extraer imágenes solo desde fuentes permitidas; validar hashes, formato, particiones, bootloader, filesystem, kernel, device tree, certificados, update manifest y rollback protection. No flashear hardware real sin banco seguro y recuperación de fábrica.

## Laboratorios
Programa benigno compilado con símbolos/no symbols, optimización, distintas arquitecturas y formatos; comparar decompilación, stack traces y comportamiento. Firmware emulado y muestras CTF. Mantener sandbox y snapshots.

## Métricas
Reproducibilidad del análisis, cobertura de funciones, calidad de anotaciones, tiempo de triage, falsos positivos y concordancia entre analistas.

## Fuentes
- Ghidra documentation: https://ghidra-sre.org/
- LLVM documentation: https://llvm.org/docs/
- NIST SP 800-86: https://doi.org/10.6028/NIST.SP.800-86
- MITRE ATT&CK: https://attack.mitre.org/

**Límite:** el material de herramientas cambia por versión; registrar build, plugins, arquitectura y licencia de cada herramienta.
