"""IFEval solver — the artifact agents evolve.

Takes an instruction-following prompt on stdin, prints the response on stdout.
The response must satisfy specific verifiable constraints (word count, format, etc.).
"""

import sys
import os

from openai import OpenAI


def solve(prompt: str) -> str:
    """Follow the instructions precisely, satisfying all constraints."""
    client = OpenAI()

    response = client.chat.completions.create(
        model=os.environ.get("SOLVER_MODEL", "gpt-4.1-nano"),
        messages=[
            {"role": "system", "content": "Follow the instructions exactly. Pay careful attention to ALL constraints in the prompt (word count, formatting, keywords, structure, etc.)."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=2048,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    import json
    data = json.loads(sys.stdin.read())
    print(solve(data["prompt"]))
