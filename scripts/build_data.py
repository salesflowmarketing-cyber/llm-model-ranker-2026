#!/usr/bin/env python3
"""Regenerate every CSV in data/ from the cached raw payloads in raw/.
Usage: python3 scripts/build_data.py   (run from the repo root)"""
import json, re, os, csv, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, "raw")
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from decode import payloads, grab   # noqa: E402

def read_text(path):
    """Read a text file, transparently handling .gz."""
    import gzip
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh: return fh.read()
    with open(path, encoding="utf-8", errors="replace") as fh: return fh.read()

def read_json(path):
    import json as _json
    return _json.loads(read_text(path))

def w(name, rows, fields):
    p = os.path.join(DATA, name)
    with open(p, "w", newline="") as f:
        cw = csv.DictWriter(f, fieldnames=fields); cw.writeheader(); cw.writerows(rows)
    print(f"  {name}: {len(rows)} rows")

# ---------- 1. Artificial Analysis: all 271 models, every per-eval score ----------
ms = read_json(os.path.join(RAW, "aa_models.json.gz"))
rows = []
for m in ms:
    rows.append({"slug": m["slug"], "name": m["name"], "creator": m.get("modelCreatorName"),
        "release_date": m.get("releaseDate"), "params": m.get("parameters"),
        "open_weights": m.get("isOpenWeights"), "reasoning": m.get("isReasoning"),
        "context_tokens": m.get("contextWindowTokens"), "intelligence_index": m.get("intelligenceIndex"),
        "intelligence_estimated": m.get("intelligenceIndexIsEstimated"),
        "gdpval_normalized": m.get("gdpvalNormalized"), "analyst_agent": m.get("analystAgent"),
        "terminalbench_hard": m.get("terminalbenchHard"), "terminalbench_2_1": m.get("terminalBench21"),
        "terminalbench_4_0": m.get("terminalBench40"), "tau2": m.get("tau2"), "tau3_banking": m.get("tauBanking"),
        "long_context_reasoning": m.get("lcr"), "hle": m.get("hle"), "gpqa": m.get("gpqa"),
        "scicode": m.get("scicode"), "ifbench": m.get("ifbench"), "critpt": m.get("critpt"),
        "apex_agents": m.get("apexAgents"), "itbench_sre": m.get("itbenchSre"), "mmmu_pro": m.get("mmmuPro"),
        "omniscience": m.get("omniscience"), "omniscience_accuracy": m.get("omniscienceAccuracy"),
        "non_hallucination": m.get("omniscienceNonHallucination"),
        "price_1m_input": m.get("price1mInputTokens"), "price_1m_output": m.get("price1mOutputTokens")})
w("aa_leaderboard_271.csv", rows, list(rows[0].keys()))

# ---------- 2. AA coding-agent leaderboard: model x harness ----------
s, _ = payloads(os.path.join(RAW, "aa_coding_agents.html"))
rows = []
for r in grab(s, "benchmarkRows"):
    if not isinstance(r, dict): continue
    ev = {e["datasetIndexName"]: e for e in r.get("evals", [])}
    saf = [(e.get("safety") or {}) for e in r.get("evals", [])]
    def rew(k):
        return ((ev.get(k, {}).get("mean") or {}).get("reward"))
    def tok(k, f):
        return ((ev.get(k, {}).get("mean") or {}).get(f))
    rows.append({"agent": r.get("agentName"), "model": (r.get("display") or {}).get("model"),
        "label": r.get("displayLabel"), "index_score": r.get("indexScore"),
        "deepswe_v1_1": rew("deep-swe-v1.1"), "swe_atlas_qna": rew("swe-atlas-qna"),
        "terminalbench_v4": rew("terminal-bench-v4"),
        "input_tokens": sum(tok(k, "inputTokens") or 0 for k in ("deep-swe-v1.1","swe-atlas-qna","terminal-bench-v4")),
        "output_tokens": sum(tok(k, "outputTokens") or 0 for k in ("deep-swe-v1.1","swe-atlas-qna","terminal-bench-v4")),
        "refusals": sum(x.get("refusedAttemptCount") or 0 for x in saf),
        "hard_stops": sum(x.get("hardStopAttemptCount") or 0 for x in saf),
        "attempts": sum(x.get("attemptCount") or 0 for x in saf)})
rows.sort(key=lambda x: -(x["index_score"] or -1))
w("aa_coding_agents.csv", rows, list(rows[0].keys()))

# ---------- 3. OpenRouter: intelligence / coding / agentic boards ----------
s, _ = payloads(os.path.join(RAW, "openrouter_rankings.html"))
def hk(r): return r.get("heuristic_openrouter_slug") or (r.get("permaslug") or "").split("-20")[0]
rows = []
for board, key in (("intelligence","intelligence"),("coding","coding"),("agentic","agentic")):
    lst = grab(s, key)
    for i, r in enumerate(lst or [], 1):
        rows.append({"board": board, "rank": i, "name": r.get("aa_name"), "score": r.get("score"),
                     "openrouter_slug": r.get("heuristic_openrouter_slug"), "permaslug": r.get("permaslug")})
w("openrouter_boards.csv", rows, list(rows[0].keys()))

# ---------- 4. benchlm per-axis ranks ----------
rows = []
for fn in sorted(os.listdir(os.path.join(RAW, "benchlm_models"))):
    if not (fn.endswith(".html") or fn.endswith(".html.gz")): continue
    slug = fn[:-8] if fn.endswith(".gz") else fn[:-5]
    s, _ = payloads(os.path.join(RAW, "benchlm_models", fn))
    vals = {v["axis"]: v.get("value") for v in (grab(s, "values") or []) if isinstance(v, dict) and "axis" in v}
    rk = {r["category"]: r for r in (grab(s, "rankData") or []) if isinstance(r, dict)}
    dec = {d["key"]: d.get("value") for d in (grab(s, "decisionStats") or []) if isinstance(d, dict)}
    row = {"slug": slug, "capability_score": dec.get("capability"), "price_input": dec.get("price"),
           "tokens_per_second": dec.get("speed"), "context": dec.get("context")}
    for axis in ("Agentic","Coding","Reasoning","Multimodal","Knowledge","Multilingual","Instruction following","Math"):
        row[f"{axis.lower().replace(' ','_')}_value"] = vals.get(axis)
        r = rk.get(axis if axis != "Instruction following" else "Inst. Following")
        row[f"{axis.lower().replace(' ','_')}_rank"] = r.get("rank") if r else None
        row[f"{axis.lower().replace(' ','_')}_n"]  = r.get("total") if r else None
    rows.append(row)
w("benchlm_axes.csv", rows, list(rows[0].keys()))

# ---------- 5. llm-stats metadata ----------
s, _ = payloads(os.path.join(RAW, "llmstats.html"))
rows = []
for m in (grab(s, "initialHomepageLLMModels") or []):
    a = m.get("arena_scores") or {}
    rows.append({"model_id": m.get("model_id"), "name": m.get("name"), "organization": m.get("organization"),
        "gpqa": m.get("gpqa_score"), "swe_bench_verified": m.get("swe_bench_verified_score"),
        "hle": m.get("hle_score"), "context": m.get("context"), "params": m.get("param_count"),
        "price_input": m.get("input_price"), "price_output": m.get("output_price"),
        "throughput_tps": m.get("throughput"), "open_source": m.get("is_open_source"),
        "release_date": m.get("release_date"), "arena_chat": a.get("chat-arena"), "arena_coding": a.get("coding-arena")})
w("llmstats.csv", rows, list(rows[0].keys()))

# ---------- 6. OpenRouter model specs (context / modalities / pricing / variants) ----------
d = read_json(os.path.join(RAW, "openrouter_models.json.gz"))["data"]
rows = []
for m in d:
    arch = m.get("architecture") or {}
    rows.append({"id": m.get("id"), "name": m.get("name"), "created": m.get("created"),
        "context_length": m.get("context_length"),
        "input_modalities": ",".join(arch.get("input_modalities") or []),
        "output_modalities": ",".join(arch.get("output_modalities") or []),
        "modality_transforms": json.dumps(arch.get("modality_transforms") or {}),
        "pricing_in": (m.get("pricing") or {}).get("prompt"),
        "pricing_out": (m.get("pricing") or {}).get("completion"),
        "params": m.get("parameters"), "open_weights": arch.get("open_weights"),
        "is_variant": m.get("is_moderated") is None or ":free" in (m.get("id") or "") or ":free" in (m.get("id") or ""),
        "description": (m.get("description") or "")[:400].replace("\n", " ")})
w("openrouter_model_specs.csv", rows, list(rows[0].keys()))

# ---------- 7. OpenRouter variant taxonomy ----------
rows = [{"variant": v, "kind": k, "source": s}
        for v, k, s in [
        (":free","catalog","separate model entry in /api/v1/models with its own price/context"),
        (":batch","catalog","batch-priced variant for the Batch API"),
        (":thinking","routing","enables interleaved thinking on providers that support it"),
        (":nitro","routing","sorts providers by throughput"),
        (":floor","routing","sorts providers by price"),
        (":exacto","routing","sorts providers by tool-calling reliability"),
        (":online","routing","deprecated - web results prepended to the prompt"),
        (":cloud","INVALID","not a documented OpenRouter variant - will 404")]]
w("openrouter_variants.csv", rows, list(rows[0].keys()))
print("done")

# ---------- 8. Arena Text Arena (human-preference votes) ----------
def arena_parse(path):
    t = read_text(path); lines = t.split("\n"); recs = []
    for i, l in enumerate(lines):
        m = re.fullmatch(r"(\d{3,4})", l.strip())
        if not m: continue
        score = int(m.group(1)); ci = None
        for k in range(i+1, min(i+5, len(lines))):
            mm = re.search(r"±(\d+)", lines[k])
            if mm: ci = int(mm.group(1)); break
        model = None; org = None
        for k in range(i-1, max(-1, i-14), -1):
            sx = lines[k].strip()
            if not sx or re.fullmatch(r"[\d\s±]*", sx): continue
            if "·" in sx and model is None: org = sx; continue
            if "(" in sx and model is None: model = sx; break
            if model is not None: break
        votes = None; price = None; ctx = None
        for k in range(i+1, min(i+12, len(lines))):
            for tok in re.split(r"\t+", lines[k].strip()):
                tok = tok.strip()
                if not tok: continue
                if re.fullmatch(r"[\d,]{3,}", tok) and votes is None: votes = int(tok.replace(",", ""))
                elif tok.startswith("$") and price is None: price = tok
                elif (tok.endswith("M") or tok.endswith("K")) and ctx is None: ctx = tok
        if model and score >= 960: recs.append({"model": model, "org": org, "score": score,
                                               "ci90": ci, "votes": votes, "price": price, "context": ctx})
    out = []; seen = set()
    for r in recs:
        if r["model"] in seen: continue
        seen.add(r["model"]); out.append(r)
    return out
ar = arena_parse(os.path.join(RAW, "arena_text_leaderboard.md.gz"))
for i, r in enumerate(ar, 1): r["rank"] = i
w("arena_text_leaderboard.csv", ar, list(ar[0].keys()))
print(f"  arena_text_leaderboard.csv: {len(ar)} models parsed")
