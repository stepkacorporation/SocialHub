FROM python:3.11.0

ARG ENVIRONMENT

ENV HOME=/home/ \
    APP_HOME=/home/app \
    PYTHONPATH="$PYTHONPATH:/home/fast" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME \
    && groupadd -r socialhub \
    && useradd -r -g socialhub socialhub

WORKDIR $HOME

COPY app/requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY app app
ADD alembic.ini .
COPY tests tests
ADD pytest.ini .
COPY scripts/wait-for-it.sh scripts/wait-for-it.sh

RUN chown -R socialhub:socialhub .

USER socialhub