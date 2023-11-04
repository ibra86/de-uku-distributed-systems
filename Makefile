requirements:
	 poetry export -f requirements.txt --output requirements.txt
image:
	docker build -f Dockerfile_base . -t python_app_base