import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def clean_transitions(transitions):
    seen_prefixes = set()
    autre_used = False
    de_plus_used = False
    cleaned = []

    for t in transitions:
        t_lower = t.lower()
        intro = " ".join(t.split()[:4])
        intro_clean = re.sub(r'[^\w\s]', '', intro.lower())
        intro_stemmed = " ".join([stemmer.stem(w) for w in intro_clean.split()])

        # Rule: only one use of "autre"
        if "autre" in t_lower:
            if autre_used:
                if not de_plus_used:
                    cleaned.append("De plus,")
                    de_plus_used = True
                else:
                    cleaned.append("[REPETITION]")
                continue
            else:
                autre_used = True

        # Rule: avoid repeating same stemmed prefix
        if intro_stemmed in seen_prefixes:
            if not de_plus_used:
                cleaned.append("De plus,")
                de_plus_used = True
            else:
                cleaned.append("[REPETITION]")
        else:
            seen_prefixes.add(intro_stemmed)
            cleaned.append(t)

    return cleaned
