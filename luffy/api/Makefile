IMAGE_NAME=fastapi-app:latest
CONTAINER_NAME=fastapi-app-container
HISTORY_FILE= .image_bash_directory

build:
	docker build -t $(IMAGE_NAME) . \
		--build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
		--build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
		--build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
		--build-arg AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
	
run:
	docker run -it \
		--rm \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_DEFAULT_REGION \
		-e AWS_SESSION_TOKEN \
		-d --name $(CONTAINER_NAME) -p 80:80 \
		$(IMAGE_NAME) 


stop:
	docker stop $(CONTAINER_NAME)

clean:
	docker rm $(CONTAINER_NAME)

delete:
	docker rmi -f $(IMAGE_NAME)
