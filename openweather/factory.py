from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openweather import models
from .database import engine
from .celery_utils import create_celery
from .routers import weatherRouter
import pytz
from .config import settings
import datetime
import logging

logger = logging.getLogger()


def create_app() -> FastAPI:
    
    # not needed after migration tool insertion alembic
    #models.Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.celery_app = create_celery()
    config_logging()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(weatherRouter.router)

    return app

class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def converter(self, timestamp):
        # Create datetime in UTC
        dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        # Change datetime's timezone
        return dt.astimezone(pytz.timezone(settings.TZ))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

def config_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)        

    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d/%m/%Y %H:%M:%S")

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # Adicionando o handlers
    logger.addHandler(ch)