FROM python:3.11-slim AS requirements

RUN python -m pip install --no-cache-dir --upgrade poetry
WORKDIR /req

COPY pyproject.toml poetry.lock /req/

RUN poetry export -f requirements.txt --without-hashes -o /requirements.txt

# Second stage: application
FROM python:3.11-slim AS application

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add a non-root user
RUN adduser djangoapp
WORKDIR /django
USER djangoapp:djangoapp

# Install requirements
COPY --from=requirements /requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the application code from the project root
COPY . /django/

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh

# Set the entrypoint
CMD ["/bin/bash", "/entrypoint.sh"]