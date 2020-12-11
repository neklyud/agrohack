FROM python:3.9.0

RUN pip install poetry==1.1.4

WORKDIR /web_back

COPY poetry.lock pyproject.toml /web_back/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

ENV PYTHONPATH ./
ENV PYTHONUNBUFFERED 1

COPY . /web_back
