define USAGE
USAGE:
> make
	build: build python package
	unit-test: run unit tests with tox
	integration-test: run integration tests with tox
	test: run all tests
	build-docker: build python package in a linux container
	unit-test-docker: run unit tests with tox in a linux container
	integration-test-docker: run integration tests with tox in a linux container
	test-docker: run all tests in a linux container
	publish: publish package on pypi
	shell: get interactive shell to builder/tester container
	clean: ...
]
endef

OS := $(shell uname -s | tr A-Z a-z)
VERSION := $(shell python setup.py --version)

export USAGE

all:
	@echo "$$USAGE"

.PHONY: build
build:
	python setup.py sdist

build-docker:
	docker build -f docker/Dockerfile -t mail-relay-builder .


unit-test:
	tox -e unit-$(OS)


integration-test:
	tox -e integration-$(OS)


test: unit-test integration-test


unit-test-docker:
	docker run --rm -it mail-relay-builder make unit-test


test-docker: unit-test-docker


shell:
	docker run --rm -it mail-relay-builder

clean:
	rm -rf ./.tox
	rm -rf ./dist
	rm -rf ./build


publish:
	pip install twine
	make clean
	make build
	twine upload dist/*
