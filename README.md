# ACE Formula reproducibility

A reduced-data reproduction of Agentic Context Engineering (ACE), with a controlled comparison of maximum correction-reflection depth. Nine main runs cover three sampling seeds and three configurations.

## Submission materials

- [Report (8 pages)](output/ACE_Reproducibility_Report.pdf)
- [Presentation (10 slides)](output/ACE_Presentation.pptx)
- [Per-run metrics](output/analysis/run_metrics.csv) and [detailed analysis](output/analysis/analysis.json)
- [Raw experimental evidence](output/experiment_evidence.tar.gz)
- [Frozen experiment protocol](docs/protocol.md)

## Results

| Configuration | Mean accuracy | Sample SD | Runs |
|---|---:|---:|---:|
| Empty playbook | 70.3% | 3.21 pp | 3 |
| ACE, maximum 3 correction rounds | 78.7% | 2.89 pp | 3 |
| ACE, maximum 1 correction round | 79.0% | 5.00 pp | 3 |

Three-round ACE improves mean accuracy by 8.3 percentage points over the empty-playbook control. The 0.3-point difference between one and three rounds does not establish superiority or equivalence. Samples overlap across seeds; these are not 300 independent test questions per configuration.

Successful API calls cost an estimated CNY 24.607 at conservative peak cache-miss prices, including pilot and interrupted attempts. 

## Reproduction scope

The upstream ACE commit is `82709de050e1db6e6ef2f07bcb0393560b94992a`. Upstream algorithm Python files are unchanged; [source hashes](docs/upstream_source_hashes.json) support verification.

Each seed uses 50 training, 30 validation and 100 test questions from Formula. Same-seed configurations share identical subsets. The hosted model is DeepSeek Flash, with thinking disabled, temperature 0 and a 2048-token output cap. No local GPU is required.

The algorithmic change is the maximum number of correction-reflection rounds, from three to one. Provider integration, logging, budgeting and concurrency are engineering adaptations. The control uses ACE's Generator with an empty playbook. Model, subset size and control prompt differ from the paper, so the study tests the direction of improvement rather than reproducing the original absolute score.

## Inspect existing evidence without API calls

Extract the evidence archive at the repository root:

```powershell
tar -xzf output/experiment_evidence.tar.gz
```

This restores `data/` and `results/`, including subset hashes, raw responses, learned playbooks, run settings, usage records and the budget ledger. Completed and interrupted attempts are retained. Accuracy aggregates include exactly one completed run per configuration and seed; all successful calls count toward cost.

See the [interruption record](docs/recovery.md) and [timeout recovery record](docs/timeout_recovery.md) for excluded incomplete runs.

## Installation and execution

The environment lock was produced on Windows with Python 3.14.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe scripts/fetch_upstream.py
.\.venv\Scripts\python.exe scripts/prepare_data.py
```

To run new experiments, configure `DEEPSEEK_API_KEY` locally and review the model and prices before paid execution. Never commit credentials. The suite skips completed runs and stops on API errors.

```powershell
.\.venv\Scripts\python.exe -X utf8 -u scripts/run_suite.py
```

To analyze saved evidence and rebuild the report:

```powershell
.\.venv\Scripts\python.exe scripts/analyze.py
.\.venv\Scripts\python.exe scripts/summarize.py
.\.venv\Scripts\python.exe scripts/build_report.py
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Analysis requires all 100 test items and reconciles error indices with correct counts. Tests cover budget persistence, settlement and refusal above the limit.

The editable PPTX is supplied. Rebuilding slides with `scripts/build_deck.mjs` requires the Codex bundled Artifact Tool and adjustment of its local runtime paths; experiment and PDF reproduction do not require that library.

## Limitations and disclosure

This study uses one task, three overlapping sampling seeds and a substituted hosted model. Temperature zero does not guarantee deterministic provider output. Fixed run order, strict exact-match scoring and finite output limits are additional limitations. The system updates an external playbook, not model weights.

AI assistance was used for implementation, orchestration and drafting. Numerical results come from saved API executions and analysis scripts.

## Sources

- [ACE paper](https://arxiv.org/html/2510.04618v3)
- [Official ACE implementation](https://github.com/ace-agent/ace)
- [DeepSeek pricing](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)
