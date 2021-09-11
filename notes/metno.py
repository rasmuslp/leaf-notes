"""Interface for Met.no's API"""

import logging

from notes.metno_requester import MetnoRequester

logger = logging.getLogger(__name__)


class Metno:
    """Met.no service"""
    def __init__(self):
        self.api = MetnoRequester()

    def locationForecast(self, latitude, longitude, altitude=None):
        """Get location forecast"""
        apiUrl = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
        payload = {
            'lat': latitude,
            'lon': longitude
        }

        if altitude:
            payload['altitude'] = altitude

        data = self.api.request(apiUrl, payload)

        return data
