from django.test import TestCase
import requests
import json


class ApiTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(ApiTestCase, self).__init__(*args, **kwargs)
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.data = None
        self.uri = ''
        self.host = 'http://127.0.0.1:8000'
        self.mode = ''

    def args(self):
        if self.mode == 'prod':
            return 'http://212.129.229.228/api/dlp'
        return 'http://127.0.0.1:8000'

    def fetch(self, uri, headers=None, data=None, method="GET", host=None, mode=''):
        if headers:
            self.headers.update(headers)
        if mode:
            self.mode = mode

        if not host:
            host = self.args()

        url = '{}{}'.format(host, uri)
        if method.upper() == 'GET' or method.upper() == 'DELETE':
            url += '?' + '&'.join(['{}={}'.format(k, v, k, v) for k, v in data.items()])
        print(url)
        return requests.request(method.upper(), url, headers=self.headers, data=json.dumps(data))
