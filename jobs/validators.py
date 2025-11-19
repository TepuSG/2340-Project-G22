from abc import ABC, abstractmethod

import requests


class LocationValidator:
    url = "https://nominatim.openstreetmap.org/search"

    def validate(self, value):
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": value, "format": "json", "limit": 1}
        headers = {"User-Agent": "MyJobPlatform/1.0"}

        response = requests.get(url, params=params, headers=headers)

        # Parse JSON
        json_data = response.json()

        # If no results -> invalid address
        if len(json_data) == 0:
            return False

        return True
