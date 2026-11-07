# ACE reproducibility: reflection budget

Course project. Current status: implementation and three-arm API pilot completed; main repeated experiments pending.

## Scope
Official ACE Formula task; base model versus ACE with 3 and 1 maximum reflection rounds. All arms use the same model, subsets and evaluation metric. This is a model-substituted, small-subset reproduction, not a claim to reproduce the original absolute score.

Source: https://github.com/ace-agent/ace at `82709de050e1db6e6ef2f07bcb0393560b94992a`.
Source downloaded from GitHub codeload; the ZIP comment identifies the commit. Original code and data are under `upstream/ace-main`; retain its license when publishing.

## Setup
Windows PowerShell:
```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe scripts/fetch_upstream.py
.\.venv\Scripts\python.exe scripts/prepare_data.py
```

Optional embedding deduplication is disabled consistently across arms; no local LLM or GPU required. Do not commit keys. Use `DEEPSEEK_API_KEY` locally.

## Protocol
Total API budget <= CNY 100. Pilot allowance CNY 5. Main sample sizes remain provisional until pilot cost is measured. Start with 5 train / 5 validation / 10 test examples. Main target 50 / 30 / 100, seeds 42,43,44. Each arm starts with an empty playbook; train updates it, validation selects it, frozen test evaluates it. Never tune against test results. Pilot test examples must be excluded from any manual error-driven prompt tuning.

Track accuracy, input/output tokens, adaptation/test costs separately, duration and playbook snapshots. Record model substitution and subset differences. Exact duplicate questions are removed across splits before sampling; the manifest records exclusions and hashes. This does not guarantee absence of semantic overlap.

## Debug diary
- 2026-11-08: direct GitHub cloning stalled and directory API was rate limited. Official codeload ZIP succeeded.
- Official Formula data are included: 500 training, 300 validation, 200 test records.
- Native DeepSeek provider is not supported by upstream initialization; experiment wrapper will supply compatible clients.
- Original call layer retries up to 1000 times. Paid runner must replace this with bounded/no automatic retries and a persistent cost ledger.
- DeepSeek API connectivity verified with the user-authorized credential held only in the process environment, not project files.

## Pilot results (2026-11-08)
Seed 42, 5 training / 5 validation / 10 test questions, deepseek-flash, thinking disabled, temperature 0, max output 2048. Base: 6/10; ACE r3: 7/10 before and 7/10 after; ACE r1: 7/10 before and 6/10 after. These small samples do not establish improvement or superiority. Repeated baseline outputs varied even at temperature 0. Calls: 10 / 47 / 48 respectively. Usage-based conservative total cost: CNY 0.353464, charging all input at CNY 2/M and output at CNY 8/M. Actual invoice can be lower due to cache hits and off-peak rates. Official pricing checked at https://api-docs.deepseek.com/zh-cn/quick_start/pricing/ .

Both learning arms completed generation, reflection, curation, validation selection and final frozen evaluation. Costs were nearly equal in this tiny pilot: maximum reflection rounds are an upper bound, not a guarantee of extra calls. Main study must record realized reflection counts and replicate runs before attributing differences to this parameter.

Reproduce the pilot after configuring the key locally:
```
.\.venv\Scripts\python.exe -X utf8 scripts/run_experiment.py --phase pilot --arm base --seed 42 --model deepseek-flash --input-cny-million 2 --output-cny-million 8
```
Replace `base` with `ace_r3` or `ace_r1` for the learning arms. Review current provider rates before reuse. Run `python scripts/summarize.py` for the machine-readable result summary. Logs and results remain local; no GitHub publication has occurred.

## Execution status and budget controls
`scripts/run_experiment.py` runs the official ACE classes with a DeepSeek client adapter; upstream algorithm files are unchanged. Use `--help` for options. Verified current input/cache-miss and output prices in CNY per million tokens are mandatory arguments; unknown pricing blocks execution. All runs share `results/budget.jsonl`, reserve a conservative per-request amount before sending, disable SDK retries, and stop on API errors. Pilot has a cumulative CNY 5 ceiling; main has a cumulative CNY 95 ceiling (CNY 5 headroom under the authorized total). Do not delete or reset this ledger. Only one runner can operate at once. Reservation totals overestimate actual spend; actual API usage is recorded separately.

Dependency versions are in `requirements-lock.txt`. Tokenizer cache is in `.cache/tiktoken`. Budget unit test: `python -m unittest discover -s tests`. This tests persistence and refusal of an over-budget request, not provider billing correctness. Data preparation and Python compilation have passed; paid end-to-end execution remains pending.
