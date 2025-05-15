def validate_transitions(transitions):
    replacements = []
    for t in transitions:
        cleaned = t.strip().lower()

        if "dans le département voisin" in cleaned:
            replacements.append("Autre actualité dans le même département")
        elif "région voisine" in cleaned:
            replacements.append("Autre fait marquant dans la même région")
        elif "par ailleurs" in cleaned and "voisin" in cleaned:
            replacements.append("Dans un autre registre local")
        else:
            replacements.append(t)

    return replacements
