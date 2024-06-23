FROM node:20.11-alpine AS node
FROM python:3.11-alpine


USER root
WORKDIR /home/root

COPY luffy luffy
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN apk add --update --no-cache \
    bash \
    aws-cli \
    make

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system

COPY --from=node /usr/lib /usr/lib
COPY --from=node /usr/local/lib /usr/local/lib
COPY --from=node /usr/local/include /usr/local/include
COPY --from=node /usr/local/bin /usr/local/bin

RUN npm install -g aws-cdk

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG AWS_SESSION_TOKEN

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
