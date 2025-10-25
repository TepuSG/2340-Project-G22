# Top 50 largest cities in the USA with their coordinates
# Data includes city name, state, and lat/lng coordinates

US_CITIES = [
    ("New York", "NY", 40.7128, -74.0060),
    ("Los Angeles", "CA", 34.0522, -118.2437),
    ("Chicago", "IL", 41.8781, -87.6298),
    ("Houston", "TX", 29.7604, -95.3698),
    ("Phoenix", "AZ", 33.4484, -112.0740),
    ("Philadelphia", "PA", 39.9526, -75.1652),
    ("San Antonio", "TX", 29.4241, -98.4936),
    ("San Diego", "CA", 32.7157, -117.1611),
    ("Dallas", "TX", 32.7767, -96.7970),
    ("San Jose", "CA", 37.3382, -121.8863),
    ("Austin", "TX", 30.2672, -97.7431),
    ("Jacksonville", "FL", 30.3322, -81.6557),
    ("Fort Worth", "TX", 32.7555, -97.3308),
    ("Columbus", "OH", 39.9612, -82.9988),
    ("Charlotte", "NC", 35.2271, -80.8431),
    ("San Francisco", "CA", 37.7749, -122.4194),
    ("Indianapolis", "IN", 39.7684, -86.1581),
    ("Seattle", "WA", 47.6062, -122.3321),
    ("Denver", "CO", 39.7392, -104.9903),
    ("Washington", "DC", 38.9072, -77.0369),
    ("Boston", "MA", 42.3601, -71.0589),
    ("El Paso", "TX", 31.7619, -106.4850),
    ("Nashville", "TN", 36.1627, -86.7816),
    ("Detroit", "MI", 42.3314, -83.0458),
    ("Oklahoma City", "OK", 35.4676, -97.5164),
    ("Portland", "OR", 45.5152, -122.6784),
    ("Las Vegas", "NV", 36.1699, -115.1398),
    ("Memphis", "TN", 35.1495, -90.0490),
    ("Louisville", "KY", 38.2527, -85.7585),
    ("Baltimore", "MD", 39.2904, -76.6122),
    ("Milwaukee", "WI", 43.0389, -87.9065),
    ("Albuquerque", "NM", 35.0844, -106.6504),
    ("Tucson", "AZ", 32.2226, -110.9747),
    ("Fresno", "CA", 36.7378, -119.7871),
    ("Mesa", "AZ", 33.4152, -111.8315),
    ("Sacramento", "CA", 38.5816, -121.4944),
    ("Atlanta", "GA", 33.7490, -84.3880),
    ("Kansas City", "MO", 39.0997, -94.5786),
    ("Colorado Springs", "CO", 38.8339, -104.8214),
    ("Omaha", "NE", 41.2565, -95.9345),
    ("Raleigh", "NC", 35.7796, -78.6382),
    ("Miami", "FL", 25.7617, -80.1918),
    ("Long Beach", "CA", 33.7701, -118.1937),
    ("Virginia Beach", "VA", 36.8529, -75.9780),
    ("Oakland", "CA", 37.8044, -122.2712),
    ("Minneapolis", "MN", 44.9778, -93.2650),
    ("Tulsa", "OK", 36.1540, -95.9928),
    ("Arlington", "TX", 32.7357, -97.1081),
    ("Tampa", "FL", 27.9506, -82.4572),
    ("New Orleans", "LA", 29.9511, -90.0715),
]

def get_cities_list():
    """Return a list of tuples for use in Django choice fields, sorted alphabetically with N/A option first"""
    cities = [(f"{city}, {state}", f"{city}, {state}") for city, state, _, _ in US_CITIES]
    sorted_cities = sorted(cities, key=lambda x: x[0])  # Sort alphabetically by city name
    # Add N/A option at the beginning
    return [("N/A", "N/A - Show All Jobs")] + sorted_cities

def get_city_coordinates(city_state):
    """Get coordinates for a given city, state string"""
    if city_state == "N/A":
        return None, None  # Return None for N/A to show all jobs
    for city, state, lat, lng in US_CITIES:
        if f"{city}, {state}" == city_state:
            return lat, lng
    return None, None