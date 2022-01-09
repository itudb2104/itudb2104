from datetime import datetime
import requests
import wikipedia
from bs4 import BeautifulSoup

# 29/05/1999 -> 22


def calculate_age(birthday):
    print(birthday)
    year, month, day = int(birthday.split(
        '-')[0]), int(birthday.split('-')[1]), int(birthday.split('-')[2])
    today = datetime.now()
    age = today.year - year - 1
    if today.month > month or (today.month == month and today.day >= day):
        age += 1
    return age


def get_description_by_isbn(isbn):
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    resp = requests.get(api + isbn)
    book_data = resp.json()
    volume_info = book_data["items"][0]["volumeInfo"]
    description = volume_info["description"]
    return description


# Get information of author by authorName from wikipedia
def get_description_of_author(authorName):
    wikipedia.set_lang("en")
    search = wikipedia.search(authorName)
    if len(search) == 0:
        return ""
    search = search[0]
    if '.' in search:
        search = search.split('.')
        search = "._".join(search)
    try:
        result = wikipedia.page(search)
        description = result.summary
    except:
        return ""
    return result.summary


def get_image_url_of_author(authorName):
    wikipedia.set_lang("en")
    search = wikipedia.search(authorName)
    if len(search) == 0:
        return ""
    search = search[0]
    if '.' in search:
        search = search.split('.')
        search = "._".join(search)
    try:
        result = wikipedia.page(search)
    except:
        return ""
    try:
        images = result.images
    except:
        return ""
    for name in authorName.split():
        if '.' in name:
            continue
        else:
            search_name = name
            break
    images = list(filter(lambda image: search_name.lower() in image.lower(
    ) and 'and' not in image.lower() and 'house' not in image, images))
    if len(images) > 0:
        return sorted(images, key=len)[0]
    else:
        return None


def get_birthday_of_author(authorName):
    url = "https://en.wikipedia.org/wiki/" + authorName
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    birthday = soup.find("span", {"class": "bday"})
    try:
        birthday = birthday.text
        return birthday
    except:
        return ""


# print(get_description_of_author("J.K. Rowling"))
# print(get_image_url_of_author("J.K. Rowling"))
# print(get_birthday_of_author("J.K. Rowling"))
