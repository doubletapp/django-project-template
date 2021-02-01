# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git project_name`
2. `cd project_name && rm -rf .git`
3. `git remote add origin your-project-git`
4. replace all occurrences of `project_name` in code with your project name
5. remove Template section from README.md

## Install python deps
1. add new dependency to Pipfile (paste from PyPi)
2. run `make piplock` to update Pipfile.lock with new deps
3. next `make build` will use new deps

## Logs
```
sudo journalctl CONTAINER_NAME=container_name -o cat
```

## Swagger
1. Edit `swagger/api-doc.yml`
2. Build swagger with `make swagger_build`
3. Run swagger locally with `make swagger_dev`
4. Or `make swagger_build swagger_dev` after making changes to rebuild and start
5. Open http://127.0.0.1:8080/swagger/

## Obtain ApiUser's JWT
EMAIL=user@test.com bash -c 'make jwt'
