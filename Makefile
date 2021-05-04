-include .env

all: build down migrate collectstatic up

s3-if-needed =
ifeq (${ENV},prod)
	s3-if-needed = -f docker-compose.s3.yml
else ifeq (${ENV},test)
	s3-if-needed = -f docker-compose.s3.yml
endif

pull:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml pull

push:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml push

build:
	make rclone
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml build

up:
	make rclone
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml up -d

down:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml down

# $m [migration]
migrate:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app python manage.py migrate $(if $m,app $m,)

createsuperuser:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app python manage.py createsuperuser

collectstatic:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app python manage.py collectstatic --no-input --clear

makemigrations:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --volume=${PWD}/src:/src app python manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

test:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app python manage.py test

test-dev:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --volume=${PWD}/src:/app/src app python manage.py test

lint:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app flake8 --ignore E, F401, F811

dev:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --volume=${PWD}/src:/src --publish=8000:8000 --publish=3000:3000 app python manage.py runserver 0.0.0.0:8000

swagger_build:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --volume=${PWD}/swagger:/app/swagger app python /app/swagger/compile.py
	sudo chown -R ${USER} swagger/build/

swagger_dev:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --volume=${PWD}/swagger/build:/swagger --publish=8080:8080 swagger

# $c [service name]
# $p [params string]
logs:
	journalctl CONTAINER_NAME=project_name__$c -o cat $(if $p,$p,)

sh:
	docker exec -it project_name__$c sh

psql:
	docker exec -it project_name__db psql -U postgres

shell:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run app python manage.py shell

# $e [email]
jwt:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --rm --volume=${PWD}/src:/src app python manage.py shell -c "from app.auth.models import APIUser; print(APIUser.objects.get(email='$e').get_auth_token())"

piplock:
	docker-compose -f docker-compose.yml $(s3-if-needed) -f docker-compose.${ENV}.yml run --rm --no-deps --volume=${PWD}/src:/src --workdir=/src app pipenv install
	sudo chown -R ${USER} src/Pipfile.lock

# $f [filename]
dotenv:
	docker build -t commands ./commands
	docker run commands /bin/sh -c 'python generate_dotenv.py && cat generate_dotenv/.env.example' > $(if $f,$f,.env.tmp)

# $f [filename]
rclone:
	docker build -t commands ./commands
	docker run --rm -v ${PWD}:/commands/src --env-file $(if $f,$f,.env) commands python3 set_rclone_config_base64.py

rclone_plugin:
	docker plugin install sapk/plugin-rclone:v0.0.10 --grant-all-permissions
