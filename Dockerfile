FROM python:3.7-alpine

RUN mkdir -p /app/src/

RUN apk update
RUN apk add --no-cache \
    # Common
    gcc libffi-dev musl-dev \
    # Pillow
    jpeg-dev zlib-dev \
    # Postgres
    postgresql-dev gdal-dev geos-dev

COPY src/Pipfile* /app/src/
RUN cd /app/src/ && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY src /app/src/
WORKDIR /app/src/

CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
