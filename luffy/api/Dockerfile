FROM node:20.11-alpine AS node
FROM python:3.11-alpine


USER root
WORKDIR /home/root

COPY src ./luffy/api/src
COPY Pipfile ./luffy/api/Pipfile
COPY Pipfile.lock ./luffy/api/Pipfile.lock

RUN pip install pipenv
RUN PIPENV_PIPFILE=./luffy/api/Pipfile pipenv install --system --deploy

ENV PYTHONPATH "${PYTHONPATH}:/home/root/luffy/api/src"

EXPOSE 80
ENV PORT=80

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG AWS_SESSION_TOKEN

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}


CMD ["uvicorn", "luffy.api.src.main:app", "--host", "0.0.0.0", "--port", "80"]