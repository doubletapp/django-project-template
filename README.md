# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git project_name`
2. `cd project_name && rm -rf .git`
3. `git remote add origin your-project-git`
4. replace all occurrences of `project_name` in code with your project name
5. remove Template section from README.md


# Docker
## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## Install docker-compose
https://docs.docker.com/compose/install/


# Nginx
## http NGINX (host machine)
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

## https NGINX (host machine)
https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx
```
server {
    listen 80;
    server_name project_name.doubletapp.ru;
    return 301 https://project_name.doubletapp.ru$request_uri;
}

server {
    listen 443 ssl;
    server_name project_name.doubletapp.ru;

    ssl_certificate /etc/letsencrypt/live/project_name.doubletapp.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/project_name.doubletapp.ru/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```
