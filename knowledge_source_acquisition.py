#!/usr/bin/env python3
"""Curated, license-aware source intake for the CYBER_AI knowledge pipeline."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "data/knowledge_sources/acquisition_sources.json"
OUTPUT_FILE = ROOT / "data/knowledge_sources/download_catalog.json"
VALID_TYPES = {"standard","standards_collection","machine_readable_dataset","technical_guidance","research_and_guidance","peer_reviewed_research","preprints","forensic_datasets","research_datasets","technical_documentation"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{1,79}$")

def load_sources(path=SOURCE_FILE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != "1.0.0":
        raise ValueError("Versión de catálogo no admitida.")
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise ValueError("sources debe ser una lista.")
    seen = set()
    for item in sources:
        if not isinstance(item, dict):
            raise ValueError("Cada fuente debe ser un objeto.")
        sid = item.get("id")
        if not isinstance(sid, str) or not ID_RE.fullmatch(sid) or sid in seen:
            raise ValueError(f"ID inválido o duplicado: {sid!r}")
        seen.add(sid)
        for field in ("title","publisher","url","landing_url","type","license","license_url","areas","format","cadence"):
            if not item.get(field): raise ValueError(f"{sid}: falta {field}")
        for field in ("url","landing_url","license_url","download_url"):
            value = item.get(field)
            if value:
                parsed = urlparse(value)
                if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError(f"{sid}: {field} debe ser HTTPS sin credenciales")
        if item["type"] not in VALID_TYPES: raise ValueError(f"{sid}: tipo no permitido")
        if not isinstance(item["areas"], list) or not item["areas"] or any(not isinstance(a,str) or not re.fullmatch(r"[a-z0-9_]+",a) for a in item["areas"]):
            raise ValueError(f"{sid}: áreas inválidas")
    return data

def build_downloader_catalog(data):
    resources=[]
    for source in data["sources"]:
        url=source.get("download_url")
        if not url: continue
        resources.append({"id":source["id"],"area_id":source["areas"][0],"url":url,"folder":source["id"],"filename":source["id"]+".json","max_bytes":20*1024*1024,"license":source["license"],"license_url":source["license_url"],"landing_url":source["landing_url"],"publisher":source["publisher"],"verified_for_download":False,"download":False})
    return {"schema_version":"1.0.0","policy":"Generated from acquisition_sources.json; downloads disabled until artifact-specific manual review.","areas":sorted({a for s in data["sources"] for a in s["areas"]}),"resources":resources}

def audit(data):
    return {"ok":True,"source_count":len(data["sources"]),"area_count":len({a for s in data["sources"] for a in s["areas"]}),"download_endpoint_count":sum(bool(s.get("download_url")) for s in data["sources"]),"enabled_download_count":0,"limitations":["Catalog metadata is not downloaded or read content.","Licenses must be verified per artifact and version.","Preprints are not treated as peer-reviewed publications.","No paywall bypass or automatic file execution."]}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit",action="store_true")
    parser.add_argument("--build-downloader-catalog",action="store_true")
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args(argv)
    if not args.audit and not args.build_downloader_catalog: parser.error("indica --audit o --build-downloader-catalog")
    data=load_sources(); report=audit(data)
    if args.build_downloader_catalog:
        OUTPUT_FILE.parent.mkdir(parents=True,exist_ok=True)
        tmp=OUTPUT_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(build_downloader_catalog(data),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        tmp.replace(OUTPUT_FILE); report["generated_catalog"]=str(OUTPUT_FILE.relative_to(ROOT))
    print(json.dumps(report,ensure_ascii=False,indent=2) if args.json else f"Fuentes: {report['source_count']} | áreas: {report['area_count']} | endpoints: {report['download_endpoint_count']} | descargas habilitadas: 0")
    return 0
if __name__=="__main__": raise SystemExit(main())
