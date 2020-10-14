DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yyy',
        'USER': 'yyy',
        'PASSWORD': 'xxx',
        'HOST': 'xxx',
        'PORT': 3306
    }
}

REDIS_CONFIG = {
    'host': 'xxx',
    'password': 'xxx',
    'port': 6379,
    'db': 1,
}

CELERY_BROKER = {
    'user': 'it-uat',
    'password': 'xxx',
    'host': 'xxx',
    'port': 5672,
    'vhost': 'it-uat',
    'scan_retry_queue': 'scan_again'
}

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(**CELERY_BROKER)
