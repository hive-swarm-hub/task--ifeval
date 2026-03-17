#!/usr/bin/env bash
set -euo pipefail
mkdir -p data
echo "Downloading IFEval..."
python3 -c "
from datasets import load_dataset
import json, pathlib

ds = load_dataset('google/IFEval', split='train')
ds = ds.shuffle(seed=42)
items = list(ds)
n = int(len(items) * 0.8)

dev_out = pathlib.Path('data/dev.jsonl')
with dev_out.open('w') as f:
    for row in items[:n]:
        f.write(json.dumps({'prompt': row['prompt'], 'instruction_id_list': row['instruction_id_list'], 'kwargs': row['kwargs']}) + '\n')

test_out = pathlib.Path('data/test.jsonl')
with test_out.open('w') as f:
    for row in items[n:]:
        f.write(json.dumps({'prompt': row['prompt'], 'instruction_id_list': row['instruction_id_list'], 'kwargs': row['kwargs']}) + '\n')

print(f'Dev:  {n} problems -> {dev_out}')
print(f'Test: {len(items)-n} problems -> {test_out}')
"
echo "Done."
