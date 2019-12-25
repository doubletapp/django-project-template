docker-compose up -d --build --force-recreate
docker exec -it project_name-api_app python manage.py migrate
docker exec -it project_name-api_app python manage.py collectstatic --no-input --clear
