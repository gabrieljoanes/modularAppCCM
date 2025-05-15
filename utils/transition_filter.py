import random

def validate_transitions(transitions, context_info=None):
    """
    Validates transitions to remove:
    - geographic misleading phrases
    - repeated starting patterns ("Par ailleurs...")
    - duplicate tones
    """
    seen_starts = set()
    seen_tones = set()
    cleaned_transitions = []

    fallback_pool = [
        "Autre actualité dans la région,",
        "Dans un autre registre local,",
        "Parallèlement à cela,",
        "Sur un tout autre sujet,",
        "Autre fait notable dans le département,",
        "D’un autre côté de l’actualité,"
    ]

    tone_tags = {
        "optimiste": ["plus positive", "note plus légère", "bonne nouvelle", "actualité réjouissante"],
        "historique": ["mémoire historique", "seconde guerre", "passé", "souvenir"],
        "géographique": ["dans les environs", "dans le département voisin"],
    }

    for t in transitions:
        cleaned = t.strip()
        lowered = cleaned.lower()

        # Detect and clean misleading geographic phrasing
        if "dans le département voisin" in lowered or "dans les environs" in lowered:
            cleaned = "Autre actualité dans le même département"

        # Detect tone repetition
        tone_detected = None
        for tone, triggers in tone_tags.items():
            if any(phrase in lowered for phrase in triggers):
                tone_detected = tone
                break

        # Detect same start (first 2–3 words)
        start_key = " ".join(cleaned.split()[:3]).lower()
        if start_key in seen_starts or (tone_detected and tone_detected in seen_tones):
            cleaned = random.choice(fallback_pool)

        seen_starts.add(start_key)
        if tone_detected:
            seen_tones.add(tone_detected)

        cleaned_transitions.append(cleaned)

    return cleaned_transitions
