# list all available commands
default:
  just --list

# clean all build, python, and lint files
clean:
	rm -fr dist
	rm -fr .eggs
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .mypy_cache

# install with all deps
install:
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

# lint, format, and check all files
lint:
	pre-commit run --all-files

DEFAULT_IMAGE_NAME := 'billhowelab/llama-fine-tune'

# build docker images
build-docker image_name=DEFAULT_IMAGE_NAME:
	docker build -t {{ image_name }} .

# run docker image locally
run-docker-bash image_name=DEFAULT_IMAGE_NAME:
  docker run --rm -it {{ image_name }} bash

# build Docker
build:
    docker build -t billhowelab/llama-fine-tune .

# run Docker
run:
    docker run -it billhowelab/llama-fine-tune

# tag a new version
tag-for-release version:
	git tag -a "{{version}}" -m "{{version}}"
	echo "Tagged: $(git tag --sort=-version:refname| head -n 1)"

# release a new version
release:
	git push --follow-tags