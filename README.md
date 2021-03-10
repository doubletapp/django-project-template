# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git project_name`
2. `cd project_name && rm -rf .git`
3. `git remote add origin your-project-git`
4. replace all occurrences of `project_name` in code with your project name
5. ENV_FILE=.env make dotenv
6. remove Template section from README.md

## Install python deps
1. add new dependency to Pipfile (paste from PyPi)
2. run `make piplock` to update Pipfile.lock with new deps
3. next `make build` will use new deps

## Logs
```
make logs c=nginx p=-f
make logs c=nginx p='--since="2021-02-11 05:04:00" --until="2021-02-11 05:05:00"'
```

## Swagger
1. Edit `swagger/api-doc.yml`
2. Build swagger with `make swagger_build`
3. Run swagger locally with `make swagger_dev`
4. Open http://127.0.0.1:8080/swagger/

## Obtain ApiUser's JWT
```
make jwt e=user@test.com
```

## Generate temporary .env.tmp for ci
```
make dotenv
make dotenv f=.env
```

### Local .env images example
```
IMAGE_DB=project_name__db
IMAGE_APP=project_name__app
IMAGE_NGINX=project_name__nginx
IMAGE_SWAGGER=project_name__swagger
```


### Remote debugging (VS Code + Docker)
```bash
mkdir .vscode
cp launch.example.json .vscode/launch.json

# (!) make sure that you're using DEBUG=True in settings.py

make dev
# open "Run and Debug" tab in VS Code
# press "Start Debugging"
```
