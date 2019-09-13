## Local development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
CREATE DATABASE {project_name};
CREATE USER {project_name}_admin WITH PASSWORD '{project_name}_admin';
GRANT ALL PRIVILEGES ON DATABASE {project_name} TO {project_name}_admin;
```

## Docker

```
sudo docker-compose up -d --build --force-recreate && \
sudo docker exec -it project_name-api_app_1 python manage.py migrate && \
sudo docker exec -it project_name-api_app_1 python manage.py collectstatic --no-input --clear
```


## Nginx
```
server {
    listen 80;
    server_name project_name.doubletapp.ru;

    location / {
        proxy_pass http://localhost:1337;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```
