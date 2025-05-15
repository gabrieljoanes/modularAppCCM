import random
import re
from nltk.stem.snowball import FrenchStemmer

stemmer = FrenchStemmer()

def validate_transitions(transitions, context_info=None):
    """
    Validates transitions to remove:
    - repeated intros (e.g. "Par ailleurs")
    - repeated tones
    - repeated stemmed words
    - overused keywords
    - unsafe fallback reuse
    """

    seen_stems = set()
    seen_tones = set()
    seen_keywords = set()
    seen_intros = set()
    cleaned_transitions = []

    fallback_pool = [
        "Autre fait marquant dans la région,",
        "Dans un registre différent,",
        "Un autre fait d’actualité locale mérite l’attention,",
        "Dans un autre cadre d’actualité régionale,",
        "D’un point de vue différent,",
        "Signalons également ce fait notable,"
    ]

    tone_tags = {
        "optimiste": ["plus positive", "note plus légère", "bonne nouvelle", "actualité réjouissante"],
        "historique": ["mémoire historique", "seconde guerre", "passé", "souvenir"],
    }

    blacklisted_keywords = ["sujet", "actualité", "thème"]

    # Known intros to block repetition
    common_intro_phrases = [
        "par ailleurs", "parallèlement", "changeons de sujet", "sur un autre sujet",
        "abordons maintenant", "dans un autre registre", "passons à",
        "dans le cadre", "du côté", "dans un contexte", "notons que"
    ]

    same_region = context_info.get("same_region", True) if context_info else True

    def detect_intro(text):
        lowered = text.strip().lower()
        for phrase in common_intro_phrases:
            if re.match(rf"^{re.escape(phrase)}([,:\s]|$)", lowered):
                return phrase
        return None

    def safe_fallback(seen_intros):
        for _ in range(10):  # try 10 times to avoid infinite loops
            fallback = random.choice(fallback_pool)
            intro = detect_intro(fallback)
            if intro is None or intro not in seen_intros:
                return fallback
        return "Autre actualité dans la région,"  # final resort fallback

    for t in transitions:
        cleaned = t.strip()
        lowered = cleaned.lower()

        # 1. Geographic language normalization
        if same_region and any(p in lowered for p in ["région voisine", "département voisin", "dans les environs"]):
            cleaned = "Autre actualité dans la même région"
            lowered = cleaned.lower()

        # 2. Tone detection
        tone_detected = None
        for tone, triggers in tone_tags.items():
            if any(trigger in lowered for trigger in triggers):
                tone_detected = tone
                break

        # 3. Retry loop: ensure no repeated intro, tone, stemmed word
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
                cleaned = safe_fallback(seen_intros)
                lowered = cleaned.lower()
                tone_detected = None
            else:
                break  # valid transition

        # 4. Blacklisted keyword enforcement
        for word in blacklisted_keywords:
            if re.search(rf"\b{word}\b", lowered):
                if word in seen_keywords:
                    cleaned = safe_fallback(seen_intros)
                    lowered = cleaned.lower()
                else:
                    seen_keywords.add(word)

        # 5. Final memory updates
        final_intro = detect_intro(lowered)
        if final_intro:
            seen_intros.add(final_intro)
        if tone_detected:
            seen_tones.add(tone_detected)
        seen_stems.update(stemmer.stem(w) for w in re.findall(r"\b\w+\b", lowered))

        cleaned_transitions.append(cleaned)

    return cleaned_transitions
