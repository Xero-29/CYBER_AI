# Verificador de vulnerabilidades conocidas para CYBER_AI.
# Consulta la base pública NVD y conserva los casos sin verificar.

import json
import urllib.parse
import urllib.request
import urllib.error


def buscar_cve(consulta):
    """Busca coincidencias posibles en la base pública NVD."""

    url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0?"
        + urllib.parse.urlencode({
            "keywordSearch": consulta,
            "resultsPerPage": 5,
        })
    )

    solicitud = urllib.request.Request(
        url,
        headers={"User-Agent": "CYBER_AI/1.0"},
    )

    try:
        with urllib.request.urlopen(solicitud, timeout=15) as respuesta:
            datos = json.load(respuesta)

        resultados = []

        for elemento in datos.get("vulnerabilities", []):
            cve = elemento["cve"]

            resultados.append({
                "id": cve.get("id"),
                "publicada": cve.get("published"),
                "descripcion": next(
                    (
                        item["value"]
                        for item in cve.get("descriptions", [])
                        if item.get("lang") == "en"
                    ),
                    "Sin descripción disponible",
                ),
                "estado": "COINCIDENCIA POSIBLE; requiere validación",
                "parche": "No verificado",
            })

        return {
            "consulta": consulta,
            "resultados": resultados,
            "nota": (
                "Una búsqueda sin coincidencias no demuestra que "
                "la vulnerabilidad sea nueva. La ausencia de parche "
                "debe verificarse por separado."
            ),
        }

    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return {
            "consulta": consulta,
            "estado": "PENDIENTE DE VERIFICACIÓN",
            "error": str(error),
        }


if __name__ == "__main__":
    consulta = input("Producto o vulnerabilidad para consultar: ").strip()

    if consulta:
        print(json.dumps(
            buscar_cve(consulta),
            indent=2,
            ensure_ascii=False,
        ))
    else:
        print("La consulta no puede estar vacía.")
