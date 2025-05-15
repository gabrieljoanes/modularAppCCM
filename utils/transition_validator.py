import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def validate_transitions(transitions):
    seen_stemmed_intros = set()
    autre_used = False
    de_plus_used = False
    validated = []

    for t in transitions:
        original = t.strip()
        t_lower = original.lower()

        # --- Rule 1: Geographic corrections ---
        if "dans le département voisin" in t_lower:
            validated.append("Autre actualité dans le même département")
            continue
        elif "région voisine" in t_lower:
            validated.append("Autre fait marquant dans la même région")
            continue
        elif "par ailleurs" in t_lower and "voisin" in t_lower:
            validated.append("Dans un autre registre local")
            continue

        # --- Rule 2: Block multiple uses of "autre" ---
        if "autre" in t_lower:
            if autre_used:
                if not de_plus_used:
                    validated.append("De plus,")
                    de_plus_used = True
                else:
                    validated.append("[REPETITION: 'autre' blocked]")
                continue
            else:
                autre_used = True

        # --- Rule 3: Prevent reuse of intro stems ---
        intro = " ".join(original.split()[:4])
        intro_clean = re.sub(r'[^\w\s]', '', intro.lower())
        intro_stemmed = " ".join([stemmer.stem(w) for w in intro_clean.split()])

        if intro_stemmed in seen_stemmed_intros:
            if not de_plus_used:
                validated.append("De plus,")
                de_plus_used = True
            else:
                validated.append("[REPETITION: intro blocked]")
        else:
            seen_stemmed_intros.add(intro_stemmed)
            validated.append(original)

    return validated
