"""Requester for Met.no's API"""

from datetime import datetime, timedelta, timezone
import json
import logging
import requests
import schedule

logger = logging.getLogger(__name__)

proxies = {}

PROXY_ENABLED = False
if PROXY_ENABLED:
    proxies['http'] = 'http://localhost:8888'
    proxies['https'] = 'https://localhost:8888'


class MetnoRequester:
    """Request with caching"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'leaf-notes/0.1.0 github.com/rasmuslp'
        }
        self.cache = {}
        self.cacheCleanSchedule = schedule.every(30).minutes.do(self.cleanCache)
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

            if not self.isExpired(cached['expires']):
                logger.info('Cache hit for %s', url)
                return json.loads(cached['data'])

            logger.info('Cache expired for %s', url)
            headers['If-Modified-Since'] = cached['lastModified']

        logger.info('Checking for new data for %s', url)
        response = requests.get(url,
                                headers=headers,
                                params=payload,
                                proxies=proxies,
                                verify=False)

        data = response.json()
        if 200 <= response.status_code < 300:
            self.cache[argsHash] = {
                'data': json.dumps(data),
                'expires': response.headers['Expires'],
                'lastModified': response.headers['Last-Modified']
            }
            logger.info('Caching new data for %s', url)

        # 304 Not Modified
        if cached and response.status_code == 304:
            logger.info('Data not modified for %s returning cached data', url)
            return json.loads(cached['data'])

        if response.status_code not in [200]:
            logger.warning('Metno API - Status Code %s: %s', response.status_code, data)

        return data

    def isExpired(self, timestampString, offsetMinutes=None):
        """Check if timestamp is expired"""
        convertedTimestamp = datetime.strptime(timestampString, self.metnoDateFormat).replace(tzinfo=timezone.utc)
        if offsetMinutes:
            convertedTimestamp = convertedTimestamp + timedelta(minutes=offsetMinutes)

        now = datetime.now(tz=timezone.utc)

        delta = datetime.timestamp(convertedTimestamp) - datetime.timestamp(now)

        if delta < 0:
            return True

        return False

    def cleanCache(self):
        """Clean cache by looking at 'expires' + an offset"""
        sixHours = 6 * 60
        for key, value in dict(self.cache).items():
            if self.isExpired(value['expires'], sixHours):
                self.cache.pop(key)
