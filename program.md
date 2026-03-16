# IFEval

Improve a solver for instruction-following tasks with verifiable constraints to maximize prompt-level accuracy on IFEval.

## Setup

1. Read these files for full context:
   - `prepare.sh` — downloads IFEval dataset. Do not modify.
   - `eval/eval.sh` — runs evaluation. Do not modify.
   - `agent.py` — the file you modify. The solver.
2. Verify data exists: check that `data/` contains `test.jsonl`. If not, run `bash prepare.sh`.
3. Create `results.tsv` with just the header row.

## Experimentation

Each experiment runs on the test set (50 prompts). You launch it as: `bash eval/eval.sh`.

**What you CAN do:**
- Modify `agent.py` — everything is fair game: prompting strategy, constraint extraction, self-verification, output formatting, chain-of-thought.

**What you CANNOT do:**
- Modify `prepare.sh` or `eval/eval.sh`. They are read-only.
- Modify the test data.
- Change the model (set via `SOLVER_MODEL` env var).
- Install new packages beyond what's in `requirements.txt`.

**The goal: get the highest prompt_accuracy on IFEval.** Each prompt has 1+ verifiable constraints (word count, keywords, formatting, etc.). A prompt is "passed" only if ALL constraints are satisfied.

**The first run**: establish the baseline by running eval as-is.

## Output format

```
---
prompt_accuracy:  0.4200
inst_accuracy:    0.6500
prompts_passed:   21
total_prompts:    50
```

## Logging results

Log to `results.tsv` (tab-separated, do not commit):

```
commit	prompt_accuracy	inst_accuracy	status	description
a1b2c3d	0.420000	0.650000	keep	baseline
```

## The experiment loop

LOOP FOREVER:

1. **THINK** — decide what to try next.
2. Modify `agent.py`.
3. git commit
4. Run: `bash eval/eval.sh > run.log 2>&1`
5. Check: `grep "^prompt_accuracy:" run.log`
6. If crashed, check `tail -n 50 run.log`.
7. Log to results.tsv.
8. If improved, keep. If not, `git reset --hard HEAD~1`.

**NEVER STOP.** The loop runs until interrupted.
