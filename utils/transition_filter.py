import random
import re

def validate_transitions(transitions, context_info=None):
    """
    Validates transitions to remove:
    - misleading phrasing
    - repeated opening phrases
    - duplicate tones
    - overuse of key nouns like 'sujet'
    """
    seen_starts = set()
    seen_tones = set()
    seen_keywords = set()
    cleaned_transitions = []

    fallback_pool = [
        "Autre fait marquant dans la région,",
        "Dans un registre différent,",
        "Parallèlement, un autre événement attire l’attention,",
        "Dans un autre cadre d’actualité locale,",
        "D’un autre point de vue régional,",
        "Signalons également ce fait notable,"
    ]

    tone_tags = {
        "optimiste": ["plus positive", "note plus légère", "bonne nouvelle", "actualité réjouissante"],
        "historique": ["mémoire historique", "seconde guerre", "passé", "souvenir"],
    }

    blacklisted_keywords = ["sujet", "actualité", "thème"]

    for t in transitions:
        cleaned = t.strip()
        lowered = cleaned.lower()

        # 1. Fix misleading geography
        if "dans le département voisin" in lowered or "dans les environs" in lowered:
            cleaned = "Autre actualité dans le même département"

        # 2. Tone detection
        tone_detected = None
        for tone, triggers in tone_tags.items():
            if any(phrase in lowered for phrase in triggers):
                tone_detected = tone
                break

        # 3. Start phrase duplication
        start_key = " ".join(lowered.split()[:3])
        if start_key in seen_starts or (tone_detected and tone_detected in seen_tones):
            cleaned = random.choice(fallback_pool)

        seen_starts.add(start_key)
        if tone_detected:
            seen_tones.add(tone_detected)

        # 4. Overuse of key nouns like "sujet"
        for word in blacklisted_keywords:
            if re.search(rf"\\b{word}\\b", cleaned.lower()):
                if word in seen_keywords:
                    cleaned = random.choice(fallback_pool)
                else:
                    seen_keywords.add(word)

        cleaned_transitions.append(cleaned)

    return cleaned_transitions
