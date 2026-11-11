# Estado del proyecto CYBER_AI

**Actualizado:** 2026-11-11  
**Rama de trabajo:** `codex/security-integrity-audit`  
**Rama base:** `main`  
**Estado:** cambios iniciales implementados; validación de ejecución pendiente.

## Resumen

Se creó una rama de trabajo independiente para aplicar correcciones de seguridad e integridad sin modificar `main`. Los cambios se concentran en autorización explícita, preservación de evidencias, validación de identificadores y pruebas automatizadas.

## Cambios implementados

- **Escaneos Nuclei:** `scan_target` exige `authorized=True`; la CLI ofrece `--confirm-authorized`. Cada escaneo usa un JSONL con identificador único para no truncar ni mezclar evidencias anteriores.
- **Informes:** el índice de duplicados falla de forma segura si está corrupto, en vez de reemplazarlo por un índice vacío. La escritura del índice es atómica.
- **Procesamiento por lotes:** los nombres de salida incorporan una huella de la ruta de origen para evitar colisiones entre archivos con el mismo nombre base.
- **CLI:** `--self-test` ejecuta el descubrimiento de pruebas unitarias en `tests/`; los informes de escaneo usan nombres únicos.
- **NVD:** los identificadores CVE se validan con el formato esperado antes de realizar solicitudes.
- **Motor de agentes:** el texto generado por el agente ya no dispara acciones HTTP o de archivos automáticamente. Las propuestas requieren aprobación; la inspección HTTP exige confirmación explícita y la inspección de archivos queda confinada al proyecto.
- **Ejecutor de tareas:** se eliminan plantillas fuera de las familias previstas y cada escaneo conserva sus propios archivos de resultados.
- **Dependencias:** se declara `requests`, utilizada por la utilidad de auditoría local.
- **Pruebas:** se amplían las pruebas de autorización de Nuclei, corrupción del índice, validación CVE y acciones del motor de agentes. Se añadió un workflow de GitHub Actions para ejecutar la suite con Python 3.12.

- **IA desacoplada:** se añadió resolución de modelos por proveedor y por especialista en `llm_providers.py`. `agent_runner.py` usa esa resolución tanto para chat como para embeddings, sin cambiar el formato de memoria ni el Skillbook.
- **Configuración de proveedores:** un proveedor puede definir `models` por rol, `default_model` y `embedding_model`; las credenciales siguen llegando por variables de entorno.
- **Pruebas de adaptadores:** se ampliaron las pruebas para la selección de modelos remotos, modelos de embeddings y compatibilidad local.
- **Documentación:** `docs/AI_PROVIDER_ARCHITECTURE.md` describe cómo conectar un endpoint OpenAI-compatible sin tocar módulos de negocio y qué limitaciones siguen existiendo.

## Cómo validar

Desde la raíz del proyecto, con las dependencias instaladas:

```bash
python -m pip install -r requirements.txt
python cyber_ai.py --self-test
```

Para un escaneo Nuclei, además de indicar una URL dentro del alcance autorizado, hay que confirmar explícitamente:

```bash
python cyber_ai.py --scan https://objetivo-autorizado.example --confirm-authorized
```

No se debe ejecutar un escaneo contra sistemas de terceros sin permiso verificable.

## Pendiente

1. Ejecutar la suite completa en un entorno Python 3.12 y registrar los resultados reales, incluidas las nuevas pruebas de proveedores.
2. Revisar todas las rutas de ejecución de herramientas para aplicar un modelo uniforme de autorización y alcance.
3. Revisar concurrencia y recuperación del índice de informes.
4. Completar auditoría de secretos, validación de entradas y manejo de errores en los módulos restantes.
5. Añadir adaptadores nativos para proveedores que no implementen OpenAI-compatible (por ejemplo, APIs con protocolo propio), conservando el mismo contrato interno.\n6. Revisar el diff y abrir un Pull Request para revisión antes de integrar en `main`.

## Limitaciones de esta entrega

Los archivos se modificaron mediante GitHub. No se dispuso de un entorno de ejecución del repositorio en esta sesión y el conector no devolvió ejecuciones de Actions para el último commit; por tanto, **las pruebas no se han ejecutado y no se afirma que estén pasando**. Los cambios deben considerarse una primera corrección revisable, no una auditoría completa ni una certificación de seguridad.
