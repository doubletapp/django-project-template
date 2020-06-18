all: build down migrate collectstatic up

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose run app python manage.py migrate

createsuperuser:
	docker-compose run app python manage.py createsuperuser

collectstatic:
	docker-compose run app python manage.py collectstatic --no-input

makemigrations:
	docker-compose run --volume=${PWD}/src:/app/src app python manage.py makemigrations

dev:
	docker-compose run --volume=${PWD}/src:/app/src --publish=8000:8000 app python manage.py runserver 0.0.0.0:8000

.PHONY: all build up down migrate makemigrations dev
