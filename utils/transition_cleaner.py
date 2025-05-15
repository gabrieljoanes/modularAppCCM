import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def clean_transitions(transitions):
    seen_stems = set()
    cleaned = []

    for t in transitions:
        intro = " ".join(t.split()[:4]).lower()
        intro_clean = re.sub(r'[^\w\s]', '', intro.strip())
        intro_stemmed = " ".join([stemmer.stem(w) for w in intro_clean.split()])

        if intro_stemmed in seen_stems:
            cleaned.append("[REPETITION: Replace manually]")
        else:
            seen_stems.add(intro_stemmed)
            cleaned.append(t)

    return cleaned
