import requests


class LocationService:
    def __init__(self):
        self.url = "https://nominatim.openstreetmap.org/search"
        self.headers = {"User-Agent": "MyJobPlatform/1.0"}

    def get_location(self, value):

        response = requests.get(
            self.url, params=self.get_params(value, 1), headers=self.headers
        )

        # Parse JSON
        json_data = response.json()

        # If no results -> invalid address
        if len(json_data) == 0:
            return None

        return json_data

    def get_params(self, value, limit):
        return {"q": value, "format": "json", "limit": limit}

    def get_best_locations(self, value):
        response = requests.get(
            self.url, params=self.get_params(value, 5), headers=self.headers
        )

        json_data = response.json()

        return json_data
