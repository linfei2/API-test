import pytest
import requests
import random
import string


@pytest.fixture
def generate_random_name():
    name = "".join(random.choices(string.ascii_letters, k=6))
    return name


@pytest.fixture
def generate_random_email():
    email = "".join(random.choices(string.ascii_lowercase, k=6)) + "@email.com"
    return email


@pytest.fixture
def register_api_client(base_url, generate_random_name, generate_random_email):
    url = base_url + "/api-clients/"
    name = generate_random_name
    email = generate_random_email
    data = {"clientName": name, "clientEmail": email}
    resp = requests.post(url, json=data)
    return resp


def test_register_api_client(register_api_client):
    resp = register_api_client
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
