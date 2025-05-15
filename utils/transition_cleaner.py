import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def clean_transitions(transitions):
    seen_prefixes = set()
    autre_used = False
    par_ailleurs_used = False
    cleaned = []

    for t in transitions:
        t_lower = t.lower().strip()

        # Rule: prevent "par ailleurs" repetition
        if "par ailleurs" in t_lower:
            if par_ailleurs_used:
                cleaned.append("[REPETITION: 'par ailleurs' already used]")
                continue
            else:
                par_ailleurs_used = True

        # Rule: prevent more than one use of "autre"
        if "autre" in t_lower:
            if autre_used:
                cleaned.append("[REPETITION: 'autre' already used]")
                continue
            else:
                autre_used = True

        # Rule: prevent repeated intros (based on first 4 words)
        intro = " ".join(t.split()[:4])
        intro_clean = re.sub(r'[^\w\s]', '', intro.lower())
        if intro_clean in seen_prefixes:
            cleaned.append("[REPETITION: intro already used]")
        else:
            seen_prefixes.add(intro_clean)
            cleaned.append(t)

    return cleaned
