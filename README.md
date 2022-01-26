# python-sanic-example
Example Web API application using [Python Sanic](https://github.com/sanic-org/sanic) 

## How to run

### 1. [Install poetry](https://python-poetry.org/docs/)

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry config virtualenvs.in-project true
```

### 2. Create a virtual environment and install dependencies

```sh
$ poetry update
```

### 3. Set environment variables
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

### 4. Initialize your database
Create `product` table using [alembic](https://alembic.sqlalchemy.org/en/latest/)

> You can find initial version of migration file at `alembic/versions/0000_init_products.py`

```sh
$ alembic upgrade head
```

### 5. Run application
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