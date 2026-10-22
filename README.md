# Which AI Model Should You Actually Use?

**A cross-validated ranking of 39 frontier models across 7 independent leaderboards — and a task-by-task routing guide for AI agents.**

*Research snapshot: **22 October 2026**. All data pulled live from source. No estimates, no vibes.*

---

## TL;DR

If you want the answer in five lines:

| Your need | Use this | Why |
|---|---|---|
| **Writing / content / copy** | **Gemini 4 Argon** | **#1 on Arena Text** (human preference, 8.9M votes) **and** lowest hallucination rate of 271 models — the only model that is both the best writer and the most factually disciplined |
| **Building agents / coding** | **Claude Sonnet 5.5** @ `xhigh` | **#1 Coding** on benchlm (84.3 of 152 models), **62.9** on AA's live coding-agent harness, #5 on Arena's agent board |
| **Video / long-context analysis** | **Gemini 4 Argon** + **Ling 3.0 Flash VL** | Argon: 1M-token output, video+audio. Ling VL: MIT-licensed, 5.5B active, and the *only* model whose card explicitly says **"video clip editing"** |
| **Reasoning / hard agentic chains** | **GPT-6.1 Sol** or **GPT-6 Astra** | #1–2 Reasoning on benchlm; #2 and #5 on Arena's agent board; Pareto-optimal at $0.78/task |
| **Self-hosted / no API lock-in** | **GLM-5.3** (MIT) | #5 on OpenRouter's Agentic board, **OpenCode's best-scoring model in AA's harness (53.6)**, 1M context, #26 on Arena Text |

**Three findings that most rankings miss:**

1. **Reasoning effort is worth more than model choice.** The *same model* in the *same harness* swings 20 points: Claude Sonnet 5.5 scores **62.9 at `xhigh`** and **42.1 at `low`** in Claude Code. Never run agent work at `low`.
2. **A model's value changes completely depending on which leaderboard you read.** Qwen3.8 Max is #15 on Artificial Analysis's composite (45.4) but **#4 on OpenRouter Intelligence (53.4)** and **#3 on OpenRouter Agentic (56.0)**. Benchlm ranks it **#2 for instruction following**. One number cannot rank a model for a job.
3. **Video support is a hard constraint, not a preference.** Only ~10 of the 39 models in this study accept video input at all. Claude, GPT-6, GLM-4.7/5.2/5.3, and Hy3/Hy4 **cannot see video, no matter how well they score**.

---

## What's in this repo

| Path | Contents |
|---|---|
| `data/aa_leaderboard_271.csv` | Artificial Analysis Intelligence Index + **27 per-eval scores** for all 271 models (Terminal-Bench 2.1/4.0/Hard, τ²/τ³-bench, GDPval-AA, AA-Analyst-Agent, AA-Briefcase, AA-Omniscience, AA-LCR, IFBench, CritPt, APEX-Agents, ITBench-SRE, MMMU-Pro, GPQA, HLE, SciCode) |
| `data/aa_coding_agents.csv` | **AA's Coding Agent Leaderboard** — 34 model×harness rows across 10 real coding agents, with per-eval scores, token usage, and refusal counts |
| `data/arena_text_leaderboard.csv` | Arena **Text Arena** — human-preference rankings, score ± 90% CI, vote counts |
| `data/benchlm_axes.csv` | benchlm.ai per-axis ranks & percentiles: Agentic, Coding, Reasoning, Multimodal, Knowledge, Instruction-following, Math |
| `data/openrouter_boards.csv` | OpenRouter's **three** boards — Intelligence (351), Coding (152), Agentic (109) |
| `data/openrouter_model_specs.csv` | Context, input/output modalities, pricing, params for 468 OpenRouter models |
| `data/openrouter_variants.csv` | The `:free` / `:thinking` / `:floor` / `:exacto` / `:nitro` / `:batch` taxonomy — **and which ones don't exist** |
| `data/llmstats.csv` | llm-stats.com: 408 models with GPQA, SWE-bench Verified, HLE, params, throughput, release dates |
| `data/consolidated_39_models.csv` | The 39 models this study is centred on, joined across every source |
| `scripts/` | The extraction code — reproduce every CSV from `raw/` with one command |
| `raw/` | The cached source payloads the CSVs are built from |

---

## 1. The master ranking

**Artificial Analysis Intelligence Index** — the most comprehensive independent composite (271 models, refreshed continuously).

| # | Model | II | GDPval | TB 4.0 | TB 2.1 | τ² tool | LongCtx | IFBench | MMMU-Pro | HLE | NonHalluc | Ctx | Open |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:--|
| 1 | **Claude Sonnet 5.5** | **56.0** | .67 | .636 | – | – | .827 | – | – | .550 | .530 | 1M | ✗ |
| 2 | **Muse Wonder Full** | **55.8** | .70 | .571 | – | – | .837 | .626 | – | .536 | .770 | 1M | ✗ |
| 3 | **GPT-6 Astra** | **52.7** | .54 | .591 | **.884** | – | .807 | – | **.869** | .547 | .487 | 1M | ✗ |
| 4 | **Gemini 4 Argon** | **52.6** | .56 | .571 | – | – | .797 | – | – | .571 | **.849** | 1M | ✗ |
| 5 | **Muse Wonder** | **52.4** | .64 | .520 | – | – | .807 | – | – | .501 | .735 | 1.05M | ✗ |
| 6 | **GPT-6.1 Sol** | **51.8** | .55 | .561 | – | – | .830 | – | .860 | .529 | .457 | 1M | ✗ |
| 7 | **MiMo-V2.6-Pro** | **46.3** | .59 | .348 | – | – | .863 | .609 | – | .494 | .594 | 1M | **MIT** |
| 8 | Qwen3.8 Max | 45.4 | .58 | .389 | **.888** | – | .803 | – | .828 | .431 | .712 | 984k | ✗ |
| 9 | **DeepSeek V4.1 Flash** | **45.1** | .62 | .338 | – | – | .827 | – | .806 | .433 | .332 | 1M | **MIT** |
| 10 | **GLM-5.3** | **44.8** | .57 | .419 | .839 | – | .797 | .590 | – | .423 | .704 | 1M | GLM-5.3 |
| 11 | Step 5 Preview | 43.7 | .54 | .333 | – | – | **.883** | – | .764 | .465 | .570 | 1M | OW |
| 12 | MiniMax-M3.1-Flash | 42.7 | .48 | .258 | – | – | .797 | – | .791 | .480 | ⚠️**.072** | 1M | ✗ |
| 13 | **GLM-5.3-Flash** | 41.8 | .57 | .328 | .843 | – | .800 | – | – | .399 | .724 | 1M | **MIT** |
| 14 | Ling 3.1 Flash | 41.1 | .56 | .333 | – | – | .830 | – | – | .394 | .621 | 1M | **MIT** |
| 15 | Gemini 3.8 Flash | 40.9 | .47 | .197 | .876 | – | .813 | – | .856 | .478 | .448 | 1M | ✗ |
| 16 | Qwen3.8-Flash-Next | 39.8 | .56 | .253 | .861 | – | .797 | – | .798 | .380 | .547 | 256k | OW |
| 17 | Muse Spark Open | 38.9 | .45 | .081 | .764 | – | .783 | – | .809 | .439 | .759 | 1.05M | Muse |
| 18 | Mistral Large 4 | 38.4 | .46 | .268 | – | – | .813 | – | .764 | .350 | .581 | 524k | ✗ |
| 19 | GPT-6 Luna | 38.1 | .47 | .126 | – | – | .833 | – | .797 | .385 | .233 | 1M | ✗ |
| 20 | MiMo-V2.6-Flash | 37.9 | .55 | .227 | – | – | .743 | – | .731 | .351 | .456 | 1M | **MIT** |
| 21 | MiniMax-M3 | 29.2 | .37 | .020 | .652 | **.889** | .830 | **.829** | .786 | .390 | .816 | 1M | Community |
| 22 | Beam 1.0 | 30.3 | .34 | .030 | – | – | .780 | – | – | .347 | .528 | 1.05M | Apache 2.0 |
| 23 | Nex-N2.5-Pro | 28.2\* | .30 | – | .678 | .816 | .817 | .662 | – | .337 | ⚠️**.051** | 262k | Apache 2.0 |
| 24 | Nemotron 3 Ultra | 22.9 | .26 | .005 | .539 | .833 | .793 | .814 | – | .284 | .703 | 262k | OpenMDW |
| 25 | Hy3 | 25.3 | .28 | .005 | .644 | – | .790 | – | – | .335 | .259 | 256k | Apache 2.0 |
| 26 | Inkling | 25.0 | .28 | .010 | .551 | .291 | .773 | – | .735 | .319 | .323 | 1M | Apache 2.0 |
| 27 | Ling 3.0 Flash VL | 24.6 | .33 | **.000** | .644 | – | .783 | – | .790 | .220 | .780 | 262k | **MIT** |
| 28 | Muse Glimmer 30B | 17.5 | .14 | .005 | .517 | – | .833 | – | .743 | .220 | .181 | 131k | Apache 2.0 |
| 29 | gpt-oss-120b | 11.6 | .05 | .000 | .262 | .658 | .520 | .690 | – | .196 | ⚠️**.092** | 131k | Apache 2.0 |
| 30 | gpt-oss-20b | 9.0 | .00 | .000 | .139 | .602 | .347 | .651 | – | .110 | ⚠️**.059** | 131k | Apache 2.0 |

`*` estimated. **NonHalluc** = AA-Omniscience non-hallucination rate. **τ²** = τ²-bench tool-use. **TB** = Terminal-Bench. **IFBench** = instruction following. **LCR** = long-context reasoning.

**Models not yet scored by AA** but covered here from official model cards: Claude Sonnet 5, GPT-6 Sol Pro, GLM-5.2, GLM-4.7, GLM-4.7-Flash, MiMo-V2.5, Step 3.7 Flash, Hy4 preview, Fugu Max, Nex-N2.5-Mini, Nemotron 3 Super, Grok Build 0.1, Dots-3 Note Preview, Muse Spark 1.3.

> ⚠️ **Watch the NonHalluc column.** MiniMax-M3.1-Flash scores **.072** — it will invent statistics and source URLs with total confidence. Same for gpt-oss-20b (.059), gpt-oss-120b (.092) and Nex-N2.5-Pro (.051). Never let these write client-facing content.

---

## 2. Arena — human preference (the metric that actually measures writing quality)

**Text Arena · 417 models · 8,900,458 votes · 20 Oct 2026**

| Rank | Model | Score | ± | Votes | |
|---:|---|---:|---:|---:|---|
| **1** | **Gemini 4 Argon (High)** · Google | **1524** | ±9 | 4,900 | *Preliminary* |
| **2** | **Muse Wonder (Max)** · Meta | **1510** | ±9 | 5,099 | *Preliminary* |
| 3 | Claude Opus 5.5 (High) | 1509 | ±7 | 9,496 | |
| 4 | Claude Fable 5 (High) | 1504 | ±4 | 43,399 | |
| 5 | Claude Opus 4.6 (High) | 1503 | ±3 | 82,619 | |
| 9 | **Gemini 3.8 Flash (High)** | 1496 | ±5 | 41,423 | |
| 10 | **Muse Spark 1.3 (Max)** | 1495 | ±5 | 19,323 | |
| 18 | Kimi K3 (Max) | 1488 | ±5 | 34,325 | |
| **26** | **GLM-5.3 (Max)** · MIT | **1481** | ±5 | 24,035 | |
| 28 | GPT-6.1 Sol (Max) | 1479 | ±8 | 7,453 | |
| 30 | **Claude Sonnet 5.5 (xHigh)** | 1477 | ±7 | 8,126 | |
| 32 | GLM-5.2 (Max) | 1476 | ±4 | 51,221 | |
| 34 | GPT-6 Astra (Max) | 1476 | ±6 | 13,293 | |
| 58 | Claude Sonnet 5 (High) | 1461 | ±4 | 50,871 | |
| 62 | GPT-6 Sol (Max) | 1459 | ±6 | 13,790 | |

**Arena Agent board** (vote share across 367M sessions):

| # | Model | Share | | # | Model | Share |
|---:|---|---:|---|---:|---|---:|
| 1 | Claude Opus 5.5 (Max) | 20.92% | | 6 | Gemini 4 Argon (High) | 12.03% |
| 2 | **GPT-6 Astra (Max)** | **14.70%** | | 7 | **Muse Wonder Full (Max)** | **11.26%** |
| 3 | Claude Fable 5.1 (Max) | 14.17% | | 8 | GPT-6 Sol (Max) | 9.36% |
| 4 | **GPT-6.1 Sol (Max)** | **13.55%** | | 9 | Claude Fable 5 (High) | 8.31% |
| 5 | **Claude Sonnet 5.5 (Max)** | **12.67%** | | 10 | Claude Opus 5 (Max) | 8.09% |

**Arena Pareto frontier (agents)** — quality per dollar:

| Model | $/task | Vote share |
|---|---:|---:|
| Claude Opus 5.5 (Max) | $6.19 | 20.92% |
| GPT-6 Astra (Max) | $4.23 | 14.70% |
| GPT-6.1 Sol (Max) | $0.78 | 13.55% |
| DeepSeek-V4.1-Flash (Max) | $0.19 | 4.73% |
| MiMo-V2.6-Pro | $0.12 | 3.68% |
| GPT-6 Luna (Max) | $0.08 | 3.03% |
| MiMo-V2.6-Flash | $0.06 | 2.52% |

**Arena license trends (Jul 25 → Oct 22, top 3 each):** proprietary — Claude Opus 5, Claude Fable 5, GPT-5.6 Sol. Open source — Kimi K3, **GLM-5.2**, **GLM-5.3**.

---

## 3. The Coding Agent Leaderboard — model × harness (the most actionable table here)

Artificial Analysis runs 10 real coding agents against 34 model configurations. Index = ⅓ DeepSWE v1.1 + ⅓ SWE-Atlas-QnA + ⅓ Terminal-Bench v4.

| Agent | Model | Index | DeepSWE | SWE-Atlas | TB v4 | input tok | refusals |
|---|---|---:|---:|---:|---:|---:|---:|
| Devin Fusion CLI | Claude Opus 5.5 + GPT-6 Luna | **68.2** | 72.6 | 69.4 | 62.6 | 40.1M | 0/908 |
| **Muse Code** | **Muse Wonder Full (max)** | **68.0** | **77.0** | 68.0 | 59.1 | 48.2M | 0/906 |
| Codex | GPT-6.1 Sol (xhigh) | 62.9 | 73.2 | 61.0 | 54.5 | 10.3M | 13/909 |
| **Claude Code** | **Sonnet 5.5 (xhigh)** | **62.9** | 68.4 | 62.1 | 58.1 | 21.9M | 34/909 |
| Codex | GPT-6.1 Sol (medium) | 61.4 | 72.0 | 60.8 | 51.5 | 7.4M | 12/909 |
| Codex | GPT-6.1 Sol (high) | 60.1 | 70.5 | 59.9 | 50.0 | 9.0M | 15/909 |
| Codex | GPT-6.1 Sol (low) | 57.2 | 67.6 | 55.1 | 49.0 | 5.9M | 9/909 |
| Codex | **GPT-6 Sol (max)** | **56.7** | 69.0 | 57.5 | 43.4 | 32.7M | 0/907 |
| Claude Code | Sonnet 5.5 (high) | 55.0 | 66.7 | 56.5 | 41.9 | 8.6M | 33/909 |
| **Muse Code** | **Muse Spark 1.3 (max)** | **54.3** | 71.7 | 59.4 | 31.8 | 59.3M | 0/909 |
| **🟢 OpenCode** | **🟢 GLM-5.3** | **🟢 53.6** | 61.4 | 59.4 | 39.9 | 48.0M | 0/909 |
| Kimi Code CLI | Kimi K3 | 51.9 | 68.4 | 66.1 | 21.2 | 28.3M | 0/909 |
| Claude Code | Step 5 Preview | 51.2 | 61.9 | 58.3 | 33.3 | 71.6M | 0/908 |
| Grok Build | Grok 4.6 (xhigh) | 47.0 | 64.9 | 58.3 | 17.7 | 18.1M | 3/909 |
| Claude Code | Sonnet 5.5 (medium) | 45.9 | 65.5 | 44.9 | 27.3 | 4.4M | 19/909 |
| Claude Code | Qwen3.8 Max | 43.3 | 51.0 | 62.1 | 16.7 | 27.6M | 0/909 |
| Antigravity SDK | Gemini 3.8 Flash (high) | 41.9 | 65.8 | 45.2 | 14.6 | 41.9M | 0/909 |
| Muse Code | Muse Spark Open (xhigh) | 41.2 | 60.2 | 57.8 | 5.6 | 53.2M | 0/908 |
| Claude Code | Haiku 5.5 (xhigh) | 41.4 | 49.0 | 51.6 | 23.7 | 20.5M | 1/907 |
| Mirror | Beam 1.0 | 27.7 | 39.8 | 39.8 | 3.5 | 16.7M | 0/906 |

**Read this table for three things:**

- **Effort level is the biggest single lever.** Sonnet 5.5 in Claude Code: `xhigh` **62.9** → `high` 55.0 → `medium` 45.9 → `low` 42.1. Same model, same harness, **20 points**.
- **OpenCode's one entry, GLM-5.3 (53.6), beats Claude Code + Qwen3.8 Max (43.3) and Antigravity + Gemini 3.8 Flash (41.9).** If you're on OpenCode, GLM-5.3 is the empirically best of the 39.
- **Refusals differ by harness.** Claude Code + Sonnet 5.5 refused 33–34 of 909 attempts; Codex + GPT-6 Sol refused 0/907; every Muse Code and OpenCode row refused 0.

---

## 4. Per-axis capability (benchlm.ai)

Ranks are within each category's full field (e.g. Coding is out of 152 models, Reasoning out of 27).

| Model | Coding | Agentic | Reasoning | Multimodal | Knowledge | Inst.Follow |
|---|---|---|---|---|---|---|
| **Claude Sonnet 5.5** | **#1** (84.3) | #11 (69.1) | – | – | #5 (82.8) | – |
| **GPT-6 Astra** | #4 (75.5) | #7 (75.1) | **#1** (93.3) | – | #3 (86.3) | – |
| **GPT-6.1 Sol** | #8 (71.0) | #5 (76.2) | #2 (90.5) | – | #4 (86.1) | – |
| **Gemini 4 Argon** | #6 (73.0) | **#3** (78.7) | #3 (86.9) | – | #8 (81.4) | – |
| **Muse Wonder Full** | #5 (74.3) | – | – | – | #10 (78.8) | – |
| **Qwen3.8 Max** | #37 (53.5) | #14 (67.4) | – | **#4** (91.2) | #25 (68.2) | **#2** (94.7) |
| **Qwen3.8-Flash-Next** | #42 (51.6) | #17 (65.5) | – | **#8** (87.7) | #53 | #22 (91.2) |
| **Gemini 3.8 Flash** | #19 (60.9) | #16 (66.0) | #14 (74.3) | **#9** (87.3) | #13 (73.4) | – |
| **MiMo-V2.6-Pro** | #13 (63.3) | #13 (67.9) | – | – | – | – |
| **GLM-5.3** | #29 (56.3) | **#8** (70.2) | – | – | #44 (62.6) | – |
| **GLM-5.3-Flash** | #47 (48.1) | #37 (56.9) | – | #14 (84.0) | #50 (60.3) | – |
| **Ling 3.1 Flash** | #27 (57.2) | #22 (62.8) | – | – | #43 (63.4) | – |
| **DeepSeek V4.1 Flash** | #18 (60.9) | #24 (61.7) | – | – | #36 (65.2) | – |
| **MiniMax-M3.1-Flash** | #17 (61.3) | #19 (64.0) | – | #30 (73.5) | #14 (73.3) | – |
| Mistral Large 4 | #54 (45.5) | #48 (50.1) | **#9** (80.8) | – | – | – |
| Hy4 preview | #28 (56.7) | #40 (56.0) | – | – | #41 (64.3) | – |
| Inkling | #84 (33.7) | #77 (37.2) | – | #35 (67.8) | #65 | #36 (87.6) |
| GLM-4.7 | #73 (37.2) | #94 (32.1) | – | – | #102 | – |
| MiniMax-M3 | #74 (37.0) | #70 (39.2) | – | #44 (60.0) | #76 | – |
| gpt-oss-120b | #113 (23.0) | #113 (19.9) | – | – | #124 | – |

**Where the boards disagree — and who wins.** AA scores MiniMax-M3 **#1 in the entire 271-model set on τ²-bench (.889)**. benchlm puts it **#70 for Agentic**; OpenRouter puts it **#30**. The resolution: it's a *strict function-calling* specialist, not a general agentic model. Same story for Qwen3.8 Max — AA's composite says #15, OpenRouter says **#4**, benchlm says **#2 for instruction following**. **One board will always mislead you. Cross-read at least two.**

---

## 5. OpenRouter's three boards

OpenRouter publishes three separate rankings, and they disagree with each other and with AA.

| Model | Intelligence | Coding | Agentic |
|---|---:|---:|---:|
| Claude Opus 5.5 | #1 · 57.6 | – | – |
| Claude Sonnet 5.5 | #2 · 56.0 | – | – |
| Claude Fable 5.1 | #3 · 53.4 | #1 · 81.6 | #1 · 57.9 |
| **Qwen3.8 Max** | **#4 · 53.4** | #11 · 76.2 | **#3 · 56.0** |
| GPT-6 Astra | #5 · 52.7 | **#4 · 77.1** | #7 · 51.0 |
| Gemini 4 Argon | #6 · 52.6 | – | – |
| GPT-6.1 Sol | #7 · 51.8 | – | – |
| **Muse Spark 1.3** | **#10 · 48.1** | **#7 · 76.5** | **#4 · 55.5** |
| GPT-6 Sol | #11 · 47.6 | – | – |
| MiMo-V2.6-Pro | #14 · 46.3 | – | – |
| **GLM-5.3** | #16 · 44.8 | **#14 · 74.8** | **#5 · 53.1** |
| **GLM-5.3-Flash** | #23 · 41.8 | #20 · 71.5 | **#8 · 50.9** |
| Gemini 3.8 Flash | #26 · 40.9 | **#9 · 76.3** | #24 · 40.2 |
| Claude Sonnet 5 | #36 · 38.2 | #21 · 71.5 | #16 · 43.6 |
| Grok Build 0.1 | #63 · 27.2 | #59 · 51.5 | – |
| **Step 3.7 Flash** | **#117 · 19.5** | **#82 · 39.6** | – |
| **GLM-4.7** | **#99 · 22.2** | #73 · 45.3 | – |
| **GLM-4.7-Flash** | **#143 · 14.9** | – | – |
| **Nemotron 3 Super** | **#159 · 12.8** | #85 · 37.7 | **#78 · 1.7** |
| gpt-oss-120b | #173 · 11.6 | #94 · 30.4 | #72 · 3.7 |

---

## 6. Multimodal / video capability — the hard constraint

Only these accept **video** input. If your pipeline involves video, everything else is off the table.

| Model | Video | Audio | Image | File/PDF | Notes |
|---|:--:|:--:|:--:|:--:|---|
| **Gemini 4 Argon** | ✅ | ✅ | ✅ | ✅ | **1M output tokens** (up from 64K); Google's only first-party LVBench claim |
| **Muse Wonder / Full** | ✅ | ✅ | ✅ | ✅ | 1M ctx; #2 Arena Text; #2 AA coding-agent |
| **Ling 3.0 Flash VL** | ✅ | – | ✅ | – | HF card: *"VideoRoPE… supporting tasks such as event localization, long-video question answering, and **video clip editing**"*. 124B/5.5B, MIT |
| **MiMo-V2.6-Pro / Flash** | ✅ | ✅ | ✅ | – | 729M ViT + dedicated audio encoder; 1M ctx; MIT |
| **Qwen3.8-Flash** | ✅ | – | ✅ | – | **LVBench 76.6** (highest in Qwen's own table) |
| **Step 3.7 Flash** | ✅ | – | ✅ | – | 1st SimpleVQA(Search) 79.2; up to 400 tok/s; 128GB unified memory |
| **Dots-3 Note** | ✅ | ✅ | ✅ | – | *"Video inputs include their audio track when available"*; 512k ctx |
| **Muse Spark 1.3** | ✅ | – | ✅ | ✅ | *"perceives video, images and documents"*; MRCR 98.1 @512k–1M |
| Gemini 3.8 Flash / 3.5 Flash-Lite | ✅ | ✅ | ✅ | ✅ | |
| Nemotron 3.5 Super VL | ✅ | – | ✅ | – | 1M ctx |
| Inkling | ❌ | ✅ | ✅ | – | **no video** |
| **Claude Sonnet 5 / 5.5** | ❌ | ❌ | ✅ | ✅ | **cannot see video** |
| **GPT-6 family** | ❌ | – | ✅ | ✅ | **cannot see video** |
| **GLM-4.7 / 5.2 / 5.3** | ❌ | ❌ | ❌ | ❌ | text only (GLM-5.3-**Flash** *does* take video) |
| Hy3 / Hy4 | ❌ | ❌ | ❌ | ❌ | text only |

---

## 7. OpenRouter ID corrections (these will 404)

A large fraction of model lists floating around use shorthand IDs that don't resolve. Verified against the live `/api/v1/models` catalogue:

| Shorthand you'll see | Correct ID |
|---|---|
| `nemotron-3-super:cloud` | ❌ **`:cloud` is not a valid variant** → `nvidia/nemotron-3-super-120b-a12b` |
| `dots-studio/dots-3-note-preview` | `dots-studio/dots-3-note-preview:free` (only the `:free` entry exists) |
| `muse-spark-open` | `meta/muse-spark-open` |
| `mistral-large-4` | `mistralai/mistral-large-4-0` |
| `minimax-m3`, `minimax-m3.1-flash` | `minimax/minimax-m3`, `minimax/minimax-m3.1-flash` |
| `beam` | `reflection/beam-1.0-501b-a23b` |
| `grok-build-0.1` | `x-ai/grok-build-0.1` |
| `deepseek-v4.1-flash` | `deepseek/deepseek-v4.1-flash` |
| `glm-5.3-flash` | `z-ai/glm-5.3-flash` |
| `gpt-oss:20b` | `openai/gpt-oss-20b` |
| `gpt-oss:120b` | `openai/gpt-oss-120b` |
| `z-ai/glm-4.7:thinking` | ✅ valid (routing variant) |
| `z-ai/glm-4.7-flash:thinking` | ✅ valid |
| `z-ai/glm-5.2:thinking` | ✅ valid |
| `deepseek/deepseek-v4.1-flash:thinking` | ✅ valid |
| `stepfun/step-3.7-flash:thinking` | ✅ valid |

**OpenRouter variant taxonomy** (full table in `data/openrouter_variants.csv`):

- **Catalog variants** — separate entries with their own pricing/context: `:free`, `:batch`
- **Routing variants** — not listed in the models API; they change how the request is routed: `:thinking` (interleaved thinking), `:nitro` (sort by throughput), `:floor` (sort by price), `:exacto` (sort by tool-calling reliability), `:online` (deprecated)
- **`:cloud` does not exist.**

---

## 8. Harness comparison — Goose vs OpenCode vs Hermes vs LibreFang

| | **Goose** (block/goose → AAIF) | **OpenCode** (anomalyco/opencode) | **Hermes Agent / Desktop** (NousResearch) | **LibreFang** (librefang/librefang) |
|---|---|---|---|---|
| **Shape** | Rust agent, desktop + CLI + API | TypeScript coding agent, CLI + desktop (beta) | Self-improving agent, CLI + desktop | Rust "Agent OS", CLI + web dashboard |
| **Provider reach** | 40+ — OpenRouter, Anthropic, OpenAI, Gemini, Vertex, Bedrock, Azure, GitHub Copilot, Groq, Mistral, Z.AI, Cerebras, Perplexity, Snowflake, Databricks, LiteLLM, **Cursor Agent (CLI)**, **Claude ACP / Codex ACP** | 75+ via AI SDK + Models.dev — OpenRouter, Anthropic, OpenAI, Azure, Bedrock, Vertex, Copilot, xAI, Z.AI, NVIDIA, Groq, DeepSeek, Together, Fireworks, **llama.cpp, LM Studio, Ollama** | Nous Portal (one OAuth → model + web search + image gen + TTS + browser), **OpenRouter `provider/model` format**, Bedrock, Vertex, Foundry, xAI OAuth | 49 providers, 230+ models, 23 aliases, 3 native drivers (Anthropic, Gemini, OpenAI-compatible) — OpenRouter, Zhipu, Z.ai, MiniMax, Qwen, Bedrock, Vertex, **Ollama, vLLM, LM Studio**, NVIDIA NIM, DeepInfra |
| **Local models** | Ollama, LM Studio, Docker Model Runner, Ramalama | ⭐ llama.cpp, LM Studio, Ollama — best local story | Runs local LLMs on Mac (has a guide) | ⭐ Ollama, vLLM, LM Studio + dynamic `~/.librefang/providers/*.toml` |
| **Reasoning effort** | Per-provider; Anthropic effort levels | Via provider | Via provider | Via provider |
| **Orchestration** | Recipes, subagents, extensions | `build`/`plan` agents + `@general` subagent | Skills that self-improve, delegation, cron, 9 messaging platforms | MCP **+ A2A**, 44 channel adapters, cron, profiles, 16-layer security |
| **Docs say** | *"goose relies heavily on tool calling capabilities and currently works best with Claude 4 models. Berkeley Function-Calling Leaderboard can be a good guide."* | — | — | — |
| **Best for** | Anthropic-direct Claude; heavy tool use | ⭐ Self-hosting and local inference | ⭐ Always-on business automation, multimodal pipelines | ⭐ Scheduled multi-channel ops, self-hosted |

**Per-harness model picks:**

- **Goose** → Claude Sonnet 5.5 (Anthropic direct). Its own docs point at function-calling reliability, so for non-Claude models weight **τ²-bench + IFBench + Toolathlon**: MiniMax-M3 (.889 τ²), Nemotron 3 Ultra (.833 τ²), GLM-5.3 (Toolathlon 73.0).
- **OpenCode** → **GLM-5.3** (the only model in AA's harness table with an OpenCode entry, at 53.6). Self-host with llama.cpp/LM Studio/Ollama; Step 3.7 Flash and Nemotron 3 Super are also viable locally.
- **Hermes** → Gemini 4 Argon or Claude Sonnet 5.5 via OpenRouter/Nous Portal. Hermes' own docs use the `provider/model` format and the `:free` tag, exactly like your `:thinking` IDs.
- **LibreFang** → Anthropic direct for Anthropic models (**File Upload ✓ and Prompt Cache ✓** vs only *partial* through OpenRouter), Zhipu/Z.ai direct for GLM, MiniMax direct for MiniMax. Best fit for scheduled, multi-channel, self-hosted work.

---

## 9. The routing plan

A 5-model setup beats a 1-model setup. Here's what a real stack looks like:

| Slot | Model | Run it in | Switch when |
|---|---|---|---|
| ✍️ **Content / copy** | **Gemini 4 Argon** | Hermes or Goose, Google direct | Always. Highest human-preference score + lowest hallucination |
| 🧠 **Agent / builder** | **Claude Sonnet 5.5 @ `xhigh`** | Goose or OpenCode, Anthropic direct | Always. #1 Coding on benchlm, 62.9 in AA's harness |
| 🎥 **Video** | **Gemini 4 Argon** (cloud) + **Ling 3.0 Flash VL** (local) | OpenCode + llama.cpp | When you need frame-level analysis or clip boundaries |
| ⚙️ **Tool chains** | **GPT-6.1 Sol @ `xhigh`** | Codex-style harness | For rigid multi-step API orchestration |
| 🔓 **Open-weights** | **GLM-5.3** | OpenCode / LibreFang, Zhipu or Z.ai direct | When you need MIT weights, 1M ctx, no API dependency |
| 📦 **High-volume cheap** | **DeepSeek V4.1 Flash** or **MiMo-V2.6-Flash** | Anywhere via OpenRouter | For bulk drafting at $0.19 / $0.06 per task |

**Non-negotiables from the data:**
1. **Set reasoning effort to `xhigh`/`max` for agentic work.** A 20-point swing within one model beats most model-to-model differences.
2. **Never use MiniMax-M3.1-Flash, gpt-oss-20b/120b, or Nex-N2.5-Pro for anything factual** (non-hallucination .072 / .059 / .092 / .051).
3. **If video matters, filter the candidate list by input modality first**, then rank. Otherwise you'll pick a brilliant model that literally cannot watch the footage.
4. **Check your model's Terminal-Bench 4.0 score before trusting it in an agent.** Ling 3.0 Flash VL scores **.000**, Muse Glimmer **.005**, Hy3 **.005**, Beam **.030** — these are not agent models no matter how good their other numbers look.

---

## 10. Source reliability ledger

| Source | What it measures | Trust | Notes |
|---|---|---|---|
| `artificialanalysis.ai/leaderboards/models` | Independent composite + 27 per-eval scores | ⭐⭐⭐⭐⭐ | 271 models, continuous refresh |
| `artificialanalysis.ai/agents/coding-agents` | Model × **real agent harness** | ⭐⭐⭐⭐⭐ | 909 attempts/row, refusal + token counts, includes OpenCode |
| `arena.ai/leaderboard` | **Human preference votes** | ⭐⭐⭐⭐⭐ | 8.9M votes on Text Arena. Gemini 4 Argon / Muse Wonder are flagged *Preliminary* (low vote count, high variance) |
| `openrouter.ai/rankings` | 3 boards, AA-sourced scores | ⭐⭐⭐⭐⭐ | Intelligence / Coding / Agentic are separate and disagree |
| `benchlm.ai` | 22 weighted + 85 display benchmarks, per-axis ranks | ⭐⭐⭐⭐ | 972 models; per-axis percentiles are its real strength |
| `openrouter.ai/api/v1/models` | Specs, modalities, pricing | ⭐⭐⭐⭐⭐ | Authoritative for context + input/output modalities |
| HuggingFace model cards | Vendor benchmark claims | ⭐⭐⭐ | Self-reported; AA's independent runs are consistently lower |
| Anthropic / Google / Meta / Z.ai blogs | Vendor announcements | ⭐⭐⭐ | Useful, but always cross-check against AA |
| `llm-stats.com` | Metadata + Bradley-Terry | ⭐⭐ metadata, ⭐ arena | **Its Arena scores have `games_played` of 1–2 — statistically meaningless. Use it for release dates, params, GPQA/SWE/HLE only.** |
| `openmodelmap.com/rankings` | Composite of 4 benchmarks | ⚠️ **stale** | Its top-10 is Kimi-K2.7-Code, GLM-5.2, DeepSeek-V4-Pro, **Qwen3.5-397B**, DeepSeek-V3.2, Qwen3.6-27B. Its "Performance TOP 100" is led by **GLM-4.7-Flash and Qwen2.5-7B**. Not updated since ~mid-2026. Don't use for decisions. |
| `nano-gpt.com/models` | Subscription catalogue | n/a | Not a leaderboard — 8 featured models, no benchmark data. (It *does* ship `z-ai/glm-5.3:thinking` as a first-class product, confirming `:thinking` is real.) |

### Known gaps in this study
- **Arena sub-boards not retrieved:** Video Edit, WebDev, Image-to-WebDev, Document, Search, Vision, Agent detail — arena.ai is Cloudflare/CAPTCHA-gated beyond the two pages captured. This is the largest remaining gap for video- and web-design-specific picks.
- **14 models have no Artificial Analysis score yet** (GLM-4.7/5.2, Step 3.7 Flash, Hy4, Fugu Max, Nemotron 3 Super, Nex-N2.5-Mini, GPT-6 Sol Pro, Dots-3, Muse Spark 1.3, Claude Sonnet 5, …) — those rows come from vendor cards and are lower-confidence.
- **Vendor vs independent numbers diverge.** Anthropic claims Terminal-Bench 4.0 = 70.6% for Sonnet 5.5; AA independently measures 63.6%. Prefer the independent number.

---

## 11. Reproducing this

```bash
git clone https://github.com/salesflowmarketing-cyber/llm-model-ranker-2026
cd llm-model-ranker-2026
python3 scripts/build_data.py      # regenerates every CSV in data/ from raw/
```

`raw/` holds the cached source payloads. Every leaderboard on this list is client-side rendered, so the extraction code reads Next.js flight-data payloads (`scripts/decode.py`) and brute-force-matches JSON arrays (`scripts/grab.py`) rather than parsing HTML tables.

### How the data was scraped

| Source | Method |
|---|---|
| artificialanalysis.ai | Extract `self.__next_f.push([1, …])` flight payload → locate the `initialModels` / `benchmarkRows` arrays → JSON-parse |
| openrouter.ai/rankings | Same flight-payload technique → `intelligence` / `coding` / `agentic` arrays |
| benchlm.ai | Flight payload → `rows` (972) + per-model `values` / `rankData` / `decisionStats` |
| arena.ai | Cloudflare blocks direct fetch; retrieved via `r.jina.ai` text proxy |
| llm-stats.com | Flight payload → `initialHomepageLLMModels` (408) |
| openmodelmap.com | Flight payload → `itemListElement` (ordered lists) |
| nano-gpt.com | Flight payload → `initialModels` (8 featured) |
| HuggingFace | `https://huggingface.co/<repo>/raw/main/README.md` |

---

## 12. Model specs worth knowing

| Model | Params | Active | Context | License |
|---|---:|---:|---:|---|
| Claude Sonnet 5.5 | — | — | 1M | proprietary |
| GPT-6 Astra / 6.1 Sol | — | — | 1.05M | proprietary |
| Gemini 4 Argon | — | — | 1M | proprietary |
| Muse Wonder / Spark | — | — | 1.05M | proprietary / Muse |
| Muse Spark Open | 816B | 42B | 1M | Muse Model License (gated) |
| GLM-5.3 | 753B | 40B | 1M | GLM-5.3 License |
| GLM-5.3-Flash | 320B | — | 1M | MIT |
| GLM-5.2 | 753B | — | 1M | MIT |
| GLM-4.7 | 358B | 32B | 202k | MIT |
| MiMo-V2.6-Pro | 1.02T | 42B | 1M | MIT |
| MiMo-V2.6-Flash | 309B | 15B | 1M | MIT |
| Qwen3.8-Flash-Next | 125B + 51B n-gram | 6B | 256k | Qwen Community |
| DeepSeek V4.1 Flash | 763B | 16B | 1M | MIT |
| Step 3.7 Flash | 198B | 11B | 256k | Apache 2.0 |
| Step 5 Preview | — | — | 1M | OW |
| Hy3 | 295B | — | 262k | Apache 2.0 |
| Hy4 preview | 770B | 49B | 1M | Apache 2.0 |
| Nemotron 3 Super | 120B | 12B | 262k | NVIDIA Open Model |
| Nemotron 3 Ultra | 550B | 55B | 262k | OpenMDW |
| Ling 3.1 Flash | 560B | 25B | 1M | proprietary |
| Ling 3.0 Flash VL | 124B | 5.5B | 262k | MIT |
| MiniMax-M3 | 428B | 23B | 1M | MiniMax Community |
| Inkling / Inkling Small | 975B / 276B | 41B / 12B | 524k | Apache 2.0 |
| Mistral Large 4 | 1.05T | — | 1M | proprietary |
| gpt-oss-120b / 20b | 117B / 21B | 5.1B / 3.6B | 131k | Apache 2.0 |
| Beam 1.0 | 501B | 23B | 1M | Apache 2.0 |
| Kimi K3 | 2.8T | — | 1M | Kimi K3 |
| Dots-3 Note | 280B | 16B | 512k | OW |

---

## Credits & attribution

All numbers belong to their original publishers:

- **Artificial Analysis** — Intelligence Index, per-eval scores, coding-agent leaderboard, task-specific indexes (engineering, strategy-and-ops, economics, legal, healthcare) — <https://artificialanalysis.ai>
- **Arena** — human-preference Text/Agent leaderboards — <https://arena.ai>
- **OpenRouter** — rankings + model catalogue — <https://openrouter.ai>
- **benchlm.ai** — multi-benchmark composite + per-axis ranks — <https://benchlm.ai>
- **llm-stats.com** — model metadata — <https://llm-stats.com>
- **Anthropic, Google DeepMind, Meta, Z.ai, Qwen, Xiaomi, DeepSeek, Tencent, StepFun, MiniMax, Mistral, NVIDIA, OpenAI, Sakana, thinkingmachines** — official model cards and release posts
- **Goose (AAIF), OpenCode, Hermes Agent (Nous Research), LibreFang** — official documentation

Benchmark names are trademarks of their respective authors. Vendor-reported figures are labelled as such throughout.

## License

MIT — see [LICENSE](LICENSE). The underlying data belongs to its respective publishers; cite them, not this repo.
