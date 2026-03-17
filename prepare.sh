#!/usr/bin/env bash
set -euo pipefail
mkdir -p data
echo "Downloading IFEval..."
python3 << 'PY'
from datasets import load_dataset
import json, pathlib
ds = load_dataset('google/IFEval', split='train')
out = pathlib.Path('data/test.jsonl')
with out.open('w') as f:
    for row in ds:
        f.write(json.dumps({"prompt": row["prompt"], "instruction_id_list": row["instruction_id_list"], "kwargs": row["kwargs"]}) + '\n')
print(f'Wrote {len(ds)} problems to {out}')
PY
echo "Done."
