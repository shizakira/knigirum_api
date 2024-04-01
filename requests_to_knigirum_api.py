import requests
from icecream import ic

URL = "http://188.120.241.222:8534/books"


def get_books_sort_title():
    response = requests.get(url=URL, params={"sort": "title"})
    assert response.status_code == 200
    titles = []
    for product in response.json()["products"]:
        titles.append(product["title"])

    return titles == sorted(titles)



ic(get_books_sort_title())