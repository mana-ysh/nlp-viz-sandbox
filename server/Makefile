
IMAGE_NAME := nlp-viz-server
CONTAINER_NAME := nlp-viz-container

build-image:
	docker build -t ${IMAGE_NAME} ./

run-container:
	docker run -p 0.0.0.0:5000:5000 ${IMAGE_NAME}