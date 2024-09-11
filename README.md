# INTRO:

This challenge focus on creating a local FHIR server and an
API for both receive info as a CSV and process it to send it
to the FHIR server itself.
It was created using Django-Ninja and Celery, both using the Postgres as DB and
Redis (Key-Value NOSQL db) as Message Broker, it was added Prometheus,
A node-exporter (for node info), and Grafana.

This project has included:

- FHIR server **API** (hapiproject/hapi:latest) **REQUIRED**
- Django-Ninja **API** (dockerfile included) **REQUIRED**
  - Postgres **DB** (postgres:16) **REQUIRED**
- Celery **Async Tasks** (same as django-ninja) **REQUIRED**
  - Redis **Broker** (redis:alpine) **REQUIRED**
- Prometheus **API Observability** (prom/prometheus) **OPTIONAL**
- Node-Exporter **Infra Observability** (prom/node-exporter:latest) **OPTIONAL**
- Grafana **Graphs** (grafana/grafana) **OPTIONAL**

# How to use:

## Development:

Is recommended to use the .devcontainers as it makes not necessary
for installing the dependencies inside your machine. Both the JetBrains IDE and VSCode are compatible.

## Dependecies:

This project uses Django-Ninja, a Python Framework. you will need:

- Any Python version between 3.11 to 3.13, and Poetry (for local debugging)
- Docker, Docker-Compose, Docker Build (To Run the project)

## Setup

The project will run with `docker compose up -d`

FHIR endpoint will be located at http://127.0.0.1:8080 , http://127.0.0.1:8888/fhir/Patient to retrieve Patient info.  
Django-API endpoint will be located at http://127.0.0.1:8000 and documentation at http://127.0.0.1:8000/api/docs .  
Grafana endpoint will be located at http://127.0.0.1:3000 .

*Note*: to run tests, you will need to run the command `pytest` inside a poetry environment or `poetry run pytest`.
Tests might take a little bit of time in the first run as it uses TestContainer library and will need
to pull docker images. To run coverage `poetry run pytest --cov`
