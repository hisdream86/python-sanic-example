# python-sanic-example
Example python apllication with sanic framework

## How to run

### [Install poetry](https://python-poetry.org/docs/)

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry config virtualenvs.in-project true
```

### Create a virtual environment and install dependencies

```sh
$ poetry update
```

### Run
```
$ source .venv/bin/activate
$ python main.py
```

### Run with docker
```
$ docker build -t python-sanic-example:test .
$ docker run -it -p 8080:8080 python-sanic-example:test
```