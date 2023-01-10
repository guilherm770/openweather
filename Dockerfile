FROM python:3.9.13 as requirements-stage

WORKDIR /tmp

RUN pip install -U pip
RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9.13

ENV PYTHONFAULTHANDLER=1 \
        PYTHONUNBUFFERED=1 \
        PYTHONHASHSEED=random \
        PIP_NO_CACHE_DIR=off \
        PIP_DISABLE_PIP_VERSION_CHECK=on \
        PIP_DEFAULT_TIMEOUT=100 \
        PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update && apt-get -y upgrade  
RUN apt-get -y install \
        wget \
        libxft-dev \
        libffi-dev \
        libssl-dev

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./.env /code/.env
COPY ./openweather /code/openweather

COPY alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic

CMD exec uvicorn openweather.main:app --host 0.0.0.0 --port 5000