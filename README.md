# de-uku-distributed-systems

Replicated log with one master and two secondary servers

## Makefile
Create requirements.txt
```sh
make requirements
```

## Run app
```shell
docker build -f Dockerfile_base . -t python_app_base
docker-compose up -d --build
```
