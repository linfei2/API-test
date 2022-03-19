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
    json_response = response.json()
    return response, json_response["accessToken"]


def test_register_api_client(register_api_client):
    response, access_token = register_api_client
    assert response.status_code == 201
    assert access_token


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


@pytest.fixture
def authorize(register_api_client):
    response, access_token = register_api_client
    headers = {"Authorization": "Bearer " + access_token}
    return headers


@pytest.fixture
def submit_order(base_url, authorize):
    url = base_url + "/orders"
    headers = authorize
    order_details = {"bookId": 1, "customerName": "John"}
    response = requests.post(url, json=order_details, headers=headers)
    json_response = response.json()
    order_id = json_response["orderId"]
    return response, order_id, headers


def test_submit_order(submit_order):
    response, order_id, headers = submit_order
    assert response.status_code == 201
    assert order_id


def test_get_all_orders(base_url, authorize):
    url = base_url + "/orders"
    headers = authorize
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_get_single_order(base_url, submit_order):
    response, order_id, headers = submit_order
    url = base_url + f"/orders/{order_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

