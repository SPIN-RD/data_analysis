FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y git

COPY ./poetry.lock ./pyproject.toml /code/

WORKDIR /code
RUN pip install gunicorn poetry && poetry config virtualenvs.create false && poetry install

COPY . /code
RUN chmod 777 /code/start-server.sh

EXPOSE 8000
CMD ["/code/start-server.sh"]
