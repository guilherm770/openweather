from .. import models
from ..pipeline.weather import WeatherChecker
from ..database import get_db
import logging

logger = logging.getLogger()


class WeatherService:

    def __init__(self):
        logger.info('Init WeatherService')
        self.db = next(get_db())

    def __before_process(self, doc: models.WeatherDocument):
        
        new_post = dict(
            status = models.ProcessingStatusType.processing.name,
            error_message = None
        )
        doc.update(new_post, synchronize_session=False)
        self.db.commit()

    def __after_process(self, doc: models.WeatherDocument):
        
        new_post = dict(
            status = models.ProcessingStatusType.done.name
        )
        doc.update(new_post, synchronize_session=False)
        self.db.commit()

    def process_document(self, doc_id):
        try:
            doc = self.db.query(models.WeatherDocument
                ).filter(models.WeatherDocument.id == doc_id)
                
            self.__before_process(doc)
            
            weatherResults = WeatherChecker(self.db).check(doc.first())
            [self.db.add(weatherResult) for weatherResult in weatherResults]
            self.db.commit()

            self.__after_process(doc)

            logger.info('End processing')
        except Exception as ex:
            
            new_post = dict(
                status = models.ProcessingStatusType.error.name,
                error_message = str(ex)
            )
            doc.update(new_post, synchronize_session=False)
            self.db.commit()

            return doc