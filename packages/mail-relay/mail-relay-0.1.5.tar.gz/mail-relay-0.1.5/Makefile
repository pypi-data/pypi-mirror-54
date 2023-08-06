define USAGE
USAGE:
> make
	build: build python package
	unit-test: run unit tests with tox
	integration-test: run integration tests with tox
	test: run all tests
	lint: run flake8 linter with tox

	docker-build: build python package in a linux container
	docker-unit-test: run unit tests with tox in a linux container
	docker-integration-test: run integration tests with tox in a linux container
	docker-test: run all tests in a linux container
	docker-build-runtime: build docker image `relay:${VERSION}` that has installed mail-relay pacakge pulled from pypi
	shell: get interactive shell to builder/tester container

	clean: ...

	publish-pypi: publish package on pypi
	publish-docker-hub: publish image on docker hub
	release: manage release on github, publish on pypi as well as docker hub

]
endef
export USAGE


OS := $(shell uname -s | tr A-Z a-z)
VERSION := $(shell python setup.py --version)


all:
	@echo "$$USAGE"

clean:
	rm -rf ./dist
	rm -rf ./build


.PHONY: build
build:
	python setup.py sdist

unit-test:
	tox -e unit-$(OS)

integration-test:
	tox -e integration-$(OS)

test: unit-test integration-test

lint:
	tox -e flake8


docker-build:
	docker build -f docker/Dockerfile.builder -t mail-relay-builder .

docker-unit-test:
	docker run --rm -it mail-relay-builder make unit-test


docker-test: unit-test-docker


docker-build-runtime:
	docker build -f docker/Dockerfile --build-arg VERSION=$(VERSION) -t relay:$(VERSION) .



shell:
	docker run --rm -it mail-relay-builder


publish-pypi:
	pip install twine
	make clean
	make build
	twine upload dist/*


publish-docker-hub:
	@echo 'todo'

release:
	@echo 'todo: handle version bump, tag releases on git, merge to master'
	make publish-pypi
	make publish-docker-hub

