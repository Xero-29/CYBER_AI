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

- Catálogo declarativo: **20 herramientas**.
- Adaptadores registrados: **14**; de ellos, **11** admiten ejecución local acotada, **1** (pip-audit) se bloquea por requerir red y **2** (YARA/TShark) se bloquean en host porque requieren aislamiento. Las restantes 6 herramientas siguen solo catalogadas.
- El inventario distingue disponibilidad del binario, adaptador registrado y bloqueo por política. Estar instalado o catalogado no concede autorización.
- La selección de herramientas no construye comandos shell ni otorga alcance de red.

## Adaptadores locales implementados

Los 11 adaptadores que pueden ejecutarse directamente en el host son Semgrep, Bandit, Ruff, Syft, Trivy, Checkov, detect-secrets, Hadolint, ShellCheck, actionlint y kube-linter.

- `tool_executor.py`: CLI explícita; sin `--execute` solo presenta un dry-run.
- Cada ejecución exige una ruta existente dentro del repositorio, rechaza enlaces simbólicos, limita el objetivo a 10.000 archivos y 100 MB, fija timeout (máximo 600 s), limita la salida capturada a 2 MB, evita shell y mata el grupo de procesos al agotar el tiempo.
- La evidencia registra versión y SHA-256 del binario antes/después, huellas del objetivo, código de salida, duración y salida. Si el binario cambia o desaparece, el resultado queda como error de integridad y los validadores del ledger fallan.
- Los archivos de evidencia se crean de forma exclusiva y atómica; en POSIX usan modo 0600 y directorio 0700. Pueden contener salida sensible. En Windows se deben aplicar ACL privadas en el directorio de evidencia.
- Semgrep exige configuración local explícita; no descarga reglas. Trivy usa flags offline y no actualiza bases.
- pip-audit se deniega porque requiere red. YARA y TShark se deniegan en el ejecutor local hasta integrarse en aislamiento. Nmap y Nuclei siguen bajo autorización de red separada.

**Límite de red importante:** el ejecutor local no aplica aislamiento de egress al proceso. La evidencia declara `network_access: not_enforced` y `network_isolation_enforced: false`; que una herramienta esté marcada como no dependiente de red no impide que el binario o una dependencia intente conectarse. Para garantizar ausencia de red se debe usar el runner Docker endurecido o una política de red del sistema operativo. No se debe analizar malware ni repositorios hostiles en modo local.

Ejemplos (desde la raíz del repositorio):

```bash
python tool_executor.py --tool ruff --target .
python tool_executor.py --tool ruff --target . --execute
python tool_executor.py --tool bandit --target .
python tool_executor.py --tool syft --target .
python tool_executor.py --tool trivy --target .
python tool_executor.py --tool semgrep --target . --config config/semgrep.yml
```

## Sandbox Docker en GitHub Actions

**Implementado en la rama `codex/security-integrity-audit`:**

- `sandbox_runner.py` invoca Docker con argumentos separados, sin shell, y mantiene una allowlist explícita que coincide con los binarios instalados en la imagen (actualmente Ruff y Bandit). Semgrep, Syft y Trivy se rechazan en el runner hasta que se incorporen y prueben en la imagen.
- El contenedor usa `--network=none`, `--read-only`, `--cap-drop=ALL`, `no-new-privileges`, usuario no root con el UID/GID del operador (la imagen tiene UID/GID predeterminado 65532), límites de 1 GiB RAM, 2 CPU y 128 procesos, y `/tmp` como tmpfs pequeño sin ejecución.
- El repositorio se monta en `/workspace` en solo lectura. La única ruta escribible montada es el directorio externo de evidencias en `/evidence`.
- No se monta el socket Docker, no se usa `--privileged`, no se pasan secretos al contenedor y las herramientas con política de red quedan denegadas. El runner limita también el proceso Docker del host; si vence el timeout, solicita `docker kill` y `docker rm --force` del contenedor nombrado.
- `.github/workflows/docker-sandbox.yml` construye la imagen y ejecuta pruebas unitarias más un smoke test de Ruff en GitHub-hosted runner efímero. El workflow tiene `contents: read`, checkout sin persistir credenciales y timeout de job.
- La imagen contiene versiones fijadas de Ruff y Bandit y ahora fija la imagen oficial Python 3.12 slim Bookworm por digest de manifiesto `linux/amd64`. El digest debe renovarse mediante revisión periódica de vulnerabilidades; fijarlo mejora reproducibilidad, pero no significa que sea permanentemente seguro. Las pruebas verifican que el runner rechaza Semgrep, Syft y Trivy mientras no estén instalados. `.dockerignore` excluye metadatos Git, artefactos, entornos virtuales y patrones comunes de secretos del contexto de build.
- Las acciones `checkout`, `setup-python` y `upload-artifact` del workflow están fijadas a SHA inmutables. El job mantiene permisos `contents: read`, checkout sin credenciales persistentes y no recibe secretos del repositorio.

Ejemplo:

```bash
docker build -t cyber-ai-tool-sandbox:local -f sandbox/Dockerfile .
python sandbox_runner.py --tool ruff --target tests/fixtures/sandbox_sample.py --execute
```

**Límites importantes:** Docker reduce la exposición, pero comparte el kernel del runner y no equivale a una microVM. GitHub-hosted runner efímero es una frontera razonable para pruebas y análisis benignos, no una garantía contra exploits del kernel o muestras deliberadamente hostiles. Para malware o entradas adversariales se requiere una VM/microVM desechable (por ejemplo, Firecracker/Kata bajo infraestructura controlada), con destrucción posterior y sin credenciales. GitHub-hosted `ubuntu-latest` no garantiza que el usuario pueda iniciar una microVM anidada con KVM; no se ha añadido una falsa promesa de microVM al workflow. La imagen base está fijada por digest, pero las dependencias Python instaladas con pip aún no están fijadas por hashes de artefactos ni tienen SBOM/procedencia firmada. No se afirma aislamiento fuerte ni ejecución de todos los adaptadores.
