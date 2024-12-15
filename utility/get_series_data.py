"""
This module contains functions for retrieving series data from next episode.
"""

import datetime
import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def get_series_data_for_current_day(page_content: str) -> list:
    """
    This function takes the page content of the calendar page
    from next episode and returns a list of tuples.
    Each tuple contains the name of the show, the l
    ink to the show and the time of the show.
    If the page content doesn't contain the anchor
    tag with the name "today", it will return an empty list

    Args:
        page_content (str):
        The page content of the calendar page from next episode.

    Returns:
        list: A list of tuples. Each tuple contains the name of the show,
        the link to the show and the time of the show.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    today_anchor: Tag = soup.find("a", {"name": "today"})
    if today_anchor:
        parent = today_anchor.parent

        shows = parent.find_all("div", class_="cal_name")
        times = parent.find_all("div", class_="cal_more")
        return [
            (
                show.find("a").text,
                _modify_link(show.find("a")["href"]),
                TIME.find("div", class_="h").text,
            )
            for show, TIME in zip(shows, times)
        ]
    else:
        return []


# not being used don't use it for now
def get_series_data_for_today_and_next_no_of_days_within_a_week(
    page_content: str, no_of_days: int
) -> list:
    """
    This function takes the page content of the calendar page
    from next episode and the number of days to retrieve
    and returns a list of tuples. Each tuple contains the name of the show,
    the link to the show and the time of the show
    for the next number of days.

    Args:
        page_content (str): The page content of the calendar page from next episode.
        no_of_days (int): The number of days for which the series data should be retrieved.

    Returns:
        list: A list of tuples. Each tuple contains the name of the show,
        the link to the show and the time of the show.
    """
    soup = BeautifulSoup(page_content, "html.parser")
    today_anchor: Tag = soup.find("a", {"name": "today"})
    series_data = []
    day_data: Tag
    if today_anchor:
        parent = today_anchor.parent
        day_data = parent

        shows = day_data.find_all("div", class_="cal_name")
        times = day_data.find_all("div", class_="cal_more")
        days_to_add_in_time = [0] * len(shows)
        series_data.extend(
            [
                (
                    show.find("a").text,
                    _modify_link(show.find("a")["href"]),
                    TIME.find("div", class_="h").text,
                    day,
                )
                for show, TIME, day in zip(shows, times, days_to_add_in_time)
            ]
        )
    for i in range(1, no_of_days + 1):
        day_data = day_data.next_sibling.next_sibling  # noqa
        shows = day_data.find_all("div", class_="cal_name")
        times = day_data.find_all("div", class_="cal_more")
        days_to_add_in_time = [i] * len(shows)
        series_data.extend(
            [
                (
                    show.find("a")["title"],
                    _modify_link(show.find("a")["href"]),
                    time_series.find("div", class_="h").text,
                    day,
                )
                for show, time_series, day in zip(shows, times, days_to_add_in_time)
            ]
        )

    return series_data


def get_series_data_for_the_current_month_btw_start_date_end_date(
    page_content: str, start_date, end_date
) -> list:
    """
    This function takes the page content of the calendar page
    from next episode and a start date and an end date
    and returns a list of tuples. Each tuple contains the name of the show,
    the link to the show and the time of the show
    for the days between the start date and the end date.

    Args:
        page_content (str): The page content of the calendar page from next episode.
        start_date (int): The start date of the range of days.
        end_date (int): The end date of the range of days.

    Returns:
        list: A list of tuples. Each tuple contains the name of the show,
        the link to the show and the time of the show.
    """
    print(start_date, end_date)
    soup = BeautifulSoup(page_content, "html.parser")
    spans = soup.find_all("span")
    series_data = []

    for span in spans:
        if (
            span.string and span.string.strip().isdigit()
        ):  # Check if the span contains a number (the day)
            day = span.string.strip()
            if start_date <= int(day) <= end_date:
                day_data_td = span.parent.parent
                shows = day_data_td.find_all("div", class_="cal_name")
                times = day_data_td.find_all("div", class_="cal_more")
                day_list = [int(day)] * len(shows)
                series_data.extend(
                    [
                        (
                            show.find("a")["title"],
                            _modify_link(show.find("a")["href"]),
                            TIME.find("div", class_="h").text,
                            day,
                        )
                        for show, TIME, day in zip(shows, times, day_list)
                    ]
                )

    return series_data


def get_series_data_for_the_current_month_btw_start_date_end_date_v2(
    page_content: str, start_date, end_date, month: int, year: int
) -> list:
    """
    This function takes the page content of the calendar page from next episode, a start date and end date
    and the month and year, and returns a list of tuples. Each tuple contains the name of the show,
    the link to the show and the time of the show for the next number of days.

    Args:
        page_content (str): The page content of the calendar page from next episode.
        start_date (int): The start date of the range of days.
        end_date (int): The end date of the range of days.
        month (int): The month of the year.
        year (int): The year.

    Returns:
        list: A list of tuples. Each tuple contains the name of the show, the link to the show and the time of the show.
    """

    print(month, year)
    soup = BeautifulSoup(page_content, "html.parser")
    spans = soup.find_all("span")
    series_data = []

    today_date: datetime.date = datetime.date.today().replace(month=month, year=year)

    for span in spans:
        if (
            span.string and span.string.strip().isdigit()
        ):  # Check if the span contains a number (the day)
            day = span.string.strip()
            if start_date <= int(day) <= end_date:
                day_data_td = span.parent.parent
                shows = day_data_td.find_all("div", class_="cal_name")
                times = day_data_td.find_all("div", class_="cal_more")
                day_to_add_to_list = today_date.replace(day=int(day))
                day_list = [day_to_add_to_list] * len(shows)
                series_data.extend(
                    [
                        (
                            show.find("a")["title"],
                            _modify_link(show.find("a")["href"]),
                            TIME.find("div", class_="h").text,
                            day,
                        )
                        for show, TIME, day in zip(shows, times, day_list)
                    ]
                )

    return series_data


def get_series_for_year(session: requests.session, year: int):
    """
    This generator function takes a requests session and a year and returns a generator that returns a list of tuples for each month in the given year.
    The list of tuples contains the name of the show, the link to the show and the time of the show.
    The days are filtered so that only the days between the start date and the end date are included.
    If the page content doesn't contain the anchor tag with the name "today", it will return an empty list

    Args:
        session (requests.session): The requests session.
        year (int): The year.

    Yields:
        list: A list of tuples. Each tuple contains the name of the show, the link to the show and the time of the show.
    """
    base_url = "https://next-episode.net/calendar/"

    start_month, end_month = get_appropriate_month_range(year)

    for month_loop in range(start_month, end_month + 1):
        start_time = time.time()
        response = session.get(base_url, params={"year": year, "month": month_loop})
        print(f"time taken = {time.time() - start_time}")
        if response.status_code == 200:
            yield get_series_data_for_the_current_month_btw_start_date_end_date_v2(
                response.text, 1, 31, month_loop, year
            )
        else:
            yield []


def get_appropriate_month_range(year) -> tuple[int, int]:
    """
    Determines the appropriate start and end month range for a given year.

    If the specified year is in the past, the function returns a start month of 13,
    effectively preventing any loop from running for that year. If the specified year
    is the current year, the start month is set to the current month. Otherwise, the
    start month is set to January and the end month is set to December.

    Args:
        year (int): The year for which the month range is to be determined.

    Returns:
        tuple[int, int]: A tuple containing the start and end month.
    """
    today_date = datetime.date.today()
    current_year = today_date.year
    current_month = today_date.month
    start_month, end_month = 1, 12
    if current_year > year:
        start_month = 13  # returning 13 so that loop won't run for the past year
    if current_year == year:
        start_month = current_month
    return start_month, end_month


def _modify_link(link: str) -> str:
    return f"https:{link}"


if __name__ == "__main__":
    print(get_appropriate_month_range(2020))
