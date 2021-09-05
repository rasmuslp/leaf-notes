"""Get weather information"""

from notes.metno import Metno


class Weather:
    """Gets weather information from Metno"""
    def __init__(self):
        self.metno = Metno()

    def getForecast(self, latitude, longitude, altitude=None):
        """Get location based forecast"""
        metnoForecast = self.metno.locationForecast(latitude, longitude, altitude)
        firstForecast = metnoForecast['properties']['timeseries'][0]

        forecast = {
            'now': {
                'airPressureAtSeaLevel': firstForecast['data']['instant']['details']['air_pressure_at_sea_level'],
                'airTemperature': firstForecast['data']['instant']['details']['air_temperature'],
                'cloudAreaFraction': firstForecast['data']['instant']['details']['cloud_area_fraction'],
                'relativeHumidity': firstForecast['data']['instant']['details']['relative_humidity'],
                'windFromDirection': firstForecast['data']['instant']['details']['wind_from_direction'],
                'windSpeed': firstForecast['data']['instant']['details']['wind_speed']
            },
            'next1Hours': {
                'symbolCode': firstForecast['data']['next_1_hours']['summary']['symbol_code'],
                'precipitationAmount': firstForecast['data']['next_1_hours']['details']['precipitation_amount']
            },
            'next6Hours': {
                'symbolCode': firstForecast['data']['next_6_hours']['summary']['symbol_code'],
                'precipitationAmount': firstForecast['data']['next_6_hours']['details']['precipitation_amount']
            },
            'next12Hours': {
                'symbolCode': firstForecast['data']['next_12_hours']['summary']['symbol_code']
            }
        }

        return forecast
