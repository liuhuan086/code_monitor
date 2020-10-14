# encoding: utf-8

from testsuite import ApiTestCase
import json


class CheckTestCase(ApiTestCase):

    def test_get_tasks(self):
        """
        获取任务
        """
        resp = self.fetch('/tasks/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_add_task(self):
        """
        添加任务
        """
        data = dict(name='python', user_id='2', keyword='python')
        resp = self.fetch('/tasks/', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 201

    def test_different_user_add_task(self):
        """
        添加任务
        """
        data = dict(name='1', user_id='3', keyword='1')
        resp = self.fetch('/tasks/', data=data, method='POST')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 201

    def test_update_task(self):
        """
        修改任务
        """
        data = dict(name='test', user_id=1, keyword='wm-icenter')
        resp = self.fetch('/tasks/1/', data=data, method='PUT')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 201

    def test_batch_del(self):
        """
        批量删除
        """
        data = dict(
            task_ids=[1, 4],
            user_id=1
        )
        resp = self.fetch('/tasks/batch_del/', data=data, method='DELETE')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_dashboard(self):
        """
        dashboard
        """
        resp = self.fetch('/tasks/dashboard/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_dashboard_detail(self):
        """
        不添加参数
        """
        resp = self.fetch('/tasks/dashboard_detail/', data={}, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_dashboard_detail_with_params(self):
        """
        添加参数
        """
        data = dict(
            start_date='2019-09-25',
            end_date='2019-09-29'
        )
        resp = self.fetch('/tasks/dashboard_detail/', data=data, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200

    def test_dashboard_detail_with_stamps(self):
        """
        添加参数
        """
        data = dict(
            start_date=1572883199000000,
            end_date=1570733200000000
        )
        resp = self.fetch('/tasks/dashboard_detail/', data=data, method='GET')
        resp_obj = json.loads(resp.text)
        print(json.dumps(resp_obj, ensure_ascii=False, indent=4))
        assert resp.status_code == 200
