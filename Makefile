build:
	docker build . -t marcpartensky/pandoc-api
run:
	docker run -it --name pandoc marcpartensky/pandoc-api
	docker rm pandoc
rm:
	docker rm pandoc
prune:
	docker rm pandoc
	docker image rm marcpartensky/pandoc-api
push:
	docker push marcpartensky/pandoc-api
