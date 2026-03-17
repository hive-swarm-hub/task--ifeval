#!/usr/bin/env bash
set -euo pipefail
mkdir -p data
echo "Downloading IFEval..."
python3 -c "
from datasets import load_dataset
import json, pathlib, random

random.seed(42)
items = list(load_dataset('google/IFEval', split='train'))
random.shuffle(items)

dev_out = pathlib.Path('data/dev.jsonl')
with dev_out.open('w') as f:
    for row in items[:150]:
        f.write(json.dumps({'prompt': row['prompt'], 'instruction_id_list': row['instruction_id_list'], 'kwargs': row['kwargs']}) + '
')

test_out = pathlib.Path('data/test.jsonl')
with test_out.open('w') as f:
    for row in items[150:300]:
        f.write(json.dumps({'prompt': row['prompt'], 'instruction_id_list': row['instruction_id_list'], 'kwargs': row['kwargs']}) + '
')

print(f'Dev:  150 problems -> {dev_out}')
print(f'Test: 150 problems -> {test_out}')
"
echo "Done."
