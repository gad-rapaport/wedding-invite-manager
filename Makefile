run:
	docker compose up -d --build

stop:
	docker compose down

logs:
	docker compose logs -f app

test:
	docker compose run --rm -e SQLALCHEMY_DATABASE_URI=sqlite:///:memory: app pytest tests/ -v

clean:
	docker compose down -v --rmi local

restart:
	docker compose restart app
