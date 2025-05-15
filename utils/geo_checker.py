# Simple database for testing. Expand with real values.
city_departments = {
    "Luitré-Dompierre": "Ille-et-Vilaine",
    "Maen Roch": "Ille-et-Vilaine",
    "Dompierre": "Ille-et-Vilaine",
    "Saint-Brice-en-Coglès": "Ille-et-Vilaine"
}

def detect_misleading_geo_transition(transition, previous_text, next_text):
    mentioned = [city for city in city_departments if city in previous_text or city in next_text]
    if not mentioned:
        return False

    if "région voisine" in transition or "département voisin" in transition:
        return True

    return False
