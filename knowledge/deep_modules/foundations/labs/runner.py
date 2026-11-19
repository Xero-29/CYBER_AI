"""Deterministic synthetic Foundations labs; no production systems are touched."""
from __future__ import annotations
import hashlib, hmac, json, random
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

def validate_token(claims, *, issuer, audience, now, required_scope, revoked):
    return bool(claims.get("iss")==issuer and claims.get("aud")==audience
        and isinstance(claims.get("exp"),int) and claims["exp"]>now
        and required_scope in str(claims.get("scope","")).split()
        and isinstance(claims.get("jti"),str) and claims["jti"] not in revoked)

def lab04_identity():
    base={"iss":"https://idp.lab.invalid","aud":"api-a","exp":2000,"scope":"case:read","jti":"token-001"}
    cases={"valid":(base,"case:read",set(),True),
      "wrong_issuer":({**base,"iss":"https://evil.invalid"},"case:read",set(),False),
      "wrong_audience":({**base,"aud":"api-b"},"case:read",set(),False),
      "expired":({**base,"exp":999},"case:read",set(),False),
      "excess_scope_missing":(base,"case:export",set(),False),
      "revoked":(base,"case:read",{"token-001"},False)}
    outcomes={name:validate_token(claims,issuer="https://idp.lab.invalid",audience="api-a",now=1000,
              required_scope=scope,revoked=revoked) for name,(claims,scope,revoked,_) in cases.items()}
    expected={name:case[3] for name,case in cases.items()}
    return {"outcomes":outcomes,"all_expected":outcomes==expected,"negative_cases":len(cases)-1,
            "limitation":"Claims validation simulation only; no JWT signature or OAuth/OIDC implementation."}

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

def lab06_event_reconstruction():
    truth=[{"id":"e1","ts":100,"actor":"svc-a","action":"token_issued"},
      {"id":"e2","ts":110,"actor":"svc-a","action":"secret_read"},
      {"id":"e3","ts":125,"actor":"svc-a","action":"deployment_started"},
      {"id":"e4","ts":140,"actor":"svc-a","action":"production_change"}]
    observed=[truth[2],truth[0],truth[1],truth[1],truth[3]]
    unique={e["id"]:e for e in observed}; timeline=sorted(unique.values(),key=lambda e:(e["ts"],e["id"]))
    expected={e["id"] for e in truth}; seen=set(unique)
    return {"timeline_ids":[e["id"] for e in timeline],"event_completeness":round(len(seen&expected)/len(expected),4),
            "duplicate_events_removed":len(observed)-len(unique),
            "chronological":all(timeline[i]["ts"]<=timeline[i+1]["ts"] for i in range(len(timeline)-1)),
            "missing_event_ids":sorted(expected-seen)}

def lab07_assurance():
    controls=[{"id":"C1","implemented":True,"evidence":"current_test","owner":"owner-a"},
      {"id":"C2","implemented":True,"evidence":"expired_policy","owner":"owner-b"},
      {"id":"C3","implemented":False,"evidence":"none","owner":"owner-c"},
      {"id":"C4","implemented":True,"evidence":"contradictory","owner":"owner-d"}]
    closed=[c["id"] for c in controls if c["implemented"] and c["evidence"]=="current_test" and c["owner"]]
    rejected=[c for c in controls if c["id"] not in closed]
    return {"controls":len(controls),"validly_closed":closed,
      "unsubstantiated_not_closed":[c["id"] for c in rejected],
      "false_closures_prevented":sum(c["evidence"] in {"expired_policy","contradictory","none"} for c in rejected),
      "coverage":round(len(closed)/len(controls),4)}

def run_all():
    labs={"LAB-FND-01A":lab01_authorization(),"LAB-FND-02A":lab02_asset_reconciliation(),
      "LAB-FND-03A":lab03_threat_model(),"LAB-FND-04A":lab04_identity(),
      "LAB-FND-05A":lab05_crypto_integrity(),"LAB-FND-06A":lab06_event_reconstruction(),
      "LAB-FND-07A":lab07_assurance()}
    checks={"authz_revocation":labs["LAB-FND-01A"]["revoked_access_denied"],
      "asset_stable_id_beats_hostname":labs["LAB-FND-02A"]["stable_resource_id"]["f1"]>=labs["LAB-FND-02A"]["hostname_baseline"]["f1"],
      "threat_paths_represented":labs["LAB-FND-03A"]["paths_found"]==labs["LAB-FND-03A"]["required_paths"],
      "identity_negative_tests":labs["LAB-FND-04A"]["all_expected"],
      "crypto_tamper_rejected":labs["LAB-FND-05A"]["tamper_rejected"],
      "timeline_ordered":labs["LAB-FND-06A"]["chronological"],
      "assurance_stale_evidence_rejected":"C2" in labs["LAB-FND-07A"]["unsubstantiated_not_closed"]}
    return {"schema_version":"1.0.0","seed":20261119,"synthetic_only":True,
            "checks":checks,"all_checks_passed":all(checks.values()),"labs":labs}

if __name__=="__main__": print(json.dumps(run_all(),indent=2,sort_keys=True))
