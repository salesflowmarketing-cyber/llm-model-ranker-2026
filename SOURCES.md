# Sources & Extraction Method

Research snapshot: **22 October 2026**. Every number in `data/` was pulled live
from the sources below on that date.

## Sources

| # | Source | URL | What was taken | Extraction |
|---|---|---|---|---|
| 1 | Artificial Analysis — models | `https://artificialanalysis.ai/leaderboards/models` | Intelligence Index + 27 per-eval scores for **271 models** | RSC flight payload → `initialModels` array |
| 2 | Artificial Analysis — coding agents | `https://artificialanalysis.ai/agents/coding-agents` | **34 model×harness rows**, 10 harnesses, DeepSWE v1.1 / SWE-Atlas-QnA / TB v4, token usage, refusal counts | flight payload → `benchmarkRows` array |
| 3 | Artificial Analysis — task indexes | `https://artificialanalysis.ai/indexes/{engineering,strategy-and-ops,economics,legal,healthcare-and-medical}` | Weighted per-domain sub-scores (knowledge, reasoning, agenticTerminalUse, agenticKnowledgeWork) | flight payload → per-index model arrays |
| 4 | Artificial Analysis — model pages | `https://artificialanalysis.ai/models/<slug>` | Specs: params, active params, context, modalities, license, weights, release date (45 pages) | HTML table parse |
| 5 | Arena | `https://arena.ai/leaderboard` and `/leaderboard/chat/text` | **Text Arena**: 417 models, 8,900,458 votes, score ± 90% CI, vote counts. Overview: Top-10 Agents by vote share, Pareto frontier, license trends | Cloudflare-gated → retrieved through the `r.jina.ai` text proxy |
| 6 | OpenRouter — rankings | `https://openrouter.ai/rankings` | **Three** boards: Intelligence (351), Coding (152), Agentic (109) | flight payload → `intelligence` / `coding` / `agentic` arrays |
| 7 | OpenRouter — models API | `https://openrouter.ai/api/v1/models` | Context length, input/output modalities, modality transforms, pricing, params for **468 models** | JSON |
| 8 | benchlm.ai | `https://benchlm.ai/` + `/models/<slug>` | 972-model leaderboard (22 weighted + 85 display benchmarks) and per-axis ranks/percentiles for 43 models | flight payload → `rows`, `values`, `rankData`, `decisionStats` |
| 9 | llm-stats.com | `https://llm-stats.com/` | 408 models: GPQA, SWE-bench Verified, HLE, params, prices, throughput, release dates, Bradley-Terry stats | flight payload → `initialHomepageLLMModels` |
| 10 | nano-gpt.com | `https://nano-gpt.com/models` | Subscription catalogue, 8 featured models (no benchmark data) | flight payload → `initialModels` |
| 11 | openmodelmap.com | `https://openmodelmap.com/rankings/*` | 25 ranking lists, ordered. **Assessed as stale — see below.** | flight payload → `itemListElement` |
| 12 | HuggingFace model cards | `https://huggingface.co/<repo>/raw/main/README.md` | Official benchmark tables, architectures, licences (20 repos) | Markdown |
| 13 | Vendor announcements | Anthropic, Google, Meta, Z.ai, Qwen, Xiaomi, DeepSeek, Tencent, StepFun, MiniMax, Mistral, NVIDIA, OpenAI, Sakana, thinkingmachines | Vendor-reported benchmark claims, marked as such throughout | HTTP fetch |
| 14 | Harness docs | `goose-docs.ai`, `opencode.ai/docs`, `hermes-agent.nousresearch.com/docs`, `docs.librefang.ai` | Provider support, local-model support, context management, orchestration features | HTML text extraction |

## Why the extraction code looks unusual

Every leaderboard above is **client-side rendered**. The served HTML contains no
`<table>` rows and no model names in any stable markup — the dataset lives
inside Next.js RSC "flight" payloads emitted as:

```js
self.__next_f.push([1, "...escaped JSON..."])
```

`scripts/decode.py` concatenates those chunks and `grab()` locates a named
JSON array by bracket matching (string-aware, so braces inside strings don't
break it). This is why the code is ~60 lines instead of a CSS-selector scrape.

## Reproducing

```bash
python3 scripts/build_data.py         # the 8 source CSVs
python3 scripts/build_consolidated.py  # the joined 45-row table
```

`raw/` holds gzipped copies of the cached payloads, so both scripts run
offline. To re-scrape from scratch, re-fetch the URLs above into `raw/` and
re-run.

## Source reliability notes

- **`openmodelmap.com` is stale.** Its "Frontier Models" top-10 is Kimi-K2.7-Code,
  GLM-5.2, DeepSeek-V4-Pro, Qwen3.5-397B-A17B, DeepSeek-V3.2, Qwen3.6-27B…
  and its "Performance TOP 100" is led by GLM-4.7-Flash and Qwen2.5-7B. It has
  not been updated since roughly mid-2026. **Not used for any ranking here.**
- **`llm-stats.com`'s Arena scores are unusable** — most of its Bradley-Terry
  entries have `games_played` of 1–2. Used only for metadata (dates, params,
  GPQA / SWE-bench Verified / HLE).
- **`nano-gpt.com` is a subscription catalogue, not a leaderboard.** It carries
  no benchmark data.
- **Vendor-reported benchmark numbers are systematically optimistic.** Anthropic
  reports Terminal-Bench 4.0 = 70.6% for Claude Sonnet 5.5; Artificial Analysis
  independently measures 63.6%. Vendor claims are labelled as such in the README.

## Known gaps

- **Arena sub-boards not retrieved:** Video Edit, WebDev, Image-to-WebDev,
  Document, Search, Vision, and the detailed Agent board. arena.ai is
  Cloudflare/CAPTCHA-gated beyond the two pages captured here. This is the
  largest remaining gap — those boards are the most directly relevant to video
  editing and web design.
- **14 of the 45 rows have no Artificial Analysis score yet** (GLM-4.7 / 5.2,
  Step 3.7 Flash, Hy4, Fugu Max, Nemotron 3 Super, Nex-N2.5-Mini, GPT-6 Sol Pro,
  Dots-3 Note, Muse Spark 1.3, Claude Sonnet 5, …). Those come from vendor
  model cards and are lower-confidence than the rest.

## Attribution

All benchmark data belongs to its publishers. Benchmark names are trademarks of
their respective authors. Please cite the sources above rather than this repo.
