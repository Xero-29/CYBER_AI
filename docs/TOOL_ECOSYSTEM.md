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
