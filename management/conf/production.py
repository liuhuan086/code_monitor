DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yyy',
        'USER': 'root',
        'PASSWORD': 'xxx',
        'HOST': 'xxx',
        'PORT': 3306
    }
}

REDIS_CONFIG = {
    'host': 'yyy-redis-prd-master',
    'password': 'xxx',
    'port': 6379,
    'db': 4,
}

BROKER_BACKEND = 'rabbitmq'

CELERY_BROKER = {
    'user': 'mission',
    'password': 'xxx',
    'host': 'xxx',
    'port': 5672,
    'vhost': 'mission',
}

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(**CELERY_BROKER)