#!/usr/bin/env python3
"""Inventario declarativo de herramientas locales; no ejecuta herramientas."""
import json
import os
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from tool_adapters import TOOL_SPECS
from domain_capability_matrix import audit_domain_matrix

TOOL_CATALOG = [
 {"id":"semgrep","binary":"semgrep","category":"sast","purpose":"Análisis estático multi-lenguaje","risk":"local_read_only","execution_policy":"local_code_review"},
 {"id":"bandit","binary":"bandit","category":"sast","purpose":"Análisis estático de seguridad Python","risk":"local_read_only","execution_policy":"local_code_review"},
 {"id":"ruff","binary":"ruff","category":"quality","purpose":"Lint y análisis de código Python","risk":"local_read_only","execution_policy":"local_code_review"},
 {"id":"pip_audit","binary":"pip-audit","category":"dependencies","purpose":"Auditoría de dependencias Python","risk":"network_or_local_read","execution_policy":"dependency_audit"},
 {"id":"osv_scanner","binary":"osv-scanner","category":"dependencies","purpose":"Detección de vulnerabilidades en dependencias","risk":"network_or_local_read","execution_policy":"dependency_audit"},
 {"id":"trivy","binary":"trivy","category":"supply_chain","purpose":"Análisis de imágenes, repositorios y configuraciones","risk":"local_read_or_network","execution_policy":"artifact_scan"},
 {"id":"grype","binary":"grype","category":"supply_chain","purpose":"Análisis de vulnerabilidades de artefactos y SBOM","risk":"local_read_or_network","execution_policy":"artifact_scan"},
 {"id":"syft","binary":"syft","category":"supply_chain","purpose":"Generación de inventarios SBOM","risk":"local_read_only","execution_policy":"artifact_inventory"},
 {"id":"checkov","binary":"checkov","category":"iac","purpose":"Análisis estático de infraestructura como código","risk":"local_read_only","execution_policy":"iac_review"},
 {"id":"gitleaks","binary":"gitleaks","category":"secrets","purpose":"Detección local de secretos expuestos","risk":"local_read_only_sensitive_output","execution_policy":"secret_audit"},
 {"id":"detect_secrets","binary":"detect-secrets","category":"secrets","purpose":"Detección preventiva de secretos","risk":"local_read_only_sensitive_output","execution_policy":"secret_audit"},
 {"id":"hadolint","binary":"hadolint","category":"containers","purpose":"Lint de Dockerfiles","risk":"local_read_only","execution_policy":"container_review"},
 {"id":"shellcheck","binary":"shellcheck","category":"quality","purpose":"Análisis estático de scripts shell","risk":"local_read_only","execution_policy":"local_code_review"},
 {"id":"actionlint","binary":"actionlint","category":"ci_cd","purpose":"Validación de workflows GitHub Actions","risk":"local_read_only","execution_policy":"pipeline_review"},
 {"id":"kube_linter","binary":"kube-linter","category":"kubernetes","purpose":"Análisis estático de manifiestos Kubernetes","risk":"local_read_only","execution_policy":"kubernetes_review"},
 {"id":"yara","binary":"yara","category":"malware_analysis","purpose":"Coincidencia de reglas YARA sobre muestras","risk":"local_file_analysis","execution_policy":"isolated_sample_analysis"},
 {"id":"tshark","binary":"tshark","category":"network_forensics","purpose":"Análisis offline de capturas de red","risk":"local_file_analysis","execution_policy":"pcap_analysis"},
 {"id":"zeek","binary":"zeek","category":"network_forensics","purpose":"Análisis de tráfico y registros","risk":"local_file_or_authorized_capture","execution_policy":"pcap_analysis"},
 {"id":"volatility3","binary":"vol","category":"memory_forensics","purpose":"Análisis forense de volcados de memoria","risk":"local_file_analysis","execution_policy":"isolated_forensics"},
 {"id":"nmap","binary":"nmap","category":"network_discovery","purpose":"Descubrimiento y auditoría de red","risk":"active_network","execution_policy":"scoped_network_authorization"},
 {"id":"nuclei","binary":"nuclei","category":"vulnerability_scanning","purpose":"Detección basada en plantillas","risk":"active_network","execution_policy":"scoped_network_authorization"}
]


def _isolated_image_available():
    docker = shutil.which("docker")
    if not docker:
        return False, None
    image = os.environ.get(
        "CYBER_AI_ANALYSIS_SANDBOX_IMAGE", "cyber-ai-analysis-sandbox:1.0"
    )
    try:
        result = subprocess.run(
            [docker, "image", "inspect", "--format", "{{.Id}}", image],
            stdin=subprocess.DEVNULL, capture_output=True, text=True,
            timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, None
    image_id = result.stdout.strip()
    if result.returncode != 0 or not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id):
        return False, None
    return True, "docker-image:" + image_id


def build_inventory():
    """Detecta presencia y ruta sin ejecutar ni instalar herramientas."""
    isolated_available, isolated_path = _isolated_image_available()
    isolated_ids = {"yara", "tshark"}
    tools = {}
    for item in TOOL_CATALOG:
        tool_id = item["id"]
        requires_isolation = bool(TOOL_SPECS.get(tool_id, {}).get("requires_isolation", False))
        if tool_id in isolated_ids:
            available = isolated_available
            path = isolated_path
            binary = "docker-image"
        else:
            path = shutil.which(item["binary"])
            available = bool(path)
            binary = item["binary"]
        tools[tool_id] = {
            "available": available,
            "path": path,
            "binary": binary,
            "adapter_registered": tool_id in TOOL_SPECS,
            "execution_ready": (
                tool_id in TOOL_SPECS and available
                and not TOOL_SPECS[tool_id].get("network", False)
            ),
            "requires_isolation": requires_isolation,
            "offline_only": bool(TOOL_SPECS.get(tool_id, {}).get("offline_only", False)),
            "local_database_required": bool(TOOL_SPECS.get(tool_id, {}).get("local_database_required", False)),
            "host_network_isolation_enforced": (
                requires_isolation and isolated_available
            ),
            "explicit_execute_required": tool_id in TOOL_SPECS,
        }
    root = Path(os.environ.get(
        "CYBER_AI_NUCLEI_TEMPLATES", Path.home() / "nuclei-templates" / "http"
    )).expanduser()
    items, categories = [], Counter()
    if root.is_dir() and not root.is_symlink():
        for path in root.rglob("*.yaml"):
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root)
            category = relative.parts[0] if len(relative.parts) > 1 else "other"
            categories[category] += 1
            items.append({"name": path.stem, "path": str(path), "category": category})
    available = sum(item["available"] for item in tools.values())
    adapted = sum(item["adapter_registered"] for item in tools.values())
    available_and_adapted = sum(item["available"] and item["adapter_registered"] for item in tools.values())
    execution_ready = sum(item["execution_ready"] for item in tools.values())
    domain_matrix = audit_domain_matrix()
    return {
        "schema_version": "2.2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tools": tools,
        "tool_catalog": TOOL_CATALOG,
        "summary": {
            "registered": len(TOOL_CATALOG),
            "available": available,
            "unavailable": len(TOOL_CATALOG) - available,
            "adapter_registered": adapted,
            "catalog_only": len(TOOL_CATALOG) - adapted,
            "available_and_adapted": available_and_adapted,
            "execution_ready": execution_ready,
        },
        "domain_matrix": {
            **domain_matrix,
            "knowledge_pack_profiles_only": True,
            "operational_coverage_claimed": False,
        },
        "nuclei_templates": {
            "root": str(root), "available": root.is_dir() and not root.is_symlink(), "count": len(items),
            "categories": dict(sorted(categories.items())),
            "items": sorted(items, key=lambda item: item["path"]),
        },
        "safety": {
            "discovery_only": True, "executes_tools": False,
            "tool_presence_grants_permission": False,
            "active_network_requires_scoped_authorization": True,
            "local_host_egress_isolation": (
                "docker_network_none_for_yara_tshark_only"
                if isolated_available else "not_enforced"
            ),
            "direct_execution_requires_explicit_execute": True,
        },
        "note": "Inventario de presencia; no ejecuta, instala ni autoriza herramientas. OSV-Scanner/Grype requieren bases locales previamente aprovisionadas; offline_only es una opción del propio escáner, no aislamiento de egress del SO. YARA/TShark requieren imagen Docker y allowlist HMAC. La matriz de dominios enlaza paquetes y candidatas, no acredita cobertura operativa.",
    }


if __name__ == "__main__":
    output = Path("reports/capability_inventory.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    data = build_inventory()
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Herramientas registradas:", data["summary"]["registered"])
    print("Herramientas disponibles:", data["summary"]["available"])
    print("Adaptadores registrados:", data["summary"]["adapter_registered"])
    print("Áreas con perfil de matriz:", data["domain_matrix"]["profile_count"])
    print("Plantillas encontradas:", data["nuclei_templates"]["count"])
    print("Informe:", output)
