include .env

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
	docker-compose run app python manage.py collectstatic --no-input --clear

makemigrations:
	docker-compose run --volume=${PWD}/src:/app/src app python manage.py makemigrations
	sudo chown -R ${USER} src/api/migrations/

test:
	docker-compose run app python manage.py test

lint:
	docker-compose run app flake8 --ignore E, F401, F811

dev:
	docker-compose run --volume=${PWD}/src:/app/src --publish=8000:8000 app python manage.py runserver 0.0.0.0:8000

swagger_build:
	docker-compose run --volume=${PWD}/swagger:/app/swagger app python /app/swagger/compile.py
	sudo chown -R ${USER} swagger/build/

swagger_dev:
	docker-compose run --volume=${PWD}/swagger/build:/swagger --publish=8080:8080 swagger

log:
	sudo journalctl CONTAINER_NAME=${NGINX_CONTAINER_NAME} CONTAINER_NAME=${APP_CONTAINER_NAME} -o cat -f

psql:
	docker exec -it project_name_db--dev psql -U postgres

shell:
	docker-compose run app python manage.py shell

jwt:
	docker-compose run --rm --volume=${PWD}/src:/app/src app python manage.py shell -c "from api.auth.models import APIUser; print(APIUser.objects.get(email='${EMAIL}').get_auth_token())"

piplock:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/app/src --workdir=/app/src app pipenv install
	sudo chown -R ${USER} src/Pipfile.lock

.PHONY: all build up down migrate test lint createsuperuser collectstatic makemigrations dev swagger_build swagger_dev
