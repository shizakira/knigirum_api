import pytest
import requests

URL = "http://188.120.241.222:8534/books"

"""Проверка параметров"""


# Тестирование параметра limit
def test_limit():
    response = requests.get(url=URL, params={"limit": 5})
    assert response.status_code == 200
    data = response.json()["products"]
    assert len(data) == 5


# Тестирование параметра offset
def test_offset():
    response = requests.get(url=URL, params={"offset": 5})
    assert response.status_code == 200
    data = response.json()["products"]
    assert data[0]["id"] == 6 and len(data) == 45


# Тестирование параметра sort
@pytest.mark.parametrize("value", [
    ("title"),
    ("author"),
    ("price")
])
def test_sort(value):
    response = requests.get(url=URL, params={"sort": value})
    assert response.status_code == 200
    data = response.json()["products"]
    values = [product[value] for product in data]
    assert values == sorted(values)


# Тестирование параметра order
@pytest.mark.parametrize("sort_value, order_value", [
    ("title", "ASC"),
    ("author", "ASC"),
    ("price", "ASC"),
    ("title", "DESC"),
    ("author", "DESC"),
    ("price", "DESC")
])
def test_order(sort_value, order_value):
    response = requests.get(url=URL, params={"sort": sort_value, "order": order_value})
    assert response.status_code == 200
    data = response.json()["products"]
    values = [product[sort_value] for product in data]
    flag = True if order_value == "DESC" else False
    assert values == sorted(values, reverse=flag)


# Тестирование параметра minPrice
def test_min_price():
    response = requests.get(url=URL, params={"minPrice": 700})
    assert response.status_code == 200
    data = response.json()["products"]
    for product in data:
        assert product["price"] >= 700


# Тестирование параметра maxPrice
def test_max_price():
    response = requests.get(url=URL, params={"maxPrice": 700})
    assert response.status_code == 200
    data = response.json()["products"]
    for product in data:
        assert product["price"] <= 700


# Тестирование параметра string
@pytest.mark.parametrize("substring", [
    ("Лавкрафт"),
    ("бе"),
    ("Оно"),
    ("xyz")
])
def test_string(substring):
    response = requests.get(url=URL, params={"string": substring})
    assert response.status_code == 200
    data = response.json()["products"]
    if substring == "xyz":
        assert not data
    else:
        for product in data:
            assert substring in product["author"] or substring in product["title"]


"""Проверка границ значений параметров:"""


# Проверка границ параметра limit
@pytest.mark.parametrize("value, expected_result", [
    (0, 0),
    (1, 1),
    (49, 49),
    (50, 50)
])
def test_limit_borders(value, expected_result):
    response = requests.get(url=URL, params={"limit": value})
    assert response.status_code == 200
    data = response.json()["products"]
    assert len(data) == expected_result


# Проверка границ параметра offset
@pytest.mark.parametrize("value, expected_result, id", [
    (0, 50, 1),
    (1, 49, 2),
    (49, 1, 50),
    (50, 0, None)
])
def test_offset_borders(value, expected_result, id):
    response = requests.get(url=URL, params={"offset": value})
    assert response.status_code == 200
    data = response.json()["products"]
    assert len(data) == expected_result
    if id:
        assert data[0]['id'] == id


# Проверка границ параметра minPrice
@pytest.mark.parametrize("value, expected_result", [
    (0, 50),
    (410, 50),
    (411, 49),
    (1190, 2),
    (1200, 1),
    (1201, 0)
])
def test_min_price_borders(value, expected_result):
    response = requests.get(url=URL, params={"minPrice": value})
    assert response.status_code == 200
    data = response.json()["products"]
    assert len(data) == expected_result
    for product in data:
        assert product["price"] >= value


# Проверка границ параметра maxPrice
@pytest.mark.parametrize("value, expected_result", [
    (0, 0),
    (410, 1),
    (411, 1),
    (1190, 49),
    (1200, 50),
    (1201, 50)
])
def test_max_price_borders(value, expected_result):
    response = requests.get(url=URL, params={"maxPrice": value})
    assert response.status_code == 200
    data = response.json()["products"]
    assert len(data) == expected_result
    for product in data:
        assert product["price"] <= value


"""Негативные тесты"""


# Негативный тест параметра limit
@pytest.mark.parametrize("value", [
    ("пять"),
    (-1)
])
def test_negative_limit(value):
    response = requests.get(url=URL, params={"limit": value})
    assert response.status_code == 400


# Негативный тест параметра offset
@pytest.mark.parametrize("value", [
    ("!!!"),
    (-1)
])
def test_negative_offset(value):
    response = requests.get(url=URL, params={"offset": value})
    assert response.status_code == 400


# Негативный тест параметра sort
@pytest.mark.parametrize("value", [
    ("ASC"),
    (-1)
])
def test_negative_sort(value):
    response = requests.get(url=URL, params={"sort": value})
    assert response.status_code == 400


# Негативный тест параметра order
@pytest.mark.parametrize("order_value", [
    ("true"),
    (-1)
])
def test_negative_order(order_value):
    response = requests.get(url=URL, params={"order": order_value, "sort": "price"})
    assert response.status_code == 400


# Негативный тест параметра minPrice
@pytest.mark.parametrize("value", [
    ("#@"),
    (-1)
])
def test_negative_min_price(value):
    response = requests.get(url=URL, params={"minPrice": value})
    assert response.status_code == 400


# Негативный тест параметра maxPrice
@pytest.mark.parametrize("value", [
    ("ten"),
    (-1)
])
def test_negative_max_price(value):
    response = requests.get(url=URL, params={"maxPrice": value})
    assert response.status_code == 400


# Негативный тест отправки запроса с телом
def test_request_with_json():
    payload = {"text": "helloworld"}
    response = requests.get(URL, json=payload)
    data = response.json()["products"]
    assert response.status_code == 200
    assert len(data) == 50
