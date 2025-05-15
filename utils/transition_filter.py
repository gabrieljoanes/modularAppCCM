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
    - any repeated word or root across transitions (stemmed)
    """

    seen_stems = set()
    seen_tones = set()
    seen_keywords = set()
    seen_intros = set()
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

    def detect_intro(text):
        for phrase in common_intro_phrases:
            if re.match(rf"^{re.escape(phrase)}([,:\s]|$)", text):
                return phrase
        return None

    for t in transitions:
        cleaned = t.strip()
        lowered = cleaned.lower()

        # 1. Geo correction
        if same_region and any(p in lowered for p in ["région voisine", "département voisin", "dans les environs"]):
            cleaned = "Autre actualité dans la même région"
            lowered = cleaned.lower()

        # 2. Tone detection (once, based on original input)
        tone_detected = None
        for tone, triggers in tone_tags.items():
            if any(trigger in lowered for trigger in triggers):
                tone_detected = tone
                break

        # 3. Retry loop for fallback if repetition is detected
        max_attempts = 3
        for _ in range(max_attempts):
            normalized_intro = detect_intro(lowered)
            words = set(re.findall(r"\b\w+\b", lowered))
            stemmed_words = {stemmer.stem(w) for w in words}

            if (
                (normalized_intro and normalized_intro in seen_intros) or
                (stemmed_words & seen_stems) or
                (tone_detected and tone_detected in seen_tones)
            ):
                cleaned = random.choice(fallback_pool)
                lowered = cleaned.lower()
            else:
                break  # valid transition

        # 4. Keyword blacklist check (independent)
        for word in blacklisted_keywords:
            if re.search(rf"\b{word}\b", lowered):
                if word in seen_keywords:
                    cleaned = random.choice(fallback_pool)
                    lowered = cleaned.lower()
                    normalized_intro = detect_intro(lowered)
                    words = set(re.findall(r"\b\w+\b", lowered))
                    stemmed_words = {stemmer.stem(w) for w in words}
                else:
                    seen_keywords.add(word)

        # 5. Final memory update
        if tone_detected:
            seen_tones.add(tone_detected)
        if normalized_intro:
            seen_intros.add(normalized_intro)
        seen_stems.update(stemmer.stem(w) for w in re.findall(r"\b\w+\b", lowered))

        cleaned_transitions.append(cleaned)

    return cleaned_transitions
