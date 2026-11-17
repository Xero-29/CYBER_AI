# Ecosistema de herramientas y capacidades de CYBER_AI

## Inventario del código

El catálogo declarativo de `capability_inventory.py` contiene **21 herramientas**. El registro de adaptadores locales contiene **14 IDs**; Nuclei, además, tiene un runner de escaneo remoto separado.

| Grupo | Herramientas | Estado de integración |
|---|---|---|
| SAST y calidad | Semgrep, Bandit, Ruff, ShellCheck | Adaptadores locales |
| Dependencias | pip-audit, OSV-Scanner | pip-audit registrado pero bloqueado por política de red; OSV-Scanner solo catalogado |
| Supply chain y SBOM | Trivy, Grype, Syft | Trivy y Syft con adaptador; Grype solo catalogado |
| IaC y secretos | Checkov, Gitleaks, detect-secrets | Checkov y detect-secrets con adaptador; Gitleaks solo catalogado |
| Contenedores y CI/CD | Hadolint, actionlint, Kube-Linter | Adaptadores locales |
| Malware y forense | YARA, TShark, Zeek, Volatility 3 | YARA/TShark por runner Docker; Zeek/Volatility 3 solo catalogados |
| Red y vulnerabilidades | Nmap, Nuclei | Nuclei con runner remoto separado; Nmap solo catalogado |

### Recuento que no debe confundirse

- **21:** herramientas declaradas en el catálogo.
- **14:** IDs registrados en `TOOL_SPECS`.
- **11:** adaptadores que pueden ejecutarse directamente en host (siguen sin aislamiento de red obligatorio).
- **1:** pip-audit, registrado pero bloqueado porque aún no existe una política de red específica.
- **2:** YARA y TShark, integrados mediante runner Docker aislado.
- **7:** herramientas sin adaptador en `TOOL_SPECS`; Nuclei tiene su runner independiente, mientras que OSV-Scanner, Grype, Gitleaks, Zeek, Volatility 3 y Nmap siguen sin runner integrado.

La presencia de un binario, una entrada de catálogo o una ruta de integración no significa que esté instalado, probado ni autorizado para ejecutarse.

## Matriz de dominios

`domain_capability_matrix.py` conecta cada uno de los 48 paquetes offline con:
- Perfil de dominio y términos de enrutamiento en español/inglés.
- Paquete de conocimiento correspondiente.
- Herramientas candidatas declaradas para ese dominio.
- Estado real de disponibilidad y adaptador de cada candidata.
- Skills activas potencialmente relacionadas, consultadas sin incrementar contadores de uso.

El planificador añade `domain_capabilities`, `domain_tool_candidates` y `skill_candidates` al plan. Las herramientas se presentan como candidatas y nunca se ejecutan por el mero hecho de coincidir con un dominio.

Comandos:

```bash
python capability_inventory.py
python tool_registry.py "analisis estatico de codigo Python"
python task_planner.py "auditoria de red y analisis de PCAP"
```

## Reglas de integración y seguridad

1. Una candidata no es una orden de ejecución.
2. Una herramienta no instalada se informa como no disponible; nunca se simula que existe.
3. Una herramienta sin adaptador se marca como catálogo solamente.
4. Las herramientas de análisis local deben ejecutarse sobre rutas explícitas y con límites de recursos.
5. Las herramientas de red requieren autorización y alcance específicos.
6. YARA/TShark usan Docker con red deshabilitada; los adaptadores host y herramientas personalizadas no tienen aislamiento de egress obligatorio.
7. La salida de una herramienta es evidencia no confiable: se valida, normaliza y conserva con versión, hash y procedencia.
8. El catálogo no instala paquetes ni descarga binarios. La instalación debe gestionarse por un proceso reproducible y verificado.
9. Una Skill solo se sugiere cuando está activa en Skillbook. Una Skill no concede permisos ni sustituye validación humana.

## Brechas por cerrar

- Añadir adaptadores seguros y pruebas para OSV-Scanner, Grype, Gitleaks, Zeek, Volatility 3 y Nmap.
- Implementar aislamiento general para adaptadores host y herramientas personalizadas.
- Aplicar filtrado de egress para Nuclei y DNS pinning antes de admitir nombres DNS.
- Ampliar los conectores de SOC/SIEM, EDR/XDR, cloud, móvil, wireless, OT/ICS, hardware/firmware, PKI/HSM y seguridad de IA.
- Crear Skills verificadas por dominio; no generar Skills activas solo por coincidencia textual.
- Incorporar fuentes externas solo tras revisar licencia, procedencia, hash y vigencia.
- Validar herramientas y metodología en laboratorios autorizados.

**Conclusión:** la matriz ahora relaciona los 48 paquetes con el planificador y muestra las herramientas/Skills candidatas. Esto cierra la desconexión de enrutamiento, pero no convierte los paquetes en 48 capacidades operativas ni certifica cobertura integral.
