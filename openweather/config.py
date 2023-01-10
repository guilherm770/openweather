import os
from functools import lru_cache
from kombu import Queue
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}

class BaseConfig(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    api_url: str
    api_key: str

    class Config:
        env_file = ".env"

    CELERY_TASK_QUEUES: list = (
        Queue("celery"),      # default queue
        Queue("weather")      # custom queue
    )

    CELERY_TASK_ROUTES = (route_task,)

class DevelopmentConfig(BaseConfig):
    database_env: str = os.getenv("DATABASE_HOMOLOG_ENV")

class ProductionConfig(BaseConfig):
    database_env: str = os.getenv("DATABASE_PROD_ENV")

@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig
    }

    config_name = os.getenv("APP_ENVIRONMENT")
    config_cls = config_cls_dict[config_name]
    return config_cls()

settings = get_settings()