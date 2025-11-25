.PHONY: start stop restart logs clean help

include .env
export

start:
	docker-compose up -d --build

stop:
	docker-compose down

remove:
	docker-compose kill
	docker-compose rm -v --force

restart: stop start

restart-listener:
	docker-compose restart listener

reset: remove start

view-responses:
	docker exec artemis-mock /opt/activemq-artemis/bin/artemis queue stat --queueName response.queue --user ${ARTEMIS_USER} --password ${ARTEMIS_PASSWORD}

clean:
	docker-compose down -v --rmi all

clean-responses:
	rm -f answers/*
	docker exec artemis-mock /opt/activemq-artemis/bin/artemis queue purge --name /queue/response.queue --user ${ARTEMIS_USER} --password ${ARTEMIS_PASSWORD}

test-request:
	docker-compose run --rm tester

logs:
	docker-compose logs -f

logs-listener:
	docker logs artemis-listener -f

logs-mock:
	docker logs artemis-mock -f