# Matriz de reconciliación de PRs — 2026-11-20

**Base comparada:** `main` en `387104756d0f8307c39a46a1ea2df07671bd81c9`  
**Método:** comparación Git de cada HEAD de PR contra el mismo SHA de `main`.  
**Regla:** estos conteos describen diferencias de árbol; no son una evaluación de calidad ni de compatibilidad.

## 1. Diferencias por PR

| PR | HEAD | Estado de comparación | Commits ahead | Commits behind | Archivos | Añadidos | Modificados |
|---|---|---|---:|---:|---:|---:|---:|
| #11 | `04c001a206cde98613cf9c151ce4f6a95fb86a21` | diverged | 51 | 1 | 28 | 7 | 21 |
| #12 | `c2a397caf36f2661b6f0307168a0a24eee2f6d38` | diverged | 2 | 1 | 10 | 9 | 1 |
| #13 | `d0a3934a473e3d1117c7410df253f659d5f475c3` | diverged | 124 | 1 | 149 | 108 | 41 |
| #14 | `efa9108fe48c376b55b431f9078cf929ffd0a661` | diverged | 312 | 1 | 135 | 40 | 95 |

Los cuatro HEADs están una confirmación por detrás de la base actual. Antes de cualquier integración, se debe actualizar/rebasar o realizar una integración de tres vías y repetir el análisis sobre el nuevo HEAD.

## 2. Solapamientos de archivos confirmados

### PR #11 frente a PR #12 — siete rutas compartidas

- `PROJECT_STATUS.md`
- `requirements-documents.in`
- `requirements-documents.lock`
- `sandbox/requirements.in`
- `sandbox/requirements.lock`
- `tests/test_wheel_lock_generator.py`
- `wheel_lock_generator.py`

**Riesgo:** #11 y #12 no son integrables de forma independiente sin reconciliar versiones de locks y generador, pruebas y documentación. Debe definirse una implementación canónica, preservar requisitos por plataforma y regenerar hashes desde artefactos verificables.

### PR #13 frente a PR #14 — once rutas compartidas

- `.github/workflows/python-tests.yml`
- `knowledge/deep_modules/README.md`
- `knowledge/packs/api/README.md`
- `knowledge/packs/crypto/README.md`
- `knowledge/packs/foundations/README.md`
- `knowledge/packs/identity/README.md`
- `knowledge/packs/incident_response/README.md`
- `knowledge/packs/malware/README.md`
- `knowledge/packs/manifest.json`
- `knowledge/packs/threat_intel/README.md`
- `knowledge/research/source_registry.json`

**Riesgo:** #13 y #14 editan recursos editoriales, manifiestos y workflow en común. La integración debe preservar el estándar de investigación y el currículo, evitar que el contenido genérico de #13 sobrescriba el desarrollo disciplinar de #14 y comprobar que los manifiestos sigan apuntando a archivos válidos.

### Otros cruces

- #11 y #14 comparten `.github/workflows/python-tests.yml`.
- No se detectaron rutas compartidas entre #12 y #14 en la comparación consultada.
- La ausencia de rutas compartidas no garantiza ausencia de conflictos semánticos o de dependencias.

## 3. Secuencia de integración recomendada

1. **Resolver #11 + #12 como una sola reconciliación lógica**, manteniendo ramas separadas hasta que locks, wheel generator, safe I/O, SBOM, tests y documentación tengan una versión compatible.
2. Ejecutar los workflows y pruebas específicas sobre el resultado combinado.
3. **Resolver #13 + #14 a nivel de contenido y manifiestos**, no mediante una selección automática de archivos. El trabajo de #14 define la base curricular; los 192 borradores de #13 solo se incorporan cuando superen auditoría de especificidad y evidencia.
4. Revisar el workflow común y la fuente de referencias compartida; asegurar que ningún cambio relaje gates.
5. Ejecutar auditoría de integridad del árbol, cobertura de los 48 dominios, validación de manifiestos y CI completo.
6. Mantener cada PR draft hasta que la evidencia de su alcance esté disponible.

## 4. Decisión

No fusionar #11, #12, #13 ni #14 en su estado observado. No usar `mergeable=true` como sustituto de revisión: el estado Git de comparación indica divergencia y hay solapamientos reales de rutas.

El PR #16 (línea base) también permanece documental y en draft. La integración de cambios de producto requiere un PR de reconciliación posterior con diffs y resultados de CI del SHA final.
