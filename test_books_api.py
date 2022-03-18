import random
import string

import pytest
import requests


@pytest.fixture
def random_name():
    name = "".join(random.choices(string.ascii_letters, k=6))
    return name


@pytest.fixture
def random_email():
    email = "".join(random.choices(string.ascii_lowercase, k=6)) + "@email.com"
    return email


@pytest.fixture
def register_api_client(base_url, random_name, random_email):
    url = base_url + "/api-clients/"
    data = {"clientName": random_name, "clientEmail": random_email}
    response = requests.post(url, json=data)
    return response


@pytest.fixture
def test_register_api_client(register_api_client):
    response = register_api_client
    json_response = response.json()
    assert response.status_code == 201
    if json_response["accessToken"]:
        return json_response["accessToken"]


def test_get_all_books(base_url):
    url = base_url + "/books"
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize("book_id", [1, 6])
def test_get_valid_book(base_url, book_id):
    url = base_url + f"/books/{book_id}"
    response = requests.get(url)
    assert response.status_code == 200


def test_get_invalid_book(base_url, book_id=50):
    url = base_url + f"/books/{book_id}"
    response = requests.get(url)
    json_response = response.json()
    assert response.status_code == 404
    assert json_response["error"] == f"No book with id {book_id}"


def test_submit_order(base_url, test_register_api_client):
    url = base_url + "/orders"
    headers = {"Authorization": "Bearer " + test_register_api_client}
    order_details = {"bookId": 1, "customerName": "John"}
    response = requests.post(url, json=order_details, headers=headers)
    assert response.status_code == 201
