#!/usr/bin/env python3
"""Join every source into one row per model: data/consolidated_39_models.csv"""
import json, re, os, csv, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, "raw"); DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from decode import payloads, grab, read_text, read_json  # noqa: E402

aa = {m["slug"]: m for m in read_json(os.path.join(RAW, "aa_models.json.gz"))}
s, _ = payloads(os.path.join(RAW, "aa_coding_agents.html"))
ca = [x for x in grab(s, "benchmarkRows") or [] if isinstance(x, dict)]
s2, _ = payloads(os.path.join(RAW, "benchlm_leaderboard.html"))
bl = {r[2]: r for r in grab(s2, "rows") or [] if isinstance(r, list) and len(r) > 29}
s3, _ = payloads(os.path.join(RAW, "openrouter_rankings.html"))
intel, cod, ag = grab(s3, "intelligence"), grab(s3, "coding"), grab(s3, "agentic")
def hk(r): return r.get("heuristic_openrouter_slug") or (r.get("permaslug") or "").split("-20")[0]
def ork(lst, slug):
    """Look up a model on an OpenRouter board.

    Substring matching is unsafe here: 'claude-sonnet-5' is a prefix of
    'claude-sonnet-5-5', so a naive match gives Claude Sonnet 5 the score of
    Claude Sonnet 5.5. Exact slug equality wins; substring is a last resort
    and only when it is unambiguous.
    """
    lst = lst or []
    for i, r in enumerate(lst, 1):
        if hk(r) == slug: return i, r.get("score")
    for i, r in enumerate(lst, 1):
        if slug.split("/")[-1] == hk(r).split("/")[-1]: return i, r.get("score")
    tail = slug.split("/")[-1]
    hits = [(i, r) for i, r in enumerate(lst, 1) if tail in hk(r)]
    if len(hits) == 1: return hits[0][0], hits[0][1].get("score")
    return None, None

def arena_parse(path):
    lines = read_text(path).split("\n"); recs = []
    for i, l in enumerate(lines):
        m = re.fullmatch(r"(\d{3,4})", l.strip())
        if not m: continue
        score = int(m.group(1)); model = None
        for k in range(i-1, max(-1, i-14), -1):
            sx = lines[k].strip()
            if not sx or re.fullmatch(r"[\d\s±]*", sx): continue
            if "(" in sx and model is None: model = sx; break
        if model and score >= 960: recs.append((model, score))
    out, seen = [], set()
    for r in recs:
        if r[0] in seen: continue
        seen.add(r[0]); out.append(r)
    return out
ar = arena_parse(os.path.join(RAW, "arena_text_leaderboard.md.gz"))
def base(m):
    """'Claude Sonnet 5.5 (xHigh)' -> 'claude sonnet 5.5'"""
    return re.sub(r"\s*\(.*$", "", m).strip().lower()

def amatch(name):
    """Match a model label to its Arena row, preferring exact base-name equality.

    Substring matching alone is wrong: 'Claude Sonnet 5' is a prefix of
    'Claude Sonnet 5.5', so a naive match assigns 5.5's score to 5.
    """
    want = base(name)
    for i, (m, sc) in enumerate(ar, 1):
        if base(m) == want: return i, sc
    for i, (m, sc) in enumerate(ar, 1):
        if want in base(m): return i, sc
    return None, None

MODELS = [
 ("Claude Sonnet 5.5","anthropic/claude-sonnet-5.5",["claude-sonnet-5-5"],"claude-sonnet-5-5"),
 ("Claude Sonnet 5","anthropic/claude-sonnet-5",[], "claude-sonnet-5"),
 ("GPT-6 Sol Pro","openai/gpt-6-sol-pro",["gpt-6-sol-daybreak-blue"],"gpt-6-sol"),
 ("GPT-6.1 Sol","openai/gpt-6.1-sol",["gpt-6-1-sol"],"gpt-6.1-sol"),
 ("GPT-6 Astra","openai/gpt-6-astra",["gpt-6-astra"],"gpt-6-astra"),
 ("GPT-6 Luna","openai/gpt-6-luna",["gpt-6-luna"],"gpt-6-luna"),
 ("Gemini 4 Argon","google/gemini-4-argon",["gemini-4-argon"],"gemini-4-argon"),
 ("Gemini 3.8 Flash","google/gemini-3.8-flash",["gemini-3-8-flash"],"gemini-3.8-flash"),
 ("Muse Wonder","meta/muse-wonder",["muse-wonder"],"muse-wonder"),
 ("Muse Wonder Full","meta/muse-wonder-full",["muse-wonder-full"],"muse-wonder-full"),
 ("Muse Spark 1.3","meta/muse-spark-1.3",["muse-spark-open"],"muse-spark-1.3"),
 ("Muse Spark Open","meta/muse-spark-open",["muse-spark-open"],"muse-spark-1.3"),
 ("GLM-5.3","z-ai/glm-5.3",["glm-5-3"],"glm-5-3"),
 ("GLM-5.3-Flash","z-ai/glm-5.3-flash",["glm-5-3-flash"],"glm-5-3-flash"),
 ("GLM-5.2","z-ai/glm-5.2",[],"glm-5-2"),
 ("GLM-4.7","z-ai/glm-4.7",[],"glm-4-7"),
 ("GLM-4.7-Flash","z-ai/glm-4.7-flash",[],"glm-4-7-flash"),
 ("MiMo-V2.6-Pro","xiaomi/mimo-v2.6-pro",["mimo-v2-6-pro"],"mimo-v2.6-pro"),
 ("MiMo-V2.6-Flash","xiaomi/mimo-v2.6-flash",["mimo-v2-6-flash"],"mimo-v2.6-flash"),
 ("MiMo-V2.5","xiaomi/mimo-v2.5",[],"mimo-v2.5"),
 ("Qwen3.8 Max","qwen/qwen3.8-max",["qwen3-8-max"],"qwen3.8-max"),
 ("Qwen3.8-Flash","qwen/qwen3.8-flash",["qwen3-8-flash-next"],"qwen3.8-flash-next"),
 ("DeepSeek V4.1 Flash","deepseek/deepseek-v4.1-flash",["deepseek-v4-1-flash-1017"],"deepseek-v4.1-flash"),
 ("Step 5 Preview","stepfun/step-5",["step-5"],"step-5"),
 ("Step 3.7 Flash","stepfun/step-3.7-flash",[],"step-3.7-flash"),
 ("MiniMax-M3.1-Flash","minimax/minimax-m3.1-flash",["minimax-m3-1-flash"],"minimax-m3.1-flash"),
 ("MiniMax-M3","minimax/minimax-m3",["minimax-m3"],"minimax-m3"),
 ("Ling 3.1 Flash","inclusionai/ling-3.1-flash",["ling-3-1-flash"],"ling-3.1-flash"),
 ("Ling 3.0 Flash VL","inclusionai/ling-3.0-flash-vl",["ling-3-0-flash-vl"],"ling-3.0-flash-vl"),
 ("Hy3","tencent/hy3",["hy3"],"hy3"),
 ("Hy4 preview","tencent/hy4-preview",[],"hy4-preview"),
 ("Nemotron 3 Super","nvidia/nemotron-3-super-120b-a12b",[],"nemotron-3-super"),
 ("Nemotron 3 Ultra","nvidia/nemotron-3-ultra-550b-a55b",["nvidia-nemotron-3-ultra-550b-a55b"],"nemotron-3-ultra"),
 ("Nemotron 3 Nano 30B","nvidia/nemotron-3-nano-30b-a3b",["nvidia-nemotron-3-nano-30b-a3b-reasoning"],"nemotron-3-nano"),
 ("Inkling","thinkingmachines/inkling",["inkling"],"inkling"),
 ("Grok Build 0.1","x-ai/grok-build-0.1",[],None),
 ("Mistral Large 4","mistralai/mistral-large-4",["mistral-large-4"],"mistral-large-4"),
 ("gpt-oss-120b","openai/gpt-oss-120b",["gpt-oss-120b"],"gpt-oss-120b"),
 ("gpt-oss-20b","openai/gpt-oss-20b",["gpt-oss-20b"],"gpt-oss-20b"),
 ("Muse Glimmer 30B","meta/muse-glimmer-30b",["muse-glimmer"],"muse-glimmer-30b"),
 ("Dots-3 Note","dots-studio/dots-3-note-preview",[],None),
 ("Fugu Max","sakana/fugu-max",[],None),
 ("Beam 1.0","reflection/beam-1.0-501b-a23b",["reflection-beam"],"reflection-beam"),
 ("Nex-N2.5-Pro","nex-agi/nex-n2.5-pro",["nex-n2-pro"],None),
 ("Nex-N2.5-Mini","nex-agi/nex-n2.5-mini",[],None),
]
HARNESS = {"Claude Sonnet 5.5":("Claude Code","Sonnet 5.5 (xhigh)",62.9),
 "GPT-6 Sol Pro":("Codex","GPT-6 Sol (max)",56.7), "GPT-6.1 Sol":("Codex","GPT-6.1 Sol (xhigh)",62.9),
 "GPT-6 Astra":("Devin Fusion CLI","GPT-6 Astra xHigh + SWE-2",58.9),
 "Gemini 3.8 Flash":("Antigravity SDK","Gemini 3.8 Flash (high)",41.9),
 "Muse Wonder":("Muse Code","Muse Wonder Full (max)",68.0), "Muse Wonder Full":("Muse Code","Muse Wonder Full (max)",68.0),
 "Muse Spark 1.3":("Muse Code","Muse Spark 1.3 (max)",54.3), "GLM-5.3":("Opencode","GLM-5.3",53.6),
 "Qwen3.8 Max":("Claude Code","Qwen3.8 Max",43.3), "Step 5 Preview":("Claude Code","Step 5 Preview",51.2),
 "Grok Build 0.1":("Grok Build","Grok 4.6 (xhigh)",47.0), "Beam 1.0":("Mirror","Beam 1.0",27.7)}
rows = []
for label, orslug, aaslugs, blslug in MODELS:
    a = next((aa[x] for x in aaslugs if x in aa), None)
    oi, ois = ork(intel, orslug); oc, ocs = ork(cod, orslug); oa, oas = ork(ag, orslug)
    b = bl.get(blslug) if blslug else None
    ar_r, ar_sc = amatch(label)
    h = HARNESS.get(label)
    rows.append({"model": label, "openrouter_id": orslug,
        "aa_intelligence_index": a.get("intelligenceIndex") if a else None,
        "aa_gdpval": a.get("gdpvalNormalized") if a else None,
        "aa_terminalbench_4_0": a.get("terminalBench40") if a else None,
        "aa_tau2_tooluse": a.get("tau2") if a else None,
        "aa_longctx_reasoning": a.get("lcr") if a else None,
        "aa_nonhallucination": a.get("omniscienceNonHallucination") if a else None,
        "aa_context_tokens": a.get("contextWindowTokens") if a else None,
        "or_intelligence_rank": oi, "or_intelligence_score": ois,
        "or_coding_rank": oc, "or_coding_score": ocs,
        "or_agentic_rank": oa, "or_agentic_score": oas,
        "benchlm_capability": b[26] if b else None,
        "arena_text_rank": ar_r, "arena_text_score": ar_sc,
        "aa_harness": h[0] if h else None, "aa_harness_model": h[1] if h else None,
        "aa_harness_index": h[2] if h else None})
p = os.path.join(DATA, "consolidated_39_models.csv")
with open(p, "w", newline="") as f:
    cw = csv.DictWriter(f, fieldnames=list(rows[0].keys())); cw.writeheader(); cw.writerows(rows)
print(f"  consolidated_39_models.csv: {len(rows)} rows")
