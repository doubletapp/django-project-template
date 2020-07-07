ENVIRONMENT?=dev

all: build down migrate collectstatic up

build:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml build

up:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml up -d

down:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml down

migrate:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml run app python manage.py migrate

createsuperuser:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml run app python manage.py createsuperuser

collectstatic:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml run app python manage.py collectstatic --no-input --clear

makemigrations:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml run --volume=${PWD}/src:/app/src app python manage.py makemigrations

test:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml  run app python manage.py test
 
lint:
	docker-compose -f env/${ENVIRONMENT}/docker-compose.yml  run app flake8 --ignore E, F401, F811

dev:
	docker-compose run --volume=${PWD}/src:/app/src --publish=8000:8000 app python manage.py runserver 0.0.0.0:8000

.PHONY: all build up down migrate test lint createsuperuser collectstatic makemigrations dev
