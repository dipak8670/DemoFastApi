# Use an official Python runtime as a parent image
FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY luffy/api/src /app/luffy/api/src

EXPOSE 80
ENV PORT=80

CMD ["uvicorn", "luffy.api.src.main:app", "--host", "0.0.0.0", "--port", "80"]