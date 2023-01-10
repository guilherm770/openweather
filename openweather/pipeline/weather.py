from ..models import WeatherResult
from openweather.pipeline.weatherRequests import WeatherRequests
from ..models import CityIds
import asyncio
import time
import logging

logger = logging.getLogger()


class WeatherChecker:

    def __init__(self, db_session):
        logger.info('Init WeatherChecker')
        self.db = db_session

    def _get_cityIds(self):
        query = self.db.query(CityIds).all()
        cityIds = []
        for item in query:
            cityIds.append(item.cityId)
        return cityIds

    def split(self, list_a, chunk_size):

        for i in range(0, len(list_a), chunk_size):
            yield list_a[i:i + chunk_size]

    def get_weather_results(self):
        
        weatherResults = []
        cityIds = self._get_cityIds()
        chunk_size = 60
        cityIdsChunks = self.split(cityIds, chunk_size)
        
        for cityIdsChunk in cityIdsChunks:
            loop = asyncio.new_event_loop()
            try:
                weatherResults.extend(loop.run_until_complete(WeatherRequests().process_weather_request(cityIdsChunk)))
                time.sleep(60)
            finally:
                loop.close()

        return weatherResults

    def convert_results(self, document, weatherResults):

        weatherConvResults = []
        for weatherResult in weatherResults:
            if weatherResult.get('status') == 200:

                result = WeatherResult()
                result.document_id = document.id
                result.cityId = weatherResult.get('cityId')
                result.tempCelsius = weatherResult.get('content').get('main').get('temp')
                result.humidity = weatherResult.get('content').get('main').get('humidity')
                
                weatherConvResults.append(result)

        return weatherConvResults

    def check(self, document):

        weatherResults = self.get_weather_results()
        return self.convert_results(document, weatherResults)