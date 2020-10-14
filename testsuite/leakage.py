# encoding: utf-8

from testsuite import ApiTestCase
import json


class CheckTestCase(ApiTestCase):

    def test_get_leakages(self):
        """
        查看任务摘要
        """
        data = dict(
            user_id='81',
            keyword='django',
        )
        resp = self.fetch('/leakages/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_get_leakage(self):
        """
        泄漏信息
        """
        resp = self.fetch('/leakages/8/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_batch_del(self):
        """
        批量删除
        """
        data = dict(
            leakage_ids=[2989, 2988]
        )
        resp = self.fetch('/leakages/batch_del/', data=data, method='DELETE')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_batch_ignore(self):
        """
        批量加白
        """
        data = dict(
            user_id=14,
            leakage_ids=[5750, 5749]
        )
        resp = self.fetch('/leakages/ignore_repo/', data=data, method='PUT')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_batch_confirm(self):
        """
        批量加白
        """
        data = dict(
            user_id=4,
            leakage_ids=[1200, 1199]
        )
        resp = self.fetch('/leakages/confirm_repo/', data=data, method='PUT')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_put_leakage(self):
        """
        添加任务
        """
        data = dict(repo_urls=[
            'https://github.com/wushanghui/project',
            'https://github.com/wkq278276130/weikeqin.github.io'], user_id=3)
        resp = self.fetch('/leakages/ignore_repos/', data=data, method='PUT')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200
