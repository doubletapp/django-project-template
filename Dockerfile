FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /app/src/

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        make \
        musl-dev \
        python3-dev \
        postgresql-dev \
    && apk add  --no-cache --virtual .build-deps-edge \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gdal-dev \
        geos-dev

COPY requirements.txt /app/
RUN cd /app/ && \
    pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY src /app/src/
WORKDIR /app/src/


CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
