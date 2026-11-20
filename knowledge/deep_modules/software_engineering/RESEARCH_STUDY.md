# Investigación técnica: Ingeniería de software, calidad y seguridad del ciclo de vida

**ID:** software_engineering · Corte: 2026-11-18 · Madurez inicial: M1/M2 · Auditoría de producto pendiente.

## Ingeniería del ciclo de vida
Requisitos, arquitectura, diseño, implementación, pruebas, release, operación y retirada. Mantener trazabilidad requisito→diseño→código→test→evidencia. Requisitos deben ser verificables, medibles, con owner, prioridad, amenaza y criterio de aceptación.

## Diseño y arquitectura
Modularidad, cohesión, acoplamiento, interfaces estables, error boundaries, idempotencia, concurrency, state management, data consistency, observability y fault tolerance. Documentar decisiones (ADR), trade-offs, invariantes y límites de confianza. Evitar capas sin propósito y abstracciones no utilizadas.

## Calidad
Tests unitarios, integración, contract, property-based, fuzz, mutation, regression, performance, chaos y end-to-end. Pirámide de pruebas debe equilibrar velocidad, fidelidad y costo. Medir cobertura de ramas y requisitos, no solo líneas. Flaky tests y skipped tests deben ser visibles y justificados.

## Seguridad de software
Threat modeling, secure coding, input validation, output encoding, parameterized queries, authn/authz, secrets, dependency hygiene, supply chain, secure defaults, logging y incident response. Integrar SSDF NIST 800-218 y perfiles aplicables. Revisiones humanas independientes para cambios sensibles.

## Mantenibilidad
Type hints, lint, formatting, documentación ejecutable, API compatibility, deprecation policy, migration, versioning y ownership. Eliminar dead code, módulos huérfanos y duplicación tras confirmar referencias y dependencias.

## Confiabilidad
Timeouts, retries con jitter, circuit breakers, bounded queues, backpressure, cancellation, graceful shutdown, transaction boundaries, backups y recovery. No reintentar operaciones no idempotentes sin estrategia.

## Laboratorios y métricas
Proyecto de referencia con pipeline CI, tests de contrato, fuzzing, SAST/SCA, SBOM, build reproducible y release firmado. Métricas: change failure rate, lead time, MTTR, escaped defects, flaky rate, coverage por requisito, deuda técnica y vulnerabilidades por release.

## Fuentes
- NIST SSDF SP 800-218: https://doi.org/10.6028/NIST.SP.800-218
- OWASP ASVS 5.0.0: https://asvs.owasp.org/
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1
- NIST CSF 2.0: https://doi.org/10.6028/NIST.CSWP.29

**Límite:** las métricas requieren definición operacional y baseline; no comparar equipos sin normalizar contexto.
