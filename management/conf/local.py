DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yyy',
        'USER': 'root',
        'PASSWORD': '11223344',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}

REDIS_CONFIG = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 4,
}

BROKER_BACKEND = 'rabbitmq'

CELERY_BROKER = {
    'user': 'guest',
    'password': 'guest',
    'host': '127.0.0.1',
    'port': 5672,
    # 'vhost': 'mission',
}

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}'.format(**CELERY_BROKER)


