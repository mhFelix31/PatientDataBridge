from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from config.settings import *  # noqa

postgres = PostgresContainer("postgres:16")
postgres.start()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': postgres.get_container_host_ip(),
        'PORT': postgres.get_exposed_port(postgres.port),
        'USER': postgres.username,
        'NAME': postgres.dbname,
        'PASSWORD': postgres.password
    }
}

redis = RedisContainer("redis:latest")
redis.start()
redis_endpoint = f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(redis.port)}"
CELERY_BROKER_URL = redis_endpoint
CELERY_RESULT_BACKEND = redis_endpoint
