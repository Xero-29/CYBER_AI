#!/usr/bin/env python3
"""Entrega resultados web a FILTRO y guarda un informe critico."""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from learning_memory import save_verified_lesson

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "reports" / "web_research"


def main():
    # Se requiere el JSON producido por web_research.py.
    if len(sys.argv) != 2:
        print(
            "Uso: .venv/bin/python review_web_report.py "
            "ruta/al/informe.json"
        )
        return 2

    source_path = Path(sys.argv[1]).expanduser()
    if not source_path.is_absolute():
        source_path = ROOT / source_path

    if not source_path.is_file():
        print(f"No existe el informe: {source_path}")
        return 2

    data = json.loads(source_path.read_text(encoding="utf-8"))

    if data.get("search_status") != "ok":
        print(
            "No se ejecuta FILTRO: la busqueda no termino con estado 'ok'."
        )
        print("Estado:", data.get("search_status", "desconocido"))
        print("No se debe interpretar un fallo de busqueda como falta de evidencia.")
        return 1

    # Solo utilizar paginas registradas que realmente se pudieron consultar.
    pages = [
        item for item in data.get("results", [])
        if item.get("registered_source") is True
        and item.get("fetch_status") == "pagina consultada"
        and item.get("page_text")
        and item.get("url")
    ][:4]

    if not pages:
        print("No hay paginas registradas con contenido consultado.")
        print("FILTRO no recibira fuentes que no podamos revisar.")
        return 1

    evidence = []
    for index, item in enumerate(pages, 1):
        host = urlparse(item["url"]).hostname or "dominio desconocido"
        evidence.append(
            f"[S{index}]\n"
            f"Titulo: {item.get('page_title') or item.get('title')}\n"
            f"Fuente registrada: {item.get('source_name')}\n"
            f"Dominio: {host}\n"
            f"Nivel de prioridad: {item.get('tier')}\n"
            f"URL: {item['url']}\n"
            f"Fecha de publicacion: "
            f"{item.get('published_at') or 'no detectada'}\n"
            f"Fecha de actualizacion: "
            f"{item.get('modified_at') or 'no detectada'}\n"
            f"Fecha de consulta: {item.get('retrieved_at_utc')}\n"
            f"Resumen del buscador: {item.get('search_snippet', '')[:400]}\n"
            f"Texto extraido de la pagina:\n"
            f"{item['page_text'][:1400]}\n"
        )

    # Mantener la evidencia original disponible durante todo el proceso.
    source_material = "\n".join(evidence)
    stage_results = []

    def run_agent(agent_name, prompt, token_limit):
        """Ejecuta un especialista y verifica si su respuesta terminó."""
        log_path = ROOT / "data" / "agent_tasks.jsonl"
        log_offset = log_path.stat().st_size if log_path.exists() else 0
        command = [
            sys.executable,
            str(ROOT / "agent_runner.py"),
            "ask", agent_name,
            "--think", "off",
            "--num-predict", str(token_limit),
            prompt,
        ]

        print(f"\n=== Ejecutando {agent_name} ===")
        try:
            result = subprocess.run(
                command, cwd=ROOT, capture_output=True,
                text=True, encoding="utf-8", errors="replace",
                timeout=300,
            )
        except subprocess.TimeoutExpired:
            print(f"ERROR: {agent_name} supero 300 segundos.")
            return ""

        if result.returncode != 0:
            print(f"ERROR: fallo {agent_name}.")
            print((result.stderr or result.stdout)[-1500:])
            return ""

        # Consultar el registro real de esta ejecución.
        task_record = None
        try:
            if log_path.exists():
                with log_path.open("rb") as log_file:
                    log_file.seek(log_offset)
                    new_lines = log_file.read().decode(
                        "utf-8", errors="replace"
                    ).splitlines()

                for line in new_lines:
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if str(record.get("agent", "")).upper() == agent_name.upper():
                        task_record = record

        except OSError as error:
            print(f"ERROR leyendo el registro: {error}")

        if not task_record or not task_record.get("done_reason"):
            print(
                f"ERROR: no se pudo verificar la finalizacion de {agent_name}. "
                "Se detiene el flujo por seguridad."
            )
            return ""

        done_reason = str(task_record["done_reason"]).lower()
        eval_count = task_record.get("eval_count")

        output = result.stdout
        marker = "=== RESPUESTA ==="
        if marker in output:
            output = output.split(marker, 1)[1]
        if "\nRegistro:" in output:
            output = output.split("\nRegistro:", 1)[0]

        answer = output.strip()
        if not answer:
            print(f"ERROR: {agent_name} no produjo respuesta final.")
            return ""

        stage_results.append({
            "agent": agent_name,
            "token_limit": token_limit,
            "eval_count": eval_count,
            "done_reason": done_reason,
            "response": answer,
        })

        print(
            f"{agent_name}: finalizacion={done_reason}; "
            f"tokens={eval_count}; caracteres={len(answer)}"
        )

        if done_reason in {"length", "limit"}:
            print(
                f"ERROR: la respuesta de {agent_name} fue truncada. "
                "No se acepta como etapa completa y no se publicara "
                "el informe final."
            )
            return ""

        return answer

    # ETAPA 1: NEXO analiza las fuentes sin inventar datos.
    nexo_prompt = f"""
Eres NEXO, analista de fuentes de CYBER_AI.
Consulta: {data.get('query', 'No especificada')}

Extrae solo hechos directamente relacionados con la consulta.
Maximo 60 palabras, con dos apartados:

Hallazgos:
Hasta dos hechos concretos, cada uno con una cita [S#].
Cada cita debe respaldar el hecho correspondiente.

Limites:
No inventes datos, fechas ni capacidades. No introduzcas temas nuevos.
No confundas fecha de consulta con fecha de publicacion.
Usa solo identificadores [S1] hasta [S{len(pages)}].

FECHA DE CONSULTA UTC: {data.get('retrieved_at_utc', 'No registrada')}

FUENTES:
{source_material}
"""
    nexo_answer = run_agent("NEXO", nexo_prompt, 260)
    if not nexo_answer:
        return 1

    # ETAPA 2: FILTRO critica el análisis de NEXO.
    filtro_prompt = f"""
Eres FILTRO, corrector de errores de CYBER_AI.

Compara la respuesta de NEXO con las fuentes originales.
Responde en español y utiliza exactamente estos campos, uno por línea:

TEMA: tema concreto de la consulta
ERROR: afirmación incorrecta o no respaldada de NEXO, o NINGUNO
CORRECCION: corrección respaldada por la fuente, o NINGUNA
LECCION: regla breve y reutilizable para evitar el error, o NINGUNA
FUENTE: identificador [S#] que respalda la corrección, o NINGUNA
EVIDENCIA: fragmento breve copiado de la fuente, o NINGUNA

No inventes errores para generar una lección.
No llames error a una afirmación correcta.
No propongas una lección si no hay un error concreto.
No confundas la fecha de consulta con publicación o actualización.
Usa solo identificadores entre [S1] y [S{len(pages)}].
Máximo 140 palabras. No repitas campos ni agregues otros apartados.

ANALISIS DE NEXO:
{nexo_answer}

FUENTES ORIGINALES:
{source_material}
"""
    filtro_critique = run_agent("FILTRO", filtro_prompt, 250)
    if not filtro_critique:
        return 1

    # ETAPA 3: VERITAS comprueba las afirmaciones frente a la evidencia.
    veritas_prompt = f"""
Eres VERITAS, verificador independiente de CYBER_AI.

Comprueba los hallazgos de NEXO y la corrección propuesta por FILTRO
contra el texto original. No inventes hechos ni temas nuevos.

Responde exactamente con estos campos, uno por línea:
HALLAZGO_1: RESPALDADA, PARCIAL o NO RESPALDADA
HALLAZGO_2: RESPALDADA, PARCIAL o NO RESPALDADA
LECCION: APROBADA, RECHAZADA o PENDIENTE
FUENTE: [S#] correspondiente, o NINGUNA
EVIDENCIA: fragmento textual breve y literal, o NINGUNA
MOTIVO: explicación breve

Aprueba la lección solo si:
- FILTRO identificó un error concreto en la respuesta de NEXO;
- la corrección está respaldada por la fuente citada;
- el fragmento de evidencia aparece en esa fuente;
- la lección es coherente con la corrección y no generaliza de más.

Si no hay un error concreto o falta evidencia, usa PENDIENTE o RECHAZADA.
No apruebes una lección solo porque la cita tenga un ID válido.
Máximo 130 palabras.

RESPUESTA DE NEXO:
{nexo_answer}

PROPUESTA DE FILTRO:
{filtro_critique}

FUENTES ORIGINALES:
{source_material}
"""
    veritas_check = run_agent("VERITAS", veritas_prompt, 250)
    if not veritas_check:
        return 1

    # 3. Guardar una lección solo tras aprobación y comprobación determinista.
    def read_field(content, label):
        match = re.search(
            rf"(?im)^\s*{re.escape(label)}\s*:\s*(.*?)\s*$",
            content
        )
        return match.group(1).strip() if match else ""

    error_text = read_field(filtro_critique, "ERROR")
    correction_text = read_field(filtro_critique, "CORRECCION")
    lesson_text = read_field(filtro_critique, "LECCION")
    filter_source = read_field(filtro_critique, "FUENTE")
    filter_evidence = read_field(filtro_critique, "EVIDENCIA")

    verdict = read_field(veritas_check, "LECCION").upper()
    verifier_source = read_field(veritas_check, "FUENTE")
    verifier_evidence = read_field(veritas_check, "EVIDENCIA")

    def source_number(value):
        match = re.search(r"\[S(\d+)\]", value)
        return int(match.group(1)) if match else None

    filter_source_id = source_number(filter_source)
    verifier_source_id = source_number(verifier_source)

    def normalize_evidence(value):
        return re.sub(r"\s+", " ", str(value)).strip().casefold()

    candidate_is_real = all([
        error_text,
        correction_text,
        lesson_text,
        error_text.upper() not in {"NINGUNO", "NINGUNA", "NO APLICA"},
        correction_text.upper() not in {"NINGUNO", "NINGUNA", "NO APLICA"},
        lesson_text.upper() not in {"NINGUNO", "NINGUNA", "NO APLICA"},
    ])

    saved_lesson = False
    save_reason = "No se aprobó una lección verificable."

    if verdict == "APROBADA" and candidate_is_real:
        if (
            filter_source_id is None
            or verifier_source_id is None
            or filter_source_id != verifier_source_id
            or not 1 <= verifier_source_id <= len(pages)
        ):
            save_reason = "Las referencias de FILTRO y VERITAS no coinciden."
        else:
            source = pages[verifier_source_id - 1]
            original_text = normalize_evidence(source.get("page_text", ""))
            quote = normalize_evidence(verifier_evidence)

            # El fragmento de VERITAS debe aparecer en el texto recolectado.
            if len(quote) < 12 or quote not in original_text:
                save_reason = (
                    "La evidencia citada por VERITAS no coincide "
                    "literalmente con el texto recopilado."
                )
            else:
                try:
                    saved = save_verified_lesson(
                        topic=read_field(filtro_critique, "TEMA")
                        or data.get("query", "Lección de investigación"),
                        error=error_text,
                        correction=correction_text,
                        evidence=[verifier_evidence],
                        source_urls=[source["url"]],
                        tags=re.findall(
                            r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
                            lesson_text.lower()
                        )[:8],
                        namespaces=["*"],
                        verified_by="VERITAS",
                        verifier_verdict="RESPALDADA",
                    )
                    saved_lesson = bool(saved.get("saved"))
                    save_reason = (
                        "Lección guardada para los agentes."
                        if saved_lesson
                        else saved.get("reason", "La lección ya existía.")
                    )
                except (ValueError, OSError, RuntimeError) as error:
                    save_reason = f"No se pudo guardar la lección: {error}"

    print("Aprendizaje compartido:", save_reason)

    # ETAPA 4: FILTRO integra la verificacion y redacta el informe final.
    # Mantener la crítica completa en los registros internos, pero no
    # mezclar afirmaciones no verificadas con los hallazgos de VERITAS.
    answer = (
        "## Verificacion de VERITAS (requiere revision humana)\n\n"
        + veritas_check.strip()
        + "\n\n## Critica interna de FILTRO\n\n"
        + "La critica completa se conserva en data/agent_tasks.jsonl. "
        + "No se incorpora como hallazgo porque sus afirmaciones deben "
        + "comprobarse individualmente contra las fuentes originales.\n\n"
        + "## Estado del analisis\n\n"
        + "Python reunio las respuestas de los agentes. Las citas se "
        + "validan por formato e identificador, pero esto no demuestra "
        + "que cada afirmacion este respaldada. El informe es un borrador."
    )
    print("Informe ensamblado con los hallazgos de VERITAS.")
    print("Informe ensamblado por Python; se omitio la cuarta llamada a FILTRO.")

    if not answer:
        return 1

    # Comprobar que existan citas y que sus IDs correspondan a las fuentes.
    citation_ids = {
        int(value) for value in re.findall(r"\[S(\d+)\]", answer)
    }
    invalid_citations = sorted(
        value for value in citation_ids
        if value < 1 or value > len(pages)
    )
    citations_ok = bool(citation_ids) and not invalid_citations
    citation_status = (
        "Citas detectadas; IDs dentro del rango"
        if citations_ok else
        "Citas ausentes o IDs invalidos: requiere revision manual"
    )
    print("Validacion automatica de citas:", citation_status)
    # Guardar el analisis y una bibliografia derivada de los datos originales.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # Ningun informe se considera verificado automaticamente.
    # Una cita valida por formato no garantiza que el contenido este respaldado.
    verification_has_unsupported = bool(
        re.search(r"NO RESPALDAD[AO]", veritas_check, flags=re.IGNORECASE)
    )

    if verification_has_unsupported:
        report_name = f"draft_unverified_{stamp}.md"
        report_status = (
            "BORRADOR NO VALIDADO: VERITAS detecto al menos "
            "una afirmacion no respaldada."
        )
    elif citations_ok:
        report_name = f"draft_with_citations_{stamp}.md"
        report_status = (
            "BORRADOR: los IDs de las citas tienen formato valido; "
            "la correspondencia entre cada afirmacion y su fuente "
            "requiere revision."
        )
    else:
        report_name = f"draft_unverified_{stamp}.md"
        report_status = (
            "BORRADOR NO VALIDADO: faltan citas o hay identificadores invalidos."
        )

    report_path = OUTPUT_DIR / report_name

    lines = [
        "# Informe de investigacion web: revision de FILTRO y VERITAS",
        "",
        f"- Consulta: {data.get('query', 'No especificada')}",
        f"- Recoleccion UTC: {data.get('retrieved_at_utc', 'No registrada')}",
        f"- Fuentes consultadas: {len(pages)}",
        f"- Validacion automatica de citas: {citation_status}",
        f"- Estado del informe: {report_status}",
        f"- Informe de origen: {source_path.relative_to(ROOT)}",
        "",
        answer,
        "",
        "## Fuentes proporcionadas a FILTRO",
        "",
    ]

    for index, item in enumerate(pages, 1):
        lines.extend([
            f"- **[S{index}] {item.get('title', 'Sin titulo')}**",
            f"  - URL: {item['url']}",
            f"  - Fuente registrada: {item.get('source_name')}",
            f"  - Publicacion: {item.get('published_at') or 'No detectada'}",
            f"  - Actualizacion: {item.get('modified_at') or 'No detectada'}",
            "",
        ])

    lines.extend([
        "## Limitacion del sistema",
        "",
        "Este informe es un analisis asistido por IA, no una certificacion "
        "automatica de veracidad. Las afirmaciones importantes requieren "
        "contraste independiente y las fechas ausentes siguen sin confirmar.",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print("\nBorrador de FILTRO guardado:")
    print("Estado:", report_status)
    print(report_path.relative_to(ROOT))
    print("\n=== INFORME ENSAMBLADO: FILTRO + VERITAS ===\n")
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
