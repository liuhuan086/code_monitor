# encoding: utf-8

from testsuite import ApiTestCase
import json


class CheckTestCase(ApiTestCase):

    def test_add_token(self):
        """
        添加token
        """
        data = dict(token='6eb83db25e5596b6428488ace89a843b0c1e65de', user_id='3')
        resp = self.fetch('/tokens/', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 201

    def test_get_token(self):
        """
        获取token
        """
        resp = self.fetch('/tokens/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

