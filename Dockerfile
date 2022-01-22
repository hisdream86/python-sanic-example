FROM python:3.8-buster

WORKDIR /app

COPY . .

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-dev

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]