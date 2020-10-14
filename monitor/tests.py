# encoding: utf-8

from utils.testcase import ApiTestCase
import json


class CheckTestCase(ApiTestCase):

    def test_get_leakages(self):
        """
        查看任务摘要
        """
        resp = self.fetch('/leakages/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_get_leakage(self):
        """
        泄漏信息
        """
        resp = self.fetch('/leakages/1/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_get_token(self):
        """
        获取token
        """
        resp = self.fetch('/tokens', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_get_tasks(self):
        """
        获取任务
        """
        resp = self.fetch('/tasks', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200


