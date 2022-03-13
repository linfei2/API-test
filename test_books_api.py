import pytest
import requests


def test_register_api_client(base_url):
    url = base_url + "/api-clients/"
    data = {"clientName": "Jorge", "clientEmail": "jgarcia@example.com"}
    resp = requests.post(url, json=data)
    j = resp.json()
    assert resp.status_code == 201
    assert j["accessToken"]


def test_get_all_books(base_url):
    url = base_url + "/books"
    resp = requests.get(url)
    assert resp.status_code == 200


@pytest.mark.parametrize("book_id", [1, 6])
def test_get_valid_book(base_url, book_id):
    url = base_url + f"/books/{book_id}"
    resp = requests.get(url)
    assert resp.status_code == 200
