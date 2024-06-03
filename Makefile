IMAGE_NAME=my-fastapi-app:latest
CONTAINER_NAME=my-fastapi-app-container

build:
	docker build -t $(IMAGE_NAME) . 
	
run:
	docker run -d --name $(CONTAINER_NAME) -p 80:80 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean:
	docker rm $(CONTAINER_NAME)

delete:
	docker rmi -f $(IMAGE_NAME)
