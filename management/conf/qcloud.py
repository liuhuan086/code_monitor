DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yyy',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'mysql',
        'PORT': 3306
    }
}

REDIS_CONFIG = {
    'host': 'redis',
    'port': 6379,
    'db': 4,
}

BROKER_BACKEND = 'rabbitmq'

CELERY_BROKER = {
    'user': 'admin',
    'password': 'admin',
    'host': 'rabbitmq',
    'port': 5672,
    'vhost': 'mission',
}

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(**CELERY_BROKER)
