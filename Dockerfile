# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY luffy /app/luffy

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
ENV PORT=80

CMD ["uvicorn", "luffy.api.src.main:app", "--host", "0.0.0.0", "--port", "80"]