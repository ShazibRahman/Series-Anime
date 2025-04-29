"""
This module contains functions for logging into a website.
"""

import requests


def login_user(username: str, password: str, login_url: str) -> requests.Session:
    """
    Logs into a website using the provided username and password and returns an authenticated requests session.

    Args:
        username (str): The username for logging in.
        password (str): The password for logging in.
        login_url (str): The URL to send the login request to.

    Returns:
        requests.Session: An authenticated session if the login is successful.
    """
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    session.post(login_url, data={"username": username, "password": password}, headers=headers)
    return session
