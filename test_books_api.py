import pytest
import requests


def test_register_api_client(base_url):
    url = base_url + "/api-clients/"
    data = {"clientName": "Jorge", "clientEmail": "jgarcia@example.com"}
    resp = requests.post(url, json=data)
    j = resp.json()
    assert resp.status_code == 201
    assert j["accessToken"]







