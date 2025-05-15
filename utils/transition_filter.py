def validate_transitions(transitions, context_info=None):
    """
    Validates transitions to avoid false geographic or contextual links.

    Parameters:
    - transitions: list of transition strings
    - context_info: optional dictionary with known location or topic metadata

    Returns:
    - list of validated transitions (replacing or flagging problematic ones)
    """
    replacements = []
    for t in transitions:
        cleaned = t.strip().lower()

        # Rule: avoid implying geographic distinction that doesn't exist
        if "dans le département voisin" in cleaned:
            replacements.append("Autre actualité dans le même département")
        elif "par ailleurs" in cleaned and "voisin" in cleaned:
            replacements.append("Dans un autre registre local")
        else:
            replacements.append(t)

    return replacements
