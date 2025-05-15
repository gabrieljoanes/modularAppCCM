import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def clean_transitions(transitions):
    seen_prefixes = set()
    autre_used = False
    cleaned = []

    for t in transitions:
        t_lower = t.lower()
        intro = " ".join(t.split()[:4])
        intro_clean = re.sub(r'[^\w\s]', '', intro.lower())

        # Rule: block multiple "autre" usage
        if "autre" in t_lower:
            if autre_used:
                cleaned.append("[REPETITION: 'autre' already used]")
                continue
            else:
                autre_used = True

        # Rule: block exact prefix reuse
        if intro_clean in seen_prefixes:
            cleaned.append("[REPETITION: Replace manually]")
        else:
            seen_prefixes.add(intro_clean)
            cleaned.append(t)

    return cleaned
