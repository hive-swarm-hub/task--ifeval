#!/usr/bin/env bash
set -euo pipefail
mkdir -p data
echo "Downloading IFEval..."
python3 << 'PY'
from datasets import load_dataset
import json, pathlib, random
random.seed(42)
items = list(load_dataset('google/IFEval', split='train'))
random.shuffle(items)
with pathlib.Path('data/train.jsonl').open('w') as f:
    for row in items[:100]:
        f.write(json.dumps({"prompt": row["prompt"], "instruction_id_list": row["instruction_id_list"], "kwargs": row["kwargs"]}) + '\n')
with pathlib.Path('data/test.jsonl').open('w') as f:
    for row in items[100:250]:
        f.write(json.dumps({"prompt": row["prompt"], "instruction_id_list": row["instruction_id_list"], "kwargs": row["kwargs"]}) + '\n')
print('Train: 100, Test: 150')
PY
echo "Done."
