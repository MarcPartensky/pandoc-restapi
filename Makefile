start:
	pipenv run python server.py
update:
	pipenv lock --pre --clear
	pipenv lock -r > requirements.txt
build: update
	docker-compose build pandoc-api
dev: update
	docker-compose up -d --build pandoc-api
push:
	docker-compose push pandoc-api
