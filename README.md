# Template
To use this template:
1. `git clone https://github.com/doubletapp/django-project-template.git project_name`
2. `cd project_name && rm -rf .git`
3. `git remote add origin your-project-git`
4. Replace all occurrences of `project_name` in code with your project name
5. `make rclone_plugin`
6. `make dotenv f=.env`
7. Set `ENV` variable in .env file. Available variants are: `prod`, `dev`, `test` 
8. Fill your AWS info in `.env` file (more info in __FILL_AWS_INFO__ section)
9. Remove Template section from README.md

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

## Fill AWS INFO
### Fill all vars in AWS S3 settings in your env file like:
```
AWS_PROVIDER=<One of "DigitalOcean" or "AWS">
AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_ACCESS_KEY>
AWS_STORAGE_BUCKET_NAME=<BUCKET_NAME_TO_MOUNT>
AWS_LOCATION=<AWS_LOCATION>
AWS_S3_PATH=<AWS_BUCKET_PREFIX>
```

## More about AWS_LOCATION
- Example for DigitalOcean provider: `fra1`. You may see other locations in documentation.
- Example for AWS provider: `eu-west-2`. You may see other locations in documentation.


### Remote debugging (VS Code + Docker)
```bash
mkdir .vscode
cp launch.example.json .vscode/launch.json

# (!) make sure that you're using DEBUG=True in settings.py

make dev
# open "Run and Debug" tab in VS Code
# press "Start Debugging"
```
