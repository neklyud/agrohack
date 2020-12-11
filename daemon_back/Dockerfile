FROM python:3.9.0

RUN pip install poetry==1.1.4

WORKDIR /daemon_back

COPY poetry.lock pyproject.toml /daemon_back/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

ENV PYTHONPATH ./

COPY . /daemon_back
