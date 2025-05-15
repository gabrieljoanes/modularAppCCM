import random
import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()


def validate_transitions(transitions, context_info=None):
    """
    Validates transitions to remove:
    - misleading geographic phrases (if same_region is True)
    - repeated openings (normalized or otherwise)
    - duplicate tones
    - overuse of key words like 'sujet'
    - any repeated word across transitions
    """

    seen_words = set()
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

    common_intro_phrases = [
        "par ailleurs", "parallèlement", "changeons de sujet", "sur un autre sujet",
        "abordons maintenant", "dans un autre registre", "passons à",
        "dans le cadre", "du côté", "dans un contexte", "notons que"
    ]

    same_region = context_info.get("same_region", True) if context_info else True

    for t in transitions:
        original = t
        cleaned = t.strip()
        lowered = cleaned.lower()

        # 1. Fix geographic phrasing
        if same_region and any(phrase in lowered for phrase in [
            "région voisine", "département voisin", "dans les environs"
        ]):
            cleaned = "Autre actualité dans la même région"
            lowered = cleaned.lower()

        # 2. Tone detection
        tone_detected = None
        for tone, triggers in tone_tags.items():
            if any(trigger in lowered for trigger in triggers):
                tone_detected = tone
                break

        # 3. Normalized intro detection
        normalized_intro = None
        for phrase in common_intro_phrases:
            if re.match(rf"^{re.escape(phrase)}([,:\s]|$)", lowered):
                normalized_intro = phrase
                break

        # 4. Keyword overuse
        for word in blacklisted_keywords:
            if re.search(rf"\b{word}\b", lowered):
                if word in seen_keywords:
                    cleaned = random.choice(fallback_pool)
                    lowered = cleaned.lower()
                else:
                    seen_keywords.add(word)

        # 5. Global word-level repetition check
        words = set(re.findall(r"\b\w+\b", lowered))
        overlap = words & seen_words
        if overlap:
            cleaned = random.choice(fallback_pool)
            lowered = cleaned.lower()
            words = set(re.findall(r"\b\w+\b", lowered))  # Recalculate for fallback

        # Add seen tone, intro, and words
        if tone_detected:
            seen_tones.add(tone_detected)

        if normalized_intro:
            seen_words.update(normalized_intro.split())

        seen_words.update(words)
        cleaned_transitions.append(cleaned)

    return cleaned_transitions
