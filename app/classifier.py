import re

# -----------------------
# Category Classification
# -----------------------

def detect_category(text):
    text = text.lower()

    if any(word in text for word in ["power", "electricity", "grid", "blackout", "outage"]):
        return "power"

    elif any(word in text for word in ["water", "drought", "flood", "pipeline", "reservoir"]):
        return "water"

    elif any(word in text for word in ["logistics", "transport", "shipment", "supply chain", "delivery", "port"]):
        return "logistics"

    else:
        return "other"


# -----------------------
# City Extraction
# -----------------------

KNOWN_CITIES = [
    "Mumbai", "Delhi", "Chennai", "Kolkata", "Hyderabad",
    "Bangalore", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Mohali", "Kochi", "Kuwait", "Punjab"
]


def detect_city(text):
    for city in KNOWN_CITIES:
        if city.lower() in text.lower():
            return city
    return None


# -----------------------
# Combined Classifier
# -----------------------

def classify_event(title, summary):
    full_text = f"{title} {summary}"

    category = detect_category(full_text)
    city = detect_city(full_text)

    return category, city
