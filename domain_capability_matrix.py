#!/usr/bin/env python3
"""Matriz trazable que conecta áreas, paquetes de conocimiento, herramientas y Skills.

La matriz descubre capacidades; nunca autoriza ni ejecuta herramientas.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "knowledge" / "packs" / "manifest.json"

# Términos en español/inglés usados para enrutar tareas. Los IDs deben coincidir
# exactamente con los paquetes offline versionados.
DOMAIN_PROFILES = {
    "foundations": {"name": "Fundamentos", "terms": ["fundamentos", "marco de ciberseguridad", "nist csf", "evaluacion de seguridad"], "tools": []},
    "appsec": {"name": "Seguridad de aplicaciones", "terms": ["aplicacion web", "appsec", "seguridad web", "sast", "codigo inseguro"], "tools": ["semgrep", "nuclei"]},
    "api": {"name": "Seguridad de API", "terms": ["api", "graphql", "rest", "swagger", "openapi"], "tools": ["semgrep", "nuclei"]},
    "network": {"name": "Redes", "terms": ["red", "network", "puertos", "firewall", "segmentacion", "pcap"], "tools": ["tshark", "zeek", "nmap"]},
    "linux": {"name": "Linux y Unix", "terms": ["linux", "unix", "hardening linux", "servidor linux"], "tools": ["semgrep"]},
    "windows_ad": {"name": "Windows y Active Directory", "terms": ["windows", "active directory", "ad ds", "kerberos", "gpo"], "tools": []},
    "cloud": {"name": "Seguridad cloud", "terms": ["cloud", "aws", "azure", "gcp", "nube"], "tools": ["trivy", "checkov"]},
    "containers": {"name": "Contenedores y Kubernetes", "terms": ["docker", "contenedor", "kubernetes", "k8s", "imagen"], "tools": ["trivy", "syft", "hadolint", "kube_linter"]},
    "mobile": {"name": "Seguridad móvil", "terms": ["android", "ios", "movil", "mobile", "apk", "ipa"], "tools": []},
    "crypto": {"name": "Criptografía", "terms": ["criptografia", "cifrado", "tls", "algoritmo criptografico"], "tools": []},
    "identity": {"name": "Identidad y acceso", "terms": ["identidad", "iam", "autenticacion", "autorizacion", "mfa", "sso"], "tools": []},
    "malware": {"name": "Análisis de malware", "terms": ["malware", "ransomware", "muestra sospechosa", "yara", "analisis estatico de malware"], "tools": ["yara"]},
    "forensics": {"name": "Forense digital", "terms": ["forense", "forensics", "memoria ram", "volcado de memoria", "pcap forense"], "tools": ["tshark", "volatility3", "yara"]},
    "incident_response": {"name": "Respuesta a incidentes", "terms": ["incidente", "respuesta a incidentes", "contencion", "erradicacion", "recuperacion"], "tools": ["yara", "tshark", "volatility3"]},
    "threat_intel": {"name": "Inteligencia de amenazas", "terms": ["inteligencia de amenazas", "threat intelligence", "ioc", "indicadores de compromiso"], "tools": []},
    "reverse": {"name": "Ingeniería inversa", "terms": ["ingenieria inversa", "reverse engineering", "desensamblado", "binario"], "tools": ["yara"]},
    "iot_hardware": {"name": "IoT y hardware", "terms": ["iot", "hardware", "firmware", "embebido", "dispositivo conectado"], "tools": []},
    "devsecops": {"name": "DevSecOps y supply chain", "terms": ["devsecops", "supply chain", "cadena de suministro", "sbom", "pipeline seguro"], "tools": ["semgrep", "trivy", "syft", "checkov", "actionlint", "gitleaks"]},
    "ai_security": {"name": "Seguridad de IA", "terms": ["seguridad de ia", "ai security", "modelo de lenguaje", "llm", "prompt injection"], "tools": ["semgrep"]},
    "governance": {"name": "Gobierno, riesgo y cumplimiento", "terms": ["gobierno", "grc", "cumplimiento", "auditoria iso", "riesgo cibernetico"], "tools": []},
    "vuln_management": {"name": "Gestión de vulnerabilidades", "terms": ["gestion de vulnerabilidades", "cve", "cvss", "epss", "priorizacion de vulnerabilidades"], "tools": ["nuclei", "trivy", "osv_scanner", "grype"]},
    "bug_bounty": {"name": "Bug bounty autorizado", "terms": ["bug bounty", "recompensa por errores", "programa de divulgacion"], "tools": ["nuclei", "nmap", "semgrep"]},
    "secure_arch": {"name": "Arquitectura segura", "terms": ["arquitectura segura", "diseno seguro", "threat modeling", "modelado de amenazas"], "tools": ["semgrep", "checkov"]},
    "data_security": {"name": "Seguridad de datos", "terms": ["seguridad de datos", "data security", "dataloss", "d lp", "clasificacion de datos"], "tools": ["gitleaks", "detect_secrets"]},
    "software_engineering": {"name": "Ingeniería de software", "terms": ["ingenieria de software", "calidad de codigo", "pruebas de software", "python", "revision de codigo"], "tools": ["semgrep", "bandit", "ruff", "shellcheck", "actionlint"]},
    "machine_learning": {"name": "Aprendizaje automático", "terms": ["machine learning", "aprendizaje automatico", "modelo ml", "entrenamiento de modelos"], "tools": []},
    "hardware_security": {"name": "Seguridad de hardware y firmware", "terms": ["seguridad de hardware", "firmware security", "arranque seguro", "secure boot", "jtag"], "tools": []},
    "mathematics": {"name": "Matemáticas y estadística", "terms": ["matematicas", "estadistica", "probabilidad", "metodos numericos"], "tools": []},
    "edr_xdr": {"name": "EDR y XDR", "terms": ["edr", "xdr", "endpoint detection", "telemetria de endpoint"], "tools": ["yara", "volatility3"]},
    "soc_siem": {"name": "SOC, SIEM y SOAR", "terms": ["soc", "siem", "soar", "centro de operaciones", "correlacion de eventos"], "tools": ["zeek", "tshark", "yara"]},
    "threat_hunting": {"name": "Threat hunting", "terms": ["threat hunting", "caza de amenazas", "busqueda de amenazas"], "tools": ["zeek", "tshark", "yara"]},
    "wireless_security": {"name": "Seguridad inalámbrica", "terms": ["wifi", "wi-fi", "wireless", "bluetooth", "nfc", "inalambrica"], "tools": ["tshark", "nmap"]},
    "ot_ics": {"name": "OT, ICS y SCADA", "terms": ["ot", "ics", "scada", "plc", "industrial"], "tools": ["tshark", "zeek", "nmap"]},
    "automotive_security": {"name": "Ciberseguridad automotriz", "terms": ["automotriz", "automotive", "can bus", "vehiculo conectado"], "tools": ["tshark"]},
    "satellite_security": {"name": "Seguridad satelital y espacial", "terms": ["satelite", "espacial", "space systems", "gnss"], "tools": ["tshark"]},
    "telecom_5g": {"name": "Telecomunicaciones y 5G", "terms": ["telecomunicaciones", "5g", "4g", "core movil", "ran"], "tools": ["tshark", "zeek"]},
    "physical_security": {"name": "Seguridad física", "terms": ["seguridad fisica", "control de acceso fisico", "cctv"], "tools": []},
    "fraud_abuse": {"name": "Fraude y abuso digital", "terms": ["fraude digital", "abuso de plataforma", "account takeover", "phishing"], "tools": []},
    "email_dns_security": {"name": "Correo, DNS y dominios", "terms": ["correo", "email security", "dns", "spf", "dkim", "dmarc"], "tools": ["nuclei", "nmap", "zeek"]},
    "privacy_engineering": {"name": "Ingeniería de privacidad", "terms": ["privacidad", "privacy engineering", "gdpr", "datos personales"], "tools": ["gitleaks", "detect_secrets"]},
    "cloud_forensics": {"name": "Forense cloud", "terms": ["forense cloud", "cloud forensics", "logs cloud", "evidencia cloud"], "tools": ["volatility3", "trivy"]},
    "database_security": {"name": "Seguridad de bases de datos", "terms": ["base de datos", "database security", "sql server", "postgresql", "mysql"], "tools": ["semgrep", "trivy"]},
    "pki_hsm": {"name": "PKI y HSM", "terms": ["pki", "hsm", "certificados digitales", "autoridad certificadora"], "tools": []},
    "post_quantum_crypto": {"name": "Criptografía poscuántica", "terms": ["poscuantica", "post quantum", "quantum safe", "kyber", "dilithium"], "tools": []},
    "ai_red_team": {"name": "Red Team de IA", "terms": ["red team de ia", "ai red teaming", "jailbreak de modelo", "evaluacion adversarial de llm"], "tools": []},
    "vulnerability_research": {"name": "Investigación de vulnerabilidades", "terms": ["investigacion de vulnerabilidades", "vulnerability research", "fuzzing", "cwe", "zero day"], "tools": ["semgrep", "nuclei", "nmap"]},
    "business_continuity": {"name": "Continuidad y recuperación", "terms": ["continuidad del negocio", "disaster recovery", "recuperacion ante desastres", "rto", "rpo"], "tools": []},
    "red_team": {"name": "Red Team autorizado", "terms": ["red team", "pentest", "prueba de penetracion", "evaluacion ofensiva autorizada"], "tools": ["nmap", "nuclei"]},
}

def _normalize(value):
    value = unicodedata.normalize("NFKD", str(value).casefold())
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", value).strip()

def load_domain_catalog():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    areas = data.get("areas", [])
    if not isinstance(areas, list):
        raise ValueError("El manifiesto de paquetes debe contener una lista de áreas.")
    ids = {item.get("id") for item in areas if isinstance(item, dict)}
    missing = ids - set(DOMAIN_PROFILES)
    stale = set(DOMAIN_PROFILES) - ids
    if missing or stale:
        raise ValueError(
            "La matriz de dominios no coincide con el manifiesto: "
            f"sin perfil={sorted(missing)}, perfiles obsoletos={sorted(stale)}"
        )
    return areas

def audit_domain_matrix():
    areas = load_domain_catalog()
    return {
        "manifest_area_count": len(areas),
        "profile_count": len(DOMAIN_PROFILES),
        "all_areas_mapped": len(areas) == len(DOMAIN_PROFILES),
        "unmapped_areas": [],
        "stale_profiles": [],
    }

def select_domain_capabilities(task, *, inventory=None, limit=12):
    """Relaciona la tarea con dominios, herramientas y Skills sin ejecutar nada."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("La tarea debe ser texto no vacío.")
    if not isinstance(limit, int) or not 1 <= limit <= 48:
        raise ValueError("limit debe estar entre 1 y 48.")
    areas = load_domain_catalog()
    from capability_inventory import TOOL_CATALOG, build_inventory
    from tool_adapters import TOOL_SPECS
    inventory = inventory or build_inventory()
    tool_catalog = {item["id"]: item for item in TOOL_CATALOG}
    normalized = _normalize(task)
    matches = []
    for area in areas:
        profile = DOMAIN_PROFILES[area["id"]]
        terms = profile["terms"]
        found = [term for term in terms if _normalize(term) in normalized]
        if not found:
            continue
        tool_candidates = []
        for tool_id in profile["tools"]:
            item = tool_catalog.get(tool_id)
            if item is None:
                continue
            detected = inventory.get("tools", {}).get(tool_id, {})
            adapted = tool_id in TOOL_SPECS
            tool_candidates.append({
                "id": tool_id,
                "name": item.get("purpose", tool_id),
                "available": bool(detected.get("available", False)),
                "adapter_registered": adapted,
                "adapter_status": (
                    "blocked_by_network_policy" if adapted and TOOL_SPECS[tool_id].get("network")
                    else "isolated_runner" if adapted and TOOL_SPECS[tool_id].get("requires_isolation")
                    else "local_adapter" if adapted
                    else "separate_runner" if tool_id == "nuclei"
                    else "catalog_only"
                ),
                "execution_permitted": False,
            })
        matches.append({
            "id": area["id"],
            "name": profile["name"],
            "knowledge_pack": area.get("path"),
            "knowledge_pack_status": area.get("status", "unknown"),
            "matched_terms": found,
            "tool_candidates": tool_candidates,
            "tool_gap": not bool(tool_candidates),
            "execution_started": False,
        })
    matches.sort(key=lambda item: (-len(item["matched_terms"]), item["id"]))
    selected = matches[:limit]
    skill_candidates = []
    try:
        from skillbook import search_skills
        seen = set()
        for domain in selected:
            for skill in search_skills(
                f"{task} {domain['id']} {domain['name']}", limit=3,
                record_usage=False,
            ):
                if skill["skill_id"] not in seen:
                    seen.add(skill["skill_id"])
                    skill_candidates.append({
                        "skill_id": skill["skill_id"],
                        "name": skill["name"],
                        "version": skill["version"],
                        "score": skill["score"],
                        "domain_id": domain["id"],
                    })
    except (ImportError, OSError, ValueError):
        skill_candidates = []
    return {
        "task": task,
        "matched_domain_count": len(selected),
        "domains": selected,
        "skill_candidates": skill_candidates[:10],
        "execution_started": False,
        "note": "La matriz enruta conocimiento y sugiere herramientas/Skills. No instala, ejecuta ni autoriza ninguna herramienta.",
    }

__all__ = ["DOMAIN_PROFILES", "audit_domain_matrix", "load_domain_catalog", "select_domain_capabilities"]
