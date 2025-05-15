import json
import random

def load_prompt(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()

def load_transitions(path):
    examples = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            examples.append(json.loads(line))
    return examples

def sample_shots(examples, n):
    return random.sample(examples, n)
