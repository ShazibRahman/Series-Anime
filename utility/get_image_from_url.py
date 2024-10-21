from pathlib import Path

import requests
from bs4 import BeautifulSoup

IMAGE_PATH = (Path(__file__)
              .parent  # utility
              .parent  # src
              .joinpath("images"))
if not IMAGE_PATH.exists():
    IMAGE_PATH.mkdir()


def get_image_from_url(session: requests.Session, url: str) -> Path | None:
    html = session.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img', id="big_image")
    return _save_image_from_url(img['src'])


def _save_image_from_url(url: str) -> Path | None:
    if url is None or url == "":
        return None
    image_name = url.split("/")[-1]
    image_path = IMAGE_PATH.joinpath(image_name)
    if image_path.exists():
        return image_path
    with open(image_path, 'wb') as file:
        file.write(requests.get(url).content)
    return image_path
