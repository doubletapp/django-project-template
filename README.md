# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git project_name`
2. `cd project_name && rm -rf .git`
3. `git remote add origin your-project-git`
4. replace all occurrences of `project_name` in code with your project name
5. remove Template section from README.md


# Docker
---
## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/

## Install docker-compose
https://docs.docker.com/compose/install/

## Logs
```
sudo journalctl CONTAINER_NAME=container_name -o cat
```

# Nginx
---
## http NGINX (host machine)
```
server {
    listen 80;
    client_max_body_size 30M;
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
    client_max_body_size 30M;
    server_name project_name.doubletapp.ru;
    return 301 https://project_name.doubletapp.ru$request_uri;
}

server {
    listen 443 ssl;
    client_max_body_size 30M;
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


# GitLab CI
---
## Environment
1. Open `Operations/Environments` in GitLab project and create New Environment (example: test and prod)
2.  Open `Settings/CI|CD/Variables` and create all required variables from .env.example (be careful with \n)
3. Open `Settings/Repository/Deploy-Tokens` and create token for CI (input `DEPLOY_TOKEN_LOGIN: login` and `DEPLOY_TOKEN_PSSWD: password` for this token in `CI|CD/Variables`)
4. Create branch `testing`
5. Create testing file in bucket (example: `autotest/{env}`)
6.  Disable Shared Runners in `Settings/CI|CD/Runners`


## Runner
1. Install (in host machine) gitlab-runnet
https://docs.gitlab.com/runner/install/linux-repository.html
2. Register runner
https://docs.gitlab.com/runner/register/
**Сonfiguration:**
`GitLab instance:` https://gitlab.com
`Token runner:` check from Setting/CI|CD/Runner/Specific-Runners
`Description:` runner-project-name
`Tags:` nothing
`Runner executor:` docker
`Docker image:` docker/compose:latest
3. Fix error x509
open `sudo nano /etc/gitlab-runner/config.toml`
change `volumes = ["/cache"]` to `volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]`
4. Run: `sudo gitlab-runner run`


# Swagger
1. Edit `swagger/api-doc.yml`
2. Build swagger with `make swagger_build`
3. Run swagger locally with `make swagger_dev`
4. Or `make swagger_build swagger_dev` after making changes to rebuild and start
5. Open http://127.0.0.1:8080/swagger/


# JWT token
EMAIL=user@test.com bash -c 'make jwt'
