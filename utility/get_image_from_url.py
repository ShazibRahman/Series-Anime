from pathlib import Path

import requests
from bs4 import BeautifulSoup

IMAGE_PATH = Path(__file__).parent.parent.joinpath("images")  # utility  # src
if not IMAGE_PATH.exists():
    IMAGE_PATH.mkdir()


def get_image_from_url(session: requests.Session, url: str) -> Path | None:
    """
    Downloads the image of the anime from the given URL and returns the path to the saved image.

    Args:
        session (requests.Session): The session to use for making the request.
        url (str): The URL of the anime page.

    Returns:
        Path | None: The path to the saved image if the image is downloaded successfully, else None.
    """
    html = session.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img", id="big_image")
    return _save_image_from_url(img["src"])


def _save_image_from_url(url: str) -> Path | None:
    """
    Downloads an image from the given URL and saves it to the images folder.

    If the image already exists in the images folder, it is not downloaded again.
    Instead, the path to the existing image is returned.

    Args:
        url (str): The URL of the image to download.

    Returns:
        Path | None: The path to the downloaded image if it is downloaded successfully, else None.
    """
    if url is None or url == "":
        return None
    image_name = url.split("/")[-1]
    image_path = IMAGE_PATH.joinpath(image_name)
    if image_path.exists():
        return image_path
    with open(image_path, "wb") as file:
        file.write(requests.get(url, timeout=10).content)
    return image_path
