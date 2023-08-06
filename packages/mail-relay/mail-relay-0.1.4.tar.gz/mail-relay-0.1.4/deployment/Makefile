define USAGE
USAGE:
> make build VERSION=$$VERSION
> make build VERSION=1.4.2
endef
export USAGE

all:
	@echo "$$USAGE"

build:
	docker build --build-arg VERSION=$(VERSION) -t relay:$(VERSION) .
