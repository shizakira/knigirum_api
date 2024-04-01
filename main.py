import requests
from icecream import ic


class HttpGetter:
    def __init__(self, base_url):
URL = "http://188.120.241.222:8534/books"


# Запрос без параметров
def send_request_without_params():
    response = requests.get(URL)

    status_code = response.status_code
    data = response.json()

    ic(status_code, data)


def send_request_with_json():
    payload = {"anything": "O_o"}
    response = requests.get(url=URL, json=payload)

    status_code = response.status_code
    data = response.json()

    ic(status_code, data)


def send_request_offset():
    response = requests.get(url=URL, params={"offset": 25})

    data = response.json()
    ic(len(data["products"]))
    for i, product in enumerate(data["products"], 1):
        ic(i)
        assert 'author_bio' in product
        for key, value in product.items():
            if key != 'author_bio':
                ic(key, value)


def formating(params):
    return "?" + "&".join(params.split())

print(formating("limit=20	offset=5	sort=author	order=ASC	minPrice=600	maxPrice=1000	string=в"))
