# Ecosistema de herramientas y capacidades de CYBER_AI

## Inventario del código

El catálogo declarativo de `capability_inventory.py` contiene **21 herramientas**. El registro local contiene **20 IDs**; Nuclei conserva un runner remoto separado.

| Grupo | Herramientas | Estado de integración |
|---|---|---|
| SAST y calidad | Semgrep, Bandit, Ruff, ShellCheck | Adaptadores locales |
| Dependencias | pip-audit, OSV-Scanner | OSV-Scanner en modo offline con base local; pip-audit bloqueado por política de red |
| Supply chain y SBOM | Trivy, Grype, Syft | Grype en modo offline con base local; Trivy y Syft con adaptador |
| IaC y secretos | Checkov, Gitleaks, detect-secrets | Gitleaks local con redacción total de secretos; Checkov y detect-secrets con adaptador |
| Contenedores y CI/CD | Hadolint, actionlint, Kube-Linter | Adaptadores locales |
| Malware y forense | YARA, TShark, Zeek, Volatility 3 | YARA/TShark por runner Docker; Zeek offline sobre PCAP; Volatility 3 con plugins allowlisted y modo offline |
| Red y vulnerabilidades | Nmap, Nuclei | Nmap con adaptador TCP limitado a IP/CIDR autorizado; Nuclei con runner remoto separado |

### Recuento que no debe confundirse

- **21:** herramientas declaradas en el catálogo.
- **20:** IDs registrados en `TOOL_SPECS`.
- **17:** adaptadores directos en host: 16 locales/offline y Nmap, que requiere autorización activa y allowlist CIDR; el egress del host no está aislado.
- **1:** pip-audit, registrado pero bloqueado porque aún no existe una política de red específica.
- **2:** YARA y TShark, integrados mediante runner Docker aislado.
- **1:** Nuclei conserva su runner remoto separado y no es un ID de `TOOL_SPECS`.

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
6. YARA/TShark usan Docker con red deshabilitada. OSV-Scanner, Grype y Volatility 3 solicitan modo offline; Gitleaks y Zeek procesan archivos locales. Estas opciones del propio programa no son aislamiento de egress del sistema operativo; los adaptadores host siguen sin sandbox general.
7. La salida de una herramienta es evidencia no confiable: se valida, normaliza y conserva con versión, hash y procedencia.
8. El catálogo no instala paquetes ni descarga binarios. La instalación debe gestionarse por un proceso reproducible y verificado.
9. Una Skill solo se sugiere cuando está activa en Skillbook. Una Skill no concede permisos ni sustituye validación humana.

## Brechas por cerrar

- Implementar aislamiento de egress obligatorio para Nmap; el adaptador actual restringe alcance, puertos y duración, pero no impone firewall/sandbox de red a nivel del sistema operativo.
- Implementar aislamiento general para adaptadores host y herramientas personalizadas.
- Verificar en preflight la presencia y vigencia de las bases locales OSV-Scanner/Grype antes de declarar esos escáneres listos.
- Aplicar filtrado de egress para Nuclei y DNS pinning antes de admitir nombres DNS.
- Ampliar los conectores de SOC/SIEM, EDR/XDR, cloud, móvil, wireless, OT/ICS, hardware/firmware, PKI/HSM y seguridad de IA.
- Crear Skills verificadas por dominio; no generar Skills activas solo por coincidencia textual.
- Incorporar fuentes externas solo tras revisar licencia, procedencia, hash y vigencia.
- Validar herramientas y metodología en laboratorios autorizados.

**Conclusión:** la matriz ahora relaciona los 48 paquetes con el planificador y muestra las herramientas/Skills candidatas. Esto cierra la desconexión de enrutamiento, pero no convierte los paquetes en 48 capacidades operativas ni certifica cobertura integral.

## Adaptadores offline añadidos

- `osv_scanner`: `--offline`, salida JSON y base local previamente descargada. La base no se descarga desde CYBER_AI.
- `grype`: análisis de directorio en JSON; se desactiva la actualización automática y las fuentes externas. Requiere base local válida.
- `gitleaks`: análisis de directorio con informe JSON y `--redact=100`; puede devolver código 1 cuando encuentra secretos, que se interpreta como escaneo completado con hallazgos, no como fallo de ejecución.
- `zeek`: solo acepta PCAP/PCAPNG/CAP y ejecuta `-r` en un directorio temporal; los logs JSON se incorporan a la evidencia.
- `volatility3`: solo acepta archivo de volcado y plugin explícito de una allowlist; usa `--offline` y caché temporal.

Ejemplos:

```bash
python tool_executor.py --tool osv_scanner --target . --execute
python tool_executor.py --tool grype --target . --execute
python tool_executor.py --tool gitleaks --target . --execute
python tool_executor.py --tool zeek --target captures/sample.pcap --execute
python tool_executor.py --tool volatility3 --target captures/memory.raw --plugin windows.info --execute
```

Los ejemplos requieren binarios y, para OSV-Scanner/Grype, bases locales ya aprovisionadas. La ejecución no se activa automáticamente ni descarga herramientas o bases.

## Nmap: autorización obligatoria

El adaptador Nmap no acepta nombres DNS ni argumentos libres. Exige el flag `--authorized-network`, una IP/CIDR literal de máximo 16 direcciones y pertenencia a la allowlist del operador `CYBER_AI_NMAP_ALLOWED_CIDRS` (lista separada por comas). Ejecuta TCP connect sobre los 100 puertos frecuentes, con un reintento y límite de tiempo por host; no habilita NSE, detección de sistema operativo, DNS ni evasión. El inventario no lo marca `execution_ready` automáticamente. La allowlist no sustituye aislamiento de egress del host: úsalo únicamente con autorización expresa y controles de red externos.

```bash
export CYBER_AI_NMAP_ALLOWED_CIDRS="192.0.2.0/28"
python tool_executor.py --tool nmap --target 192.0.2.10 --authorized-network --execute
```

El rango anterior es solo un ejemplo documental reservado para pruebas; no representa un activo real.
