import json

import pytest
import requests


class API:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}

    def post(self, endpoint, data, *args, **kwargs):
        data = json.dumps(data)
        return requests.post(f'{self.base_url}/{endpoint}',
                             data=data, headers=self.headers,
                             *args, **kwargs)

    def get(self, endpoint, *args, **kwargs):
        return requests.get(f'{self.base_url}/{endpoint}', *args, **kwargs)

    def patch(self, endpoint, data, *args, **kwargs):
        data = json.dumps(data)
        return requests.patch(f'{self.base_url}/{endpoint}',
                             data=data, headers=self.headers,
                             *args, **kwargs)


@pytest.fixture
def api():
    return API('http://localhost:8080')


def test_post(api):
    data = {
        "user_id": 102,
        "product_ids": [10, 20, 30]
    }
    resp = api.post('api/v1/order', data=data)
    assert resp.status_code == 201
    resp_data = resp.json()
    resp_data.pop('order_id')
    assert data == resp_data


def test_get(api):
    data = {
        "order_id": 10,
        "user_id": 1,
        "status": "accepted",
        "product_ids": [
            0, 1, 2, 3, 4
        ]
    }
    resp = api.get(f'api/v1/order/{data["order_id"]}')
    assert resp.status_code == 200
    assert data == resp.json()


def test_patch(api):
    order_id = 10
    data = {"status": "delivery"}
    resp = api.patch(f'api/v1/order/{order_id}', data=data)
    assert resp.status_code == 200
    data['order_id'] = order_id
    assert data == resp.json()
    api.patch(f'api/v1/order/{order_id}', data={"status": "accepted"})
