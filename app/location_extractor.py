def extract_location(text):
    cities = ["Mumbai", "Delhi", "Chennai", "Hyderabad", "Bangalore", "Kolkata"]

    for city in cities:
        if city.lower() in text.lower():
            return city, "India"

    return None, None
