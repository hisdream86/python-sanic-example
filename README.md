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

## How to Run

### 1. Set environment variables
Set environment variables for integrating your database

- `PG_HOST`: Postgres hostname
- `PG_PORT`: Postgres port 
- `PG_DATABASE`: Posrgres database name
- `PG_USER`: Postgres username
- `PG_PASSWORD`: Postgres password

```sh
# Example

$ export PG_HOST='localhost'
$ export PG_PORT='5432'
$ export PG_DATABASE='sanic_example'
$ export PG_USER='sanic_example'
$ export PG_PASSWORD='sanic_example'
```

### 2. Initialize your database
Create `product` table using [alembic](https://alembic.sqlalchemy.org/en/latest/)

> You can find initial version of migration file at `alembic/versions/0000_init_products.py`

```sh
$ alembic upgrade head
```

### 3. Run application
You can run application with simple command below
```
$ source .venv/bin/activate
$ python main.py
```

Or you can run application with docker

```
$ docker build -t python-sanic-example:test .
$ docker run -it -p 8080:8080 python-sanic-example:test
```