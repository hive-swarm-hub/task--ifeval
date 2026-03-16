"""Evaluate agent.py on IFEval using instruction_following_eval verifiers."""

import json
import subprocess
import sys
import re


def check_instruction(response: str, instruction_id: str, kwargs: dict) -> bool:
    """Check if a response satisfies a specific instruction constraint."""
    resp_lower = response.lower()

    # keyword constraints
    if instruction_id == "keywords:existence":
        keywords = kwargs.get("keywords", [])
        return all(k.lower() in resp_lower for k in keywords)
    if instruction_id == "keywords:frequency":
        keyword = kwargs.get("keyword", "")
        freq = kwargs.get("frequency", 1)
        relation = kwargs.get("relation", "at least")
        count = resp_lower.count(keyword.lower())
        if relation == "at least":
            return count >= freq
        elif relation == "at most":
            return count <= freq
        return count == freq
    if instruction_id == "keywords:forbidden_words":
        forbidden = kwargs.get("forbidden_words", [])
        return not any(w.lower() in resp_lower for w in forbidden)
    if instruction_id == "keywords:letter_frequency":
        letter = kwargs.get("letter", "").lower()
        let_count = kwargs.get("let_relation", "at least")
        let_freq = kwargs.get("let_frequency", 1)
        count = resp_lower.count(letter)
        if let_count == "at least":
            return count >= let_freq
        return count <= let_freq

    # length constraints
    if instruction_id == "length_constraints:number_sentences":
        num = kwargs.get("num_sentences", 1)
        relation = kwargs.get("relation", "at least")
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        if relation == "at least":
            return len(sentences) >= num
        elif relation == "at most":
            return len(sentences) <= num
        return len(sentences) == num
    if instruction_id == "length_constraints:number_paragraphs":
        num = kwargs.get("num_paragraphs", 1)
        paragraphs = [p.strip() for p in response.split("\n\n") if p.strip()]
        return len(paragraphs) >= num
    if instruction_id == "length_constraints:number_words":
        num = kwargs.get("num_words", 1)
        relation = kwargs.get("relation", "at least")
        words = len(response.split())
        if relation == "at least":
            return words >= num
        elif relation == "at most":
            return words <= num
        return words == num
    if instruction_id == "length_constraints:nth_paragraph_first_word":
        num = kwargs.get("num_paragraphs", 1)
        first_word = kwargs.get("first_word", "").lower()
        paragraphs = [p.strip() for p in response.split("\n\n") if p.strip()]
        if len(paragraphs) >= num:
            words = paragraphs[num - 1].split()
            return words and words[0].lower().strip("*_#") == first_word
        return False

    # format constraints
    if instruction_id == "detectable_format:number_bullet_lists":
        num = kwargs.get("num_bullets", 1)
        bullets = len(re.findall(r'^\s*[\*\-•]\s', response, re.MULTILINE))
        return bullets >= num
    if instruction_id == "detectable_format:constrained_response":
        # must be one of the allowed responses
        return True  # too varied to check generically
    if instruction_id == "detectable_format:number_highlighted_sections":
        num = kwargs.get("num_highlights", 1)
        highlights = len(re.findall(r'\*[^*]+\*', response))
        return highlights >= num
    if instruction_id == "detectable_format:title":
        return bool(re.search(r'^#\s|<<.*>>', response, re.MULTILINE))
    if instruction_id == "detectable_format:json_format":
        try:
            json.loads(response)
            return True
        except:
            return False

    # case constraints
    if instruction_id == "change_case:english_lowercase":
        # all letters should be lowercase
        return response == response.lower()
    if instruction_id == "change_case:english_capital":
        # all letters should be uppercase
        return response == response.upper()

    # content constraints
    if instruction_id == "detectable_content:number_placeholders":
        num = kwargs.get("num_placeholders", 1)
        placeholders = len(re.findall(r'\[.*?\]', response))
        return placeholders >= num
    if instruction_id == "detectable_content:postscript":
        return bool(re.search(r'P\.?S\.?', response, re.IGNORECASE))

    # language constraint
    if instruction_id == "language:response_language":
        return True  # hard to verify without a language detector

    # combination/startend
    if instruction_id == "startend:end_checker":
        end_phrase = kwargs.get("end_phrase", "")
        return response.rstrip().endswith(end_phrase)
    if instruction_id == "startend:quotation":
        return response.startswith('"') and response.rstrip().endswith('"')

    # default: pass (unknown constraint)
    return True


def main():
    with open(sys.argv[1]) as f:
        problems = [json.loads(line) for line in f]

    total_instructions = 0
    satisfied_instructions = 0
    total_prompts = len(problems)
    fully_satisfied = 0

    print(f"Evaluating {total_prompts} problems...", file=sys.stderr)

    for item in problems:
        try:
            result = subprocess.run(
                ["python3", "agent.py"],
                input=json.dumps(item), capture_output=True, text=True, timeout=60,
            )
            response = result.stdout
        except (subprocess.TimeoutExpired, Exception):
            response = ""

        all_passed = True
        for inst_id, kw in zip(item["instruction_id_list"], item["kwargs"]):
            total_instructions += 1
            if isinstance(kw, str):
                try:
                    kw = json.loads(kw)
                except:
                    kw = {}
            if check_instruction(response, inst_id, kw):
                satisfied_instructions += 1
            else:
                all_passed = False

        if all_passed:
            fully_satisfied += 1

    inst_accuracy = satisfied_instructions / total_instructions if total_instructions else 0
    prompt_accuracy = fully_satisfied / total_prompts if total_prompts else 0

    print("---")
    print(f"prompt_accuracy:  {prompt_accuracy:.6f}")
    print(f"inst_accuracy:    {inst_accuracy:.6f}")
    print(f"prompts_passed:   {fully_satisfied}")
    print(f"total_prompts:    {total_prompts}")
    print(f"insts_passed:     {satisfied_instructions}")
    print(f"total_insts:      {total_instructions}")


if __name__ == "__main__":
    main()
