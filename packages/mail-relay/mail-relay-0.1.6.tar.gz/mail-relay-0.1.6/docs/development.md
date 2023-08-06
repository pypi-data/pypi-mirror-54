# Development guide


## Install

Currently py27 is the only supported python version. It is recommended that you install this tool within a fresh virtual environment. More info on https://virtualenv.pypa.io/en/stable/userguide/.

```shell
> cd ${repo_root}
> ${envpip} install -r requirements.txt -r requirements_${osx/linux}.txt
> ${envpip} install .
```



## Testing

We use [tox](https://tox.readthedocs.io/en/latest/index.html) as the project's test runner. Make sure you have **tox >= 3.5.3** installed in your python environment.

#### Run all tests

```shell
> cd ${repo_core}
> tox
```



#### Unit tests

```shell
> tox -e unit-${darwin/linux}
```



#### Integration tests

```shell
> tox -e integration-${darwin/linux}
```



## Linting

We use [flake8](http://flake8.pycqa.org/en/latest/) as project's linter. Enforcement via:

```shell
> tox -e flake8
```


## Some helper CLIs through make
There are some handy make commands that you can use. Check out usage:

```shell
> cd ${repo-root}
> make
```
