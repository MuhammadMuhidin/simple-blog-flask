build:
	docker compose -f docker/docker-compose.flask.yml build

up:
	docker compose \
		-f docker/docker-compose.db.yml \
		-f docker/docker-compose.flask.yml \
		-f docker/docker-compose.nginx.yml up -d


down:
	docker compose \
		-f docker/docker-compose.db.yml \
		-f docker/docker-compose.flask.yml \
		-f docker/docker-compose.nginx.yml down
