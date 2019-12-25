FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /app/src/

RUN apt-get update
RUN apt-get -y install libgdal-dev

COPY requirements.txt /app/
RUN cd /app/ && \
    pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY src /app/src/
WORKDIR /app/src/


CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
