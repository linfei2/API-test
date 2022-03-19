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
    return response, response.json()["accessToken"]


def test_register_api_client(register_api_client):
    response, access_token = register_api_client
    assert response.status_code == 201
    assert access_token


def test_get_all_books(base_url):
    url = base_url + "/books"
    response = requests.get(url)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize("book_id", [1, 6])
def test_get_valid_book(base_url, book_id):
    url = base_url + f"/books/{book_id}"
    response = requests.get(url)
    assert response.status_code == 200


def test_get_invalid_book(base_url, book_id=50):
    url = base_url + f"/books/{book_id}"
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["error"] == f"No book with id {book_id}"


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
    order_id = response.json()["orderId"]
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
    assert isinstance(response.json(), list)


def test_get_single_order(base_url, submit_order):
    response, order_id, headers = submit_order
    url = base_url + f"/orders/{order_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_update_order(base_url, submit_order):
    response, order_id, headers = submit_order
    url = base_url + f"/orders/{order_id}"
    data = {"customerName": "Jane"}
    patch_response = requests.patch(url, json=data, headers=headers)
    get_response = requests.get(url, headers=headers)
    assert patch_response.status_code == 204
    assert get_response.json()["customerName"] == "Jane"


def test_delete_order(base_url, submit_order):
    response, order_id, headers = submit_order
    url = base_url + f"/orders/{order_id}"
    delete_response = requests.delete(url, headers=headers)
    get_response = requests.get(url, headers=headers)
    assert delete_response.status_code == 204
    assert get_response.status_code == 404
    assert get_response.json()["error"] == f"No order with id {order_id}."
