"""Consulta referencias CVE exactas en la base pública NVD."""

import json
import urllib.error
import urllib.parse
import urllib.request


NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def verify_cve(cve_id):
    """Comprueba si NVD contiene el identificador CVE consultado."""
    if not cve_id.startswith("CVE-"):
        return {
            "cve_id": cve_id,
            "status": "invalid_identifier",
            "patch_status": "unverified",
        }

    url = f"{NVD_URL}?{urllib.parse.urlencode({'cveId': cve_id})}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CYBER_AI/1.0"},
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))

        vulnerabilities = payload.get("vulnerabilities", [])
        exact_match = any(
            item.get("cve", {}).get("id", "").upper() == cve_id.upper()
            for item in vulnerabilities
        )

        if exact_match:
            cve = next(
                item["cve"]
                for item in vulnerabilities
                if item.get("cve", {}).get("id", "").upper() == cve_id.upper()
            )
            descriptions = cve.get("descriptions", [])
            description = next(
                (item.get("value", "") for item in descriptions
                 if item.get("lang") == "en"),
                descriptions[0].get("value", "") if descriptions else "",
            )
            return {
                "cve_id": cve_id,
                "status": "found_in_nvd",
                "nvd_status": cve.get("vulnStatus", "unknown"),
                "published": cve.get("published"),
                "description": description,
                "patch_status": "unverified",
                "source": NVD_URL,
            }

        return {
            "cve_id": cve_id,
            "status": "not_found_in_nvd",
            "patch_status": "unverified",
            "source": NVD_URL,
            "warning": "No aparecer en NVD no demuestra que sea una vulnerabilidad nueva.",
        }

    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError) as exc:
        return {
            "cve_id": cve_id,
            "status": "verification_pending",
            "patch_status": "unverified",
            "error": str(exc),
        }


def enrich_analysis(analysis):
    """Añade verificaciones NVD sin declarar confirmado el hallazgo."""
    analysis["nvd_checks"] = [
        verify_cve(cve_id)
        for cve_id in analysis.get("cve_references", [])
    ]
    analysis["confirmed_vulnerability"] = False
    analysis["patch_status"] = "unverified"
    analysis["requires_manual_validation"] = True
    return analysis
