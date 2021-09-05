"""Interface for Met.no's API"""

from datetime import datetime, timezone
import json
import logging
import requests

logger = logging.getLogger(__name__)

proxies = {
    'http': 'http://localhost:8888',
    'https': 'http://localhost:8888'
}


class MetnoApi:
    """Request interface with caching"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'leaf-notes/0.0.1 github.com/rasmuslp'
        }
        self.cache = {}
        self.metnoDateFormat = '%a, %d %b %Y %H:%M:%S %Z'

    def request(self, url, payload):
        """Perform a cached API request"""
        logger.debug('Requesting data from %s', url)
        headers = self.headers.copy()
        argsHash = hash(url) + hash(json.dumps(payload, sort_keys=True))
        cached = self.cache.get(argsHash)
        if cached:
            # 'expires': 'Sun, 05 Sep 2021 09:16:02 GMT',
            # 'lastModified': 'Sun, 05 Sep 2021 08:45:38 GMT'}

            # you must first check if the current time is later than the
            # expires value stored earlier;

            # If the expires timestamp is in the past, you can repeat
            # the request. However you should do this using the
            # If-Modified-Since HTTP request header with the stored
            # last_modified variable above as value. If the data has not
            # been updated since your last request you will get a
            # 304 Not Modified status code back with no body; you should
            # then continue using the stored data until you get a 200 OK
            # response.

            if not self.isExpired(cached.expires):
                logger.debug('Cache hit for %s', url)
                return json.loads(cached.data)

            headers['If-Modified-Sinc'] = cached.lastModified

        logger.debug('Cache miss for %s', url)
        response = requests.get(url,
                                headers=headers,
                                params=payload,
                                proxies=proxies,
                                verify=False)

        data = response.json()
        if 200 <= response.status_code < 300:
            self.cache[argsHash] = {
                'data': data,
                'expires': response.headers['Expires'],
                'lastModified': response.headers['Last-Modified']
            }
            print(self.cache[argsHash])

        # 304 Not Modified
        if cached and response.status_code == 304:
            return cached.data

        if response.status_code not in [200]:
            logger.warning('Metno API - Status Code %s: %s', response.status_code, data)

        return data

    def isExpired(self, timestampString):
        """Check if timestamp is expired"""
        convertedTimestamp = datetime.strptime(timestampString, self.metnoDateFormat).replace(tzinfo=timezone.utc)

        now = datetime.now(tz=timezone.utc)

        delta = datetime.timestamp(convertedTimestamp) - datetime.timestamp(now)

        if delta < 0:
            return True

        return False


class Metno:
    """Met.no service"""
    def __init__(self, latitude, longitude, altitude=None):
        self.api = MetnoApi()
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def locationForecast(self):
        """Get location forecast"""
        apiUrl = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
        payload = {
            'lat': self.latitude,
            'lon': self.longitude
        }
        print(payload)

        if self.altitude:
            payload['altitude'] = self.altitude

        data = self.api.request(apiUrl, payload)

        return data
