def validate_transitions(transitions, context_info=None):
    """
    Validates and filters transitions to avoid:
    - misleading geography
    - repeated phrasing
    - excessive tone similarity

    Returns a cleaned list of transitions.
    """
    seen_prefixes = set()
    seen_tones = set()
    cleaned_transitions = []

    for t in transitions:
        cleaned = t.strip()
        lowered = cleaned.lower()

        # Rule 1: Geography cleanup
        if "dans le département voisin" in lowered:
            cleaned = "Autre actualité dans le même département"
        elif "par ailleurs" in lowered and "voisin" in lowered:
            cleaned = "Dans un autre registre local"

        # Rule 2: Detect repetitive tone (semantic variants)
        tone_tags = {
            "optimiste": ["plus positive", "note plus légère", "bonne nouvelle", "actualité réjouissante"],
            "changement": ["changeons de sujet", "passons à", "sur un autre sujet", "dans un autre registre"],
        }
        tone_detected = None
        for tone, triggers in tone_tags.items():
            for phrase in triggers:
                if phrase in lowered:
                    tone_detected = tone
                    break
            if tone_detected:
                break

        # Rule 3: Block repetition by prefix or semantic tone
        prefix_key = " ".join(lowered.split()[:4])
        if prefix_key in seen_prefixes or (tone_detected and tone_detected in seen_tones):
            cleaned = "Par ailleurs, un autre fait marquant mérite l'attention,"
        seen_prefixes.add(prefix_key)
        if tone_detected:
            seen_tones.add(tone_detected)

        cleaned_transitions.append(cleaned)

    return cleaned_transitions
