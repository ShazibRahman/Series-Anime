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
    session.post(login_url, data={'username': username, 'password': password})
    return session
