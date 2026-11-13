# Ecosistema de herramientas de CYBER_AI

## Catálogo detectado

El inventario registra 20 herramientas en categorías separadas:

| Área | Herramientas |
|---|---|
| SAST y calidad | Semgrep, Bandit, Ruff, ShellCheck |
| Dependencias y vulnerabilidades | pip-audit, OSV-Scanner |
| Supply chain y SBOM | Trivy, Grype, Syft |
| IaC, secretos y contenedores | Checkov, Gitleaks, detect-secrets, Hadolint |
| CI/CD y Kubernetes | actionlint, kube-linter |
| Malware y forense | YARA, TShark, Zeek, Volatility 3 |
| Red activa | Nmap, Nuclei |

## Componentes

- `capability_inventory.py`: detecta ejecutables disponibles y plantillas locales. Solo consulta el PATH y el sistema de archivos; no ejecuta herramientas.
- `tool_registry.py`: selecciona candidatos según la tarea, explica coincidencias y muestra disponibilidad.
- `execution_policy.py`: conserva el control de autorización para acciones de red activas.

Uso:

```bash
python capability_inventory.py
python tool_registry.py "analisis estatico de codigo Python"
python tool_registry.py "inventario de dependencias"
python tool_registry.py "descubrimiento de red y puertos"
```

## Reglas de integración

1. Un candidato no es una orden de ejecución.
2. Una herramienta no instalada se informa como no disponible; nunca se simula que existe.
3. Las herramientas de análisis local deben ejecutarse sobre rutas explícitas y con límites de recursos.
4. Las herramientas que consultan bases remotas deben declarar su comportamiento de red, fuentes y caché.
5. Nmap y Nuclei requieren alcance autorizado y una integración de política específica antes de ejecutarse.
6. Análisis de muestras y volcados requiere aislamiento, límites de tamaño y protección de datos.
7. La salida de una herramienta es evidencia no confiable: se valida, normaliza y conserva con versión, hash y procedencia.
8. El catálogo no instala paquetes ni descarga binarios. La instalación debe gestionarse por un proceso reproducible de dependencias y verificación de hashes.

## Estado real

**Implementado:** inventario declarativo de 20 herramientas, detección de disponibilidad, selección explicable de candidatos y pruebas unitarias.

**No implementado todavía:** adaptadores de ejecución para Semgrep, Bandit, Ruff, pip-audit, OSV-Scanner, Trivy, Grype, Syft, Checkov, Gitleaks, detect-secrets, Hadolint, ShellCheck, actionlint, kube-linter, YARA, TShark, Zeek y Volatility. Su presencia en el catálogo no implica que estén instaladas ni que CYBER_AI ya pueda ejecutarlas.

**Próximo paso:** adaptadores pequeños y tipados, cada uno con esquema de entrada/salida, timeout, límites de salida, allowlist de rutas, versión, registro de evidencia y pruebas con binarios simulados. Integrarlos al motor de autorización sin permitir que el modelo construya comandos shell arbitrarios.

## Adaptadores locales implementados

- `tool_adapters.py`: adaptadores para **Semgrep, Bandit, Ruff, Syft y Trivy**.
- `tool_executor.py`: CLI explícita; sin `--execute` solo presenta un dry-run.
- `tool_registry.py`: distingue adaptadores disponibles, herramientas pendientes y capacidades bloqueadas por red.
- Cada ejecución exige una ruta existente dentro del repositorio, rechaza enlaces simbólicos, limita el objetivo a 10.000 archivos y 100 MB, fija timeout (máximo 600 s), limita la salida capturada a 2 MB, evita shell y mata el grupo de procesos al agotar el tiempo.
- Se registra JSON de evidencia con hash SHA-256 antes/después, código de salida, tiempo, comando, salida y estado. La salida no se convierte automáticamente en hallazgos confirmados ni Skills.
- Semgrep exige configuración local explícita; no descarga reglas.
- Trivy se ejecuta en modo offline y no actualiza bases. Si la base local no existe, la herramienta puede fallar; no se descarga automáticamente.
- **pip-audit permanece bloqueado**: su consulta de vulnerabilidades requiere red. No se ha habilitado acceso remoto implícito.
- Nmap y Nuclei mantienen su ruta de autorización de red separada; este conjunto de adaptadores no les concede permisos.

Ejemplos (desde la raíz del repositorio):

```bash
python tool_executor.py --tool ruff --target .
python tool_executor.py --tool ruff --target . --execute
python tool_executor.py --tool bandit --target .
python tool_executor.py --tool syft --target .
python tool_executor.py --tool trivy --target .
python tool_executor.py --tool semgrep --target . --config config/semgrep.yml
```

## Límites de seguridad pendientes

Estos adaptadores evitan invocación por shell y acotan tiempo/salida/rutas, pero **todavía no ejecutan los binarios dentro de un sandbox del sistema operativo**. No deben procesar repositorios hostiles o muestras de malware en una máquina con privilegios. Antes de uso institucional se requiere contenedor/namespace sin privilegios, filesystem de solo lectura, red deshabilitada por defecto, límites CPU/RAM/PID, firma/verificación de binarios y registro inmutable. La versión de cada binario aún debe incorporarse al manifiesto de evidencia.
