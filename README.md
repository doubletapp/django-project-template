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
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
CREATE DATABASE project_name;
CREATE USER project_name_admin WITH PASSWORD 'project_name_admin';
GRANT ALL PRIVILEGES ON DATABASE project_name TO project_name_admin;
```

```
python src/manage.py runserver
```

# Docker development
## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## Install docker-compose
https://docs.docker.com/compose/install/

## Local Settings
### Django
```
/src/config/local_settings.py
```
example:
```
SECRET_KEY = 'ula3!*a=yi3s2c+cheho#d3%*2g@5dp8w#1n5!gic3p(k@e35q'
AUTH_SECRET = 'BuzOqkKctCjcM1pvHC1OSagv4Wr23tYnXF0komnkx4Pq88Tw1TiUBJ8CAGXQHqQ1_lUovnnl-qpix8NAV8A-Y9InlFph1v6GgbNNyfblZH3-q5Hy12Vfg0VeAaVpoWua'
JWT_SECRET = 'f-1KX3azkZy69tNz-IJ1RN35xiiwwlIDB03gbi4oUzxS9JvirtQLRh4WXsFAPVNFBu3ATORMrQ70onuzJT_nJ52kTNyQtPBCEYdvgrOrbUKeyoGTnf7m7Cx-zaPnz8fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'confapp',
        'USER': 'confapp_admin',
        'PASSWORD': 'confapp_admin',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    }
}

DEBUG = True
```

### Docker
```
/.env
```
example:
```
PORT=1337
```

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
sudo docker-compose up -d --build --force-recreate && \
sudo docker exec -it project_name-api_app_1 python manage.py migrate && \
sudo docker exec -it project_name-api_app_1 python manage.py collectstatic --no-input --clear
```
