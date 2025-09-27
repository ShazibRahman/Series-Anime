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

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from .pickle_utility import (
    get_picked_series_to_image_mapping,
    save_picked_series_to_image_mapping,
)

IMAGE_PATH = Path(__file__).parent.parent.joinpath("images")  # utility  # src
if not IMAGE_PATH.exists():
    IMAGE_PATH.mkdir()


async def _get_image_from_url(
    session: aiohttp.ClientSession, url: str, image_mapping: dict[str, str]
) -> Path | None:
    """
    Downloads the image of the anime from the given URL asynchronously
    and returns the path to the saved image.
    """
    async with session.get(url) as resp:
        html = await resp.text()
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find("img", id="big_image")
    if not img or not img.get("src"):
        return None
    image_path = await _save_image_from_url(session, img["src"])
    if image_path:
        image_mapping[url] = str(image_path)
    return image_path


async def _save_image_from_url(session: aiohttp.ClientSession, url: str) -> Path | None:
    """
    Downloads an image from the given URL asynchronously and saves it to the images folder.
    """
    if not url:
        return None

    image_name = url.split("/")[-1]
    image_path = IMAGE_PATH.joinpath(image_name)

    if image_path.exists():
        return image_path

    async with session.get(url) as resp:
        content = await resp.read()
        async with aiofiles.open(image_path, "wb") as f:
            await f.write(content)

    return image_path


async def _bulk_download(urls: list[str], image_mapping: dict) -> dict[str, str]:
    """
    Downloads anime images from multiple page URLs concurrently.
    """

    unique_urls = set(urls)
    async with aiohttp.ClientSession() as session:
        tasks = [
            _get_image_from_url(session, url, image_mapping)
            for url in unique_urls
            if url not in image_mapping
        ]
        if len(tasks) != 0:
            await asyncio.gather(*tasks)
        save_picked_series_to_image_mapping(image_mapping)

        return image_mapping


def download_image_from_urls(urls: list[str]) -> dict[str, str]:
    # test_urls = [
    #     "https://next-episode.net/wednesday",
    #     "https://next-episode.net/alice-in-borderland",
    #     "https://next-episode.net/my-hero-academia",
    # ]

    image_mapping = get_picked_series_to_image_mapping()

    final_urls = set(urls)
    final_urls = [url for url in final_urls if url not in image_mapping]
    print("Final URLs to download:", final_urls)
    if not final_urls and len(final_urls) == 0:
        return image_mapping
    results = asyncio.run(_bulk_download(urls, image_mapping))
    return results


# Example usage
if __name__ == "__main__":
    print(download_image_from_urls)
