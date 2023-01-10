import aiohttp
import asyncio
from ..config import settings
import logging

logger = logging.getLogger()


class WeatherRequests:

    async def make_request(self, cityId, session):
        
        api_url = settings.api_url
        params = {
            'id': cityId,
            'appid': settings.api_key
        }

        #1,000 API calls per day for free
        try:
            async with session.post(api_url, params=params) as requests_results:
                logger.info("Async request for city ID {}".format(cityId))
                weatherResult = await requests_results.json()
                status = requests_results.status

            return dict(content=weatherResult, cityId=cityId, status=status)

        except Exception as e:
            logger.error(e)
            return dict(content=e, cityId=cityId, status=500)

    async def process_weather_request(self, cityIds):

        async with aiohttp.ClientSession() as session:
            tasks = []
            for cityId in cityIds:
                task = asyncio.ensure_future(self.make_request(cityId, session))
                tasks.append(task)
    
            return await asyncio.gather(*tasks, return_exceptions=True)