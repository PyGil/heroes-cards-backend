# HeroesCards

## Description

This is a simple project developed using flask with flask-restx.
Sqlite was chosen as the project database for reasons of simplicity.
The project includes CRUD operations with heroes' cards.

## Development

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a development `.env` file using the `.env.example` file in the root directory.

4. Apply database migrations:

```bash
flask db upgrade
```

5. Run the development server:

```bash
flask run
```

## Production

1. Create a production `.env` file using the `.env.example` file in the root directory.

2. Create a docker image using Dockerfile and than run the container.
The commands example: 

```bash
docker build  -t heroes-cards .
docker run --name heroes-cards -p 8000:8000 --rm -d heroes-cards
```