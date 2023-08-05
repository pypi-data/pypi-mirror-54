
OS := $(shell uname -s | tr A-Z a-z)
VERSION := $(shell python setup.py --version)


all:
	$(error usage -> 'make [build]')


.PHONY: build
build:
	python setup.py bdist_wheel sdist

build-docker:
	docker build -f docker/Dockerfile -t mail-relay .


unit-test:
	tox -e unit-$(OS)


integration-test:
	tox -e integration-$(OS)


test: unit-test integration-test


unit-test-docker:
	docker run --rm -it mail-relay make unit-test


test-docker: unit-test-docker


shell:
	docker run --rm -it mail-relay

clean:
	rm -rf ./.tox
	rm -rf ./dist
	rm -rf ./build

publish:
	pip install twine
	# @echo
