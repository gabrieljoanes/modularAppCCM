def validate_transitions(transitions, context_info=None):
    """
    Validates and filters transitions to avoid false geographic or contextual links
    and repeated phrasing within a single article.

    Parameters:
    - transitions: list of transition strings
    - context_info: optional dictionary with known location or topic metadata

    Returns:
    - list of validated transitions (cleaned and de-duplicated)
    """
    seen = set()
    replacements = []

    for t in transitions:
        cleaned = t.strip()

        # Check for geographic misleading phrasing
        lowered = cleaned.lower()
        if "dans le département voisin" in lowered:
            cleaned = "Autre actualité dans le même département"
        elif "par ailleurs" in lowered and "voisin" in lowered:
            cleaned = "Dans un autre registre local"

        # Check for repeated phrases (especially first 3–5 words)
        base_key = " ".join(cleaned.lower().split()[:4])  # identify by prefix
        if base_key in seen:
            cleaned = "Dans un autre domaine de l’actualité,"
        seen.add(base_key)

        replacements.append(cleaned)

    return replacements
