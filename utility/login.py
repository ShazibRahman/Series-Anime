"""
This module contains functions for logging into a website.
"""

import httpx


def login_user_httpx(username: str, password: str, login_url: str) -> httpx.Client:
    """
    Logs into a website using the provided username and password and returns an authenticated httpx client.

    Args:
        username (str): The username for logging in.
        password (str): The password for logging in.
        login_url (str): The URL to send the login request to.

    Returns:
        httpx.Client: An authenticated client if the login is successful.
    """
    client = httpx.Client(timeout=10.0, http2=True)
    print("trying to login")

    client.post(
        login_url, data={"username": username, "password": password}, timeout=10
    )
    return client
