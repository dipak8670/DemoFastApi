# Use an official Python runtime as a parent image
FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/luffy/api/requirements.txt

RUN pip install --no-cache-dir -r /app/luffy/api/requirements.txt

COPY src /app/luffy/api/src

EXPOSE 80
ENV PORT=80

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG AWS_SESSION_TOKEN

ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}
ENV AWS_SESSION_TOKEN ${AWS_SESSION_TOKEN}


CMD ["uvicorn", "luffy.api.src.main:app", "--host", "0.0.0.0", "--port", "80"]