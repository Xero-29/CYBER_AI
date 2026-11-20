"""Deterministic synthetic Foundations labs; no production systems are touched."""
from __future__ import annotations
import base64, hashlib, hmac, json, random
from collections import defaultdict
from typing import Any

def lab01_authorization() -> dict[str, Any]:
    policy={"version":1,"grants":{("analyst","case-1","read")}}
    cache={}
    def evaluate(role, resource, action):
        key=(role,resource,action); cached=cache.get(key)
        if cached and cached[0]==policy["version"]: return cached[1]
        decision=key in policy["grants"]; cache[key]=(policy["version"],decision); return decision
    before=evaluate("analyst","case-1","read")
    policy["grants"].remove(("analyst","case-1","read")); policy["version"]+=1
    after=evaluate("analyst","case-1","read")
    return {"initial_allow":before,"revoked_access_denied":not after,
            "unknown_action_denied":not evaluate("analyst","case-1","export"),
            "policy_version":policy["version"],"checks":3}

def _pair_metrics(predicted, truth):
    tp=len(predicted&truth); fp=len(predicted-truth); fn=len(truth-predicted)
    precision=tp/(tp+fp) if tp+fp else 1.0; recall=tp/(tp+fn) if tp+fn else 1.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {"precision":round(precision,4),"recall":round(recall,4),"f1":round(f1,4),"tp":tp,"fp":fp,"fn":fn}

def lab02_asset_reconciliation(seed=20261119):
    rng=random.Random(seed); records=[]; count=250
    for asset in range(count):
        host=f"host-{asset:04d}"
        if asset%25 in (0,1): host=f"clone-{asset//25:02d}"
        for source in ("cloud","edr"):
            records.append({"asset":asset,"hostname":host,"resource_id":f"cloud://region/resource/{asset:04d}","source":source})
    rng.shuffle(records); truth=set(); by_asset=defaultdict(list); by_host=defaultdict(list); by_resource=defaultdict(list)
    for i,r in enumerate(records):
        by_asset[r["asset"]].append(i); by_host[r["hostname"]].append(i); by_resource[r["resource_id"]].append(i)
    for ids in by_asset.values(): truth.add(tuple(sorted(ids)))
    def pairs(groups):
        return {tuple(sorted((ids[i],ids[j]))) for ids in groups.values() for i in range(len(ids)) for j in range(i+1,len(ids))}
    host=_pair_metrics(pairs(by_host),truth); stable=_pair_metrics(pairs(by_resource),truth)
    return {"seed":seed,"assets":count,"records":len(records),"hostname_baseline":host,
            "stable_resource_id":stable,"false_merge_reduction":host["fp"]-stable["fp"]}

def lab03_threat_model():
    edges={"internet":{"api"},"api":{"identity","queue"},"identity":{"database"},"queue":{"worker"},
           "worker":{"ci_runner"},"ci_runner":{"deployment_secret"},"deployment_secret":{"production"},
           "database":set(),"production":set()}
    paths=[("internet","api","identity","database"),("internet","api","queue","worker"),
           ("worker","ci_runner","deployment_secret","production")]
    found=sum(all(path[i+1] in edges.get(path[i],set()) for i in range(len(path)-1)) for path in paths)
    controls={"api":"authz","identity":"token_audience_validation","worker":"workload_identity",
              "ci_runner":"ephemeral_runner","deployment_secret":"secret_broker"}
    nodes={n for p in paths for n in p}
    return {"required_paths":len(paths),"paths_found":found,"path_coverage":round(found/len(paths),4),
            "control_mapped_nodes":sum(n in controls for n in nodes),"control_map":controls,
            "warning":"A graph path is a scenario candidate, not proof of exploitability."}

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _decode_b64url(segment: str) -> bytes:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    if not segment or "=" in segment or len(segment) % 4 == 1 or any(ch not in alphabet for ch in segment):
        raise ValueError("invalid unpadded base64url segment")
    return base64.b64decode(segment + "=" * (-len(segment) % 4), altchars=b"-_", validate=True)

def _strict_json_object(raw: bytes) -> dict[str, Any]:
    def reject_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON member")
            result[key] = value
        return result
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise ValueError("JWT segment must be a JSON object")
    return value

def encode_hs256_jwt(claims: dict[str, Any], key: bytes) -> str:
    """Test-fixture signer only; never use the embedded lab key in production."""
    if len(key) < 32:
        raise ValueError("HS256 test key must contain at least 256 bits")
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = f"{_b64url(json.dumps(header, separators=(',', ':'), sort_keys=True).encode())}.{_b64url(json.dumps(claims, separators=(',', ':'), sort_keys=True).encode())}"
    signature = hmac.new(key, signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url(signature)}"

def validate_hs256_jwt(token: str, *, key: bytes, issuer: str, audience: str,
                       now: int, required_scope: str, revoked: set[str]) -> bool:
    """Strict, bounded HS256 JWS verifier for the lab; not a general OIDC client."""
    try:
        if len(key) < 32 or not isinstance(token, str):
            return False
        parts = token.split(".")
        if len(parts) != 3 or any(not part for part in parts):
            return False
        header = _strict_json_object(_decode_b64url(parts[0]))
        claims = _strict_json_object(_decode_b64url(parts[1]))
        if set(header) != {"alg", "typ"} or header.get("alg") != "HS256" or header.get("typ") != "JWT":
            return False
        signing_input = f"{parts[0]}.{parts[1]}".encode("ascii")
        supplied = _decode_b64url(parts[2])
        expected = hmac.new(key, signing_input, hashlib.sha256).digest()
        if not hmac.compare_digest(supplied, expected):
            return False
        exp, nbf, aud = claims.get("exp"), claims.get("nbf", 0), claims.get("aud")
        audience_ok = aud == audience or (isinstance(aud, list) and audience in aud)
        if isinstance(exp, bool) or not isinstance(exp, (int, float)) or exp <= now:
            return False
        if isinstance(nbf, bool) or not isinstance(nbf, (int, float)) or nbf > now:
            return False
        if claims.get("iss") != issuer or not audience_ok:
            return False
        if not isinstance(claims.get("scope"), str) or required_scope not in claims["scope"].split():
            return False
        jti = claims.get("jti")
        if not isinstance(jti, str) or not jti or jti in revoked:
            return False
        return True
    except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError,
            base64.binascii.Error, OverflowError):
        return False

def lab04_identity():
    key = b"foundations-lab-hs256-key-32-bytes!"
    base = {"iss": "https://idp.lab.invalid", "aud": "api-a", "exp": 2000,
            "nbf": 900, "scope": "case:read", "jti": "token-001"}
    valid = encode_hs256_jwt(base, key)
    parts = valid.split(".")
    parts[1] = ("A" if parts[1][0] != "A" else "B") + parts[1][1:]
    wrong_signature = ".".join(parts)
    alg_none_header = _b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps(base).encode())
    unsigned = f"{alg_none_header}.{payload}."
    crit_header = _b64url(json.dumps({"alg": "HS256", "typ": "JWT", "crit": ["exp"]}, separators=(",", ":")).encode())
    crit_input = f"{crit_header}.{payload}"
    crit_signature = _b64url(hmac.new(key, crit_input.encode("ascii"), hashlib.sha256).digest())
    unsupported_header = f"{crit_input}.{crit_signature}"
    cases = {
        "valid": (valid, "case:read", set(), True),
        "wrong_signature": (wrong_signature, "case:read", set(), False),
        "alg_none_rejected": (unsigned, "case:read", set(), False),
        "unsupported_header_parameter": (unsupported_header, "case:read", set(), False),
        "wrong_issuer": (encode_hs256_jwt({**base, "iss": "https://evil.invalid"}, key), "case:read", set(), False),
        "wrong_audience": (encode_hs256_jwt({**base, "aud": "api-b"}, key), "case:read", set(), False),
        "expired": (encode_hs256_jwt({**base, "exp": 999}, key), "case:read", set(), False),
        "not_yet_valid": (encode_hs256_jwt({**base, "nbf": 1500}, key), "case:read", set(), False),
        "missing_scope": (valid, "case:export", set(), False),
        "revoked": (valid, "case:read", {"token-001"}, False),
        "malformed": ("not.a.jwt.with.extra", "case:read", set(), False),
    }
    outcomes = {name: validate_hs256_jwt(token, key=key, issuer="https://idp.lab.invalid",
        audience="api-a", now=1000, required_scope=scope, revoked=revoked)
        for name, (token, scope, revoked, _) in cases.items()}
    expected = {name: case[3] for name, case in cases.items()}
    return {"outcomes": outcomes, "all_expected": outcomes == expected,
        "negative_cases": len(cases) - 1, "signature_verified": outcomes["valid"],
        "limitations": "Faithful HS256 JWS verification prototype using Python stdlib; strict unpadded base64url, duplicate JSON rejection and exact header allowlist; no JWKS rotation, asymmetric algs, OIDC discovery, nonce/state flow, TLS, IdP or OAuth server integration."}

def lab05_crypto_integrity():
    old=b"synthetic-lab-key-v1-not-for-production"; new=b"synthetic-lab-key-v2-not-for-production"
    msg=b"synthetic evidence record: case-0001"
    tag=hmac.new(old,msg,hashlib.sha256).digest()
    valid=hmac.compare_digest(tag,hmac.new(old,msg,hashlib.sha256).digest())
    tamper=not hmac.compare_digest(tag,hmac.new(old,msg+b" altered",hashlib.sha256).digest())
    tag2=hmac.new(new,msg,hashlib.sha256).digest()
    rotated=hmac.compare_digest(tag2,hmac.new(new,msg,hashlib.sha256).digest())
    return {"valid_before":valid,"tamper_rejected":tamper,"new_key_verified":rotated,
            "old_tag_rejected_under_new_key":not hmac.compare_digest(tag,tag2),
            "scope":"HMAC-SHA-256 integrity/authenticity only; no confidentiality, AES, KMS, or FIPS validation."}

def _canonical_json(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def build_audit_chain(events: list[dict[str, Any]], key: bytes) -> list[dict[str, Any]]:
    if len(key) < 32:
        raise ValueError("audit-chain key must contain at least 256 bits")
    previous = "0" * 64
    records = []
    for sequence, event in enumerate(events, start=1):
        body = {"sequence": sequence, "event": event, "previous_mac": previous}
        mac = hmac.new(key, _canonical_json(body), hashlib.sha256).hexdigest()
        records.append({**body, "mac": mac})
        previous = mac
    return records

def verify_audit_chain(records: list[dict[str, Any]], key: bytes) -> bool:
    if len(key) < 32:
        return False
    previous = "0" * 64
    for expected_sequence, record in enumerate(records, start=1):
        if record.get("sequence") != expected_sequence or record.get("previous_mac") != previous:
            return False
        body = {"sequence": record.get("sequence"), "event": record.get("event"),
                "previous_mac": record.get("previous_mac")}
        expected = hmac.new(key, _canonical_json(body), hashlib.sha256).hexdigest()
        supplied = record.get("mac")
        if not isinstance(supplied, str) or not hmac.compare_digest(supplied, expected):
            return False
        previous = supplied
    return True

def lab06_event_reconstruction():
    truth = [{"id":"e1","ts":100,"actor":"svc-a","action":"token_issued"},
      {"id":"e2","ts":110,"actor":"svc-a","action":"secret_read"},
      {"id":"e3","ts":125,"actor":"svc-a","action":"deployment_started"},
      {"id":"e4","ts":140,"actor":"svc-a","action":"production_change"}]
    observed = [truth[2], truth[0], truth[1], truth[1], truth[3]]
    unique = {e["id"]: e for e in observed}
    timeline = sorted(unique.values(), key=lambda e: (e["ts"], e["id"]))
    expected = {e["id"] for e in truth}
    seen = set(unique)
    key = b"foundations-audit-chain-key-32-bytes!"
    chain = build_audit_chain(timeline, key)
    tampered = [dict(item) for item in chain]
    tampered[1]["event"] = {**tampered[1]["event"], "action": "forged_action"}
    reordered = [chain[1], chain[0], chain[2], chain[3]]
    return {"timeline_ids":[e["id"] for e in timeline],
      "event_completeness":round(len(seen & expected)/len(expected),4),
      "duplicate_events_removed":len(observed)-len(unique),
      "chronological":all(timeline[i]["ts"]<=timeline[i+1]["ts"] for i in range(len(timeline)-1)),
      "missing_event_ids":sorted(expected-seen),
      "hmac_chain_valid":verify_audit_chain(chain, key),
      "tampering_detected":not verify_audit_chain(tampered, key),
      "reordering_detected":not verify_audit_chain(reordered, key)}

def lab07_assurance():
    controls = [
      {"id":"C1","implemented":True,"owner":"owner-a","evidence":{"status":"current_test","valid_until":"2026-12-01","scope":"production","sha256":"a"*64,"contradictory":False}},
      {"id":"C2","implemented":True,"owner":"owner-b","evidence":{"status":"policy","valid_until":"2026-01-01","scope":"production","sha256":"b"*64,"contradictory":False}},
      {"id":"C3","implemented":False,"owner":"owner-c","evidence":None},
      {"id":"C4","implemented":True,"owner":"owner-d","evidence":{"status":"test","valid_until":"2026-12-01","scope":"production","sha256":"c"*64,"contradictory":True}},
    ]
    as_of = "2026-11-19"
    def acceptable(control):
        evidence = control.get("evidence")
        if not control.get("implemented") or not control.get("owner") or not isinstance(evidence, dict):
            return False
        digest = evidence.get("sha256", "")
        return (evidence.get("status") == "current_test"
          and evidence.get("scope") == "production"
          and evidence.get("valid_until", "") >= as_of
          and len(digest) == 64 and all(ch in "0123456789abcdef" for ch in digest)
          and evidence.get("contradictory") is False)
    closed = [c["id"] for c in controls if acceptable(c)]
    rejected = [c for c in controls if c["id"] not in closed]
    return {"controls":len(controls),"validly_closed":closed,
      "unsubstantiated_not_closed":[c["id"] for c in rejected],
      "false_closures_prevented":len(rejected),"coverage":round(len(closed)/len(controls),4),
      "as_of":as_of}



def lab08_safety_security_tradeoff():
    """Synthetic emergency-exit model; not a certified safety controller."""
    emergency = True
    electronic_ingress_locked = True  # fail-secure against unauthorized entry
    independent_mechanical_egress = True  # egress remains possible without controller power
    safety_egress_preserved = emergency and independent_mechanical_egress
    security_ingress_denied = emergency and electronic_ingress_locked
    return {
        "emergency": emergency,
        "safety_egress_preserved": safety_egress_preserved,
        "security_ingress_denied": security_ingress_denied,
        "joint_requirement_met": safety_egress_preserved and security_ingress_denied,
        "warning": "A synthetic state model is not a hazard analysis, certification or physical test.",
    }

def lab09_privacy_confidentiality_gap():
    """Shows that encrypted, access-controlled data can still be misused."""
    encrypted_at_rest = True
    access_controlled = True
    secondary_use_without_compatible_purpose = True
    confidentiality_protected = encrypted_at_rest and access_controlled
    privacy_risk = secondary_use_without_compatible_purpose
    minimised = True
    purpose_bound = True
    retention_limited = True
    mitigated_privacy_risk = not (secondary_use_without_compatible_purpose and not (minimised and purpose_bound and retention_limited))
    return {
        "confidentiality_protected": confidentiality_protected,
        "privacy_risk_detected": privacy_risk,
        "privacy_risk_mitigated_after_design_change": mitigated_privacy_risk,
        "warning": "The model is illustrative; legal basis and individual rights require context-specific review.",
    }

def lab10_resilience_recovery_trust():
    """Distinguishes service restoration from restoration of a trustworthy state."""
    service_restored_from_backup = True
    attacker_credentials_still_valid = True
    trust_restored_initially = service_restored_from_backup and not attacker_credentials_still_valid
    credential_rotation = True
    identity_rebuild = True
    backup_provenance_verified = True
    recovery_validation = credential_rotation and identity_rebuild and backup_provenance_verified
    trust_restored_after_controls = recovery_validation
    return {
        "service_available_after_restore": service_restored_from_backup,
        "trust_restored_before_controls": trust_restored_initially,
        "trust_restored_after_controls": trust_restored_after_controls,
        "warning": "A synthetic decision model does not prove recovery of a real environment.",
    }

def lab11_common_cause_redundancy():
    """Detects two nominally redundant nodes sharing a critical identity dependency."""
    nodes = ["node-a", "node-b"]
    shared_identity_provider = True
    shared_provider_failure = True
    both_unavailable = shared_identity_provider and shared_provider_failure
    independent_breakglass_path = True
    degraded_service_available = both_unavailable and independent_breakglass_path
    return {
        "redundant_nodes": len(nodes),
        "common_cause_detected": both_unavailable,
        "independent_recovery_path": independent_breakglass_path,
        "degraded_service_available": degraded_service_available,
        "warning": "Independence must be evidenced; naming two nodes does not establish redundancy.",
    }

def lab12_integrity_vs_truth():
    """Shows that an authentic, unmodified sensor record may still be wrong."""
    signature_valid = True
    hash_valid = True
    calibration_current = False
    independent_sensor_agrees = False
    integrity_and_authenticity = signature_valid and hash_valid
    semantic_validity = calibration_current and independent_sensor_agrees
    after_calibration_and_crosscheck = True
    return {
        "integrity_and_authenticity": integrity_and_authenticity,
        "semantic_validity_before_review": semantic_validity,
        "semantic_validity_after_calibration_and_crosscheck": after_calibration_and_crosscheck,
        "warning": "Cryptographic integrity does not establish truth, calibration or physical correctness.",
    }

def run_all():
    labs={"LAB-FND-01A":lab01_authorization(),"LAB-FND-02A":lab02_asset_reconciliation(),
      "LAB-FND-03A":lab03_threat_model(),"LAB-FND-04A":lab04_identity(),
      "LAB-FND-05A":lab05_crypto_integrity(),"LAB-FND-06A":lab06_event_reconstruction(),
      "LAB-FND-07A":lab07_assurance(),"LAB-FND-08A":lab08_safety_security_tradeoff(),
      "LAB-FND-09A":lab09_privacy_confidentiality_gap(),"LAB-FND-10A":lab10_resilience_recovery_trust(),
      "LAB-FND-11A":lab11_common_cause_redundancy(),"LAB-FND-12A":lab12_integrity_vs_truth()}
    checks={"authz_revocation":labs["LAB-FND-01A"]["revoked_access_denied"],
      "asset_stable_id_beats_hostname":labs["LAB-FND-02A"]["stable_resource_id"]["f1"]>=labs["LAB-FND-02A"]["hostname_baseline"]["f1"],
      "threat_paths_represented":labs["LAB-FND-03A"]["paths_found"]==labs["LAB-FND-03A"]["required_paths"],
      "identity_negative_tests":labs["LAB-FND-04A"]["all_expected"],
      "jwt_signature_verified":labs["LAB-FND-04A"]["signature_verified"],
      "crypto_tamper_rejected":labs["LAB-FND-05A"]["tamper_rejected"],
      "timeline_ordered":labs["LAB-FND-06A"]["chronological"],
      "audit_chain_tamper_detected":labs["LAB-FND-06A"]["tampering_detected"],
      "audit_chain_reordering_detected":labs["LAB-FND-06A"]["reordering_detected"],
      "assurance_stale_evidence_rejected":"C2" in labs["LAB-FND-07A"]["unsubstantiated_not_closed"],
      "safety_security_tradeoff_preserved":labs["LAB-FND-08A"]["joint_requirement_met"],
      "privacy_not_confidentiality":labs["LAB-FND-09A"]["confidentiality_protected"] and labs["LAB-FND-09A"]["privacy_risk_detected"],
      "recovery_requires_trust_rebuild":not labs["LAB-FND-10A"]["trust_restored_before_controls"] and labs["LAB-FND-10A"]["trust_restored_after_controls"],
      "common_cause_redundancy_detected":labs["LAB-FND-11A"]["common_cause_detected"],
      "integrity_not_truth":labs["LAB-FND-12A"]["integrity_and_authenticity"] and not labs["LAB-FND-12A"]["semantic_validity_before_review"]}
    return {"schema_version":"1.0.0","seed":20261119,"synthetic_only":True,
            "checks":checks,"all_checks_passed":all(checks.values()),"labs":labs}

if __name__=="__main__": print(json.dumps(run_all(),indent=2,sort_keys=True))
