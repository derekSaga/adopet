# Adopet Backend

O projeto é o produto do sexto desafio backend, promovido pela Alura

## Stacks

- [Python](https://go.dev)
- [Python-Poetry](https://python-poetry.org/docs/repositories/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/)
- [Aio-Pika](https://aio-pika.readthedocs.io/en/latest/)
- [SQLAlchemy ](https://www.sqlalchemy.org/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

## Requisitos

- [Docker](https://www.docker.com/)

## Criar migrações

* docker-compose run -e PYTHONPATH=adopet --rm adopet-revision alembic revision --autogenerate -m "[comentário sobre a revisão]"

## Atualizar banco
* docker-compose run -e PYTHONPATH=adopet --rm adopet-revision alembic upgrade head

## Rodar local

1. Clone the repository
2. Run `docker-compose up --build -d` in the root directory of the project
3. The application will be running on `localhost:8080`