import re
import random
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

fallback_pool = [
    "Dans l'actualité toujours locale,",
    "Signalons également ce fait notable,",
    "À noter également dans la région,",
    "Autre information à retenir ce jour,",
    "Dans un cadre régional différent,",
    "Fait marquant dans la même zone,",
    "Du côté de l'actualité quotidienne,",
    "Point d'information complémentaire,",
]

def clean_transitions(transitions):
    seen_prefixes = set()
    autre_used = False
    par_ailleurs_used = False
    cleaned = []

    for t in transitions:
        t_lower = t.lower().strip()
        replaced = False

        # Rule 1: prevent multiple "par ailleurs"
        if "par ailleurs" in t_lower:
            if par_ailleurs_used:
                cleaned.append(random.choice(fallback_pool))
                continue
            else:
                par_ailleurs_used = True

        # Rule 2: prevent multiple "autre" usage
        if "autre" in t_lower:
            if autre_used:
                cleaned.append(random.choice(fallback_pool))
                continue
            else:
                autre_used = True

        # Rule 3: prevent reused intros (first 4 words stemmed & cleaned)
        intro = " ".join(t.split()[:4])
        intro_clean = re.sub(r'[^\w\s]', '', intro.lower())
        intro_stemmed = " ".join([stemmer.stem(w) for w in intro_clean.split()])

        if intro_stemmed in seen_prefixes:
            cleaned.append(random.choice(fallback_pool))
        else:
            seen_prefixes.add(intro_stemmed)
            cleaned.append(t)

    return cleaned
