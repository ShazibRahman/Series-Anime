"""
This module provides functionality to download images from a given URL and save them to a local directory.

Functions:
    get_image_from_url(session: requests.Session, url: str) -> Path | None:
        Downloads the image of the anime from the given URL and returns the path to the saved image.

    _save_image_from_url(url: str) -> Path | None:
        Downloads an image from the given URL and saves it to the images folder.
"""

from pathlib import Path
import asyncio
import logging

import aiofiles
import httpx
from bs4 import BeautifulSoup

from .series_to_image_mapping import SeriesToImageMapping

logger = logging.getLogger(__name__)

IMAGE_PATH = Path(__file__).parent.parent.joinpath("images")  # utility  # src
if not IMAGE_PATH.exists():
    IMAGE_PATH.mkdir()


series_to_image_mapping = SeriesToImageMapping()


async def _get_image_from_url(session: httpx.AsyncClient, url: str) -> Path | None:
    """
    Downloads the image of the anime from the given URL asynchronously
    and returns the path to the saved image.
    """

    image_mapping = series_to_image_mapping.get_mapping()
    if image_mapping is None:
        image_mapping = {}

    image_name = url.split("/")[-1]
    image_path = IMAGE_PATH.joinpath(image_name + ".jpg")

    if image_path.exists():
        logger.info("Image {} already exists, skipping download.".format(image_name))
        image_mapping[url] = str(image_path)

        return image_path

    # async with session.get(url) as resp:
    #     html = await resp.text()
    intermediate_response = await session.get(url)
    html = intermediate_response.text
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img", id="big_image")
    if not img or not img.get("src"):
        return None

    image_path = await _save_image_from_url(session, str(img["src"]))
    if image_path:
        image_mapping[url] = str(image_path)
    return image_path


async def _save_image_from_url(session: httpx.AsyncClient, url: str) -> Path | None:
    if not url:
        return None

    image_name = url.split("/")[-1]
    image_path = IMAGE_PATH.joinpath(image_name)

    if image_path.exists():
        logger.info("Image {} already exists, skipping download.".format(image_name))
        return image_path

    resp = await session.get(url)
    content = resp.content  # bytes directly

    async with aiofiles.open(image_path, "wb") as f:
        await f.write(content)

    return image_path


async def _bulk_download(urls: list[str]) -> None:
    """
    Downloads anime images from multiple page URLs concurrently.
    """
    async with httpx.AsyncClient(http2=True) as client:
        tasks = [_get_image_from_url(client, url) for url in urls]
        if len(tasks) != 0:
            await asyncio.gather(*tasks)

    # async with aiohttp.ClientSession() as session:
    #     tasks = [_get_image_from_url(session, url) for url in urls]
    #     if len(tasks) != 0:
    #         await asyncio.gather(*tasks)


def download_image_from_urls(urls: list[str]) -> dict | None:
    # test_urls = [
    #     "https://next-episode.net/wednesday",
    #     "https://next-episode.net/alice-in-borderland",
    #     "https://next-episode.net/my-hero-academia",
    # ]

    image_mapping = series_to_image_mapping.get_mapping()
    if image_mapping is None:
        image_mapping = {}

    final_urls = set(urls)
    final_urls = [url for url in final_urls if url not in image_mapping]
    print("Final URLs to download:", final_urls)
    if not final_urls and len(final_urls) == 0:
        return None
    asyncio.run(_bulk_download(final_urls))
    return None


# Example usage
if __name__ == "__main__":
    print(download_image_from_urls)
