#!/usr/bin/env bash
# Download IFEval dataset. Run once.
set -euo pipefail

mkdir -p data

echo "Downloading IFEval..."
python3 -c "
from datasets import load_dataset
import json, pathlib, random

random.seed(42)
ds = load_dataset('google/IFEval', split='train')
samples = list(ds)
random.shuffle(samples)
samples = samples[:50]

out = pathlib.Path('data/test.jsonl')
with out.open('w') as f:
    for row in samples:
        f.write(json.dumps({
            'prompt': row['prompt'],
            'instruction_id_list': row['instruction_id_list'],
            'kwargs': row['kwargs'],
        }) + '\n')

print(f'Wrote {len(samples)} problems to {out}')
"

echo "Done. $(wc -l < data/test.jsonl) problems in data/test.jsonl"
