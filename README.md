# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git`
2. `mv django-project-template project_name-api`
3. `cd project_name-api && rm -rf .git`
4. `git remote add origin your-project-git`
5. replace all occurrences of `project_name` in code with your project name
6. replace secrets (`change_me!` in code) with your secrets
7. remove Template section from README.md


# Local development
virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

psql
```
CREATE DATABASE project_name;
CREATE USER project_name_admin WITH PASSWORD 'project_name_admin';
GRANT ALL PRIVILEGES ON DATABASE project_name TO project_name_admin;
```

migrate and run
```
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver
```

# Docker deployment
## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## Install docker-compose
https://docs.docker.com/compose/install/

## Nginx (host machine)
```
server {
    listen 80;
    server_name project_name.doubletapp.ru;

    location / {
        proxy_pass http://localhost:{PORT}; // replace port with port from .env
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

## Start
```
cmod +x docker_start.sh
./docker_start.sh
```

## URLs
API Base URL:
```
http://project_name.doubletapp.ru/api
```
Doc:
```
http://project_name.doubletapp.ru/swagger
```
URL:
```
http://project_name.doubletapp.ru/admin
```
---
Secret header for all requests:
```
Secret: change_me!
```
Header for authenticated requests:
```
Authorization: JWT token
```
