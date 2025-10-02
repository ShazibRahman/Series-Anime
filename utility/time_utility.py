"""
This module contains utility functions for time related tasks.
"""

import calendar
from datetime import date, datetime

day_name_list = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


# suppose I pass sunday as the day_name to the function match_current_day(day_name: str) -> bool
def match_current_day(day_name: str) -> bool:
    """
    This function takes a day_name and returns True if the day_name matches the current day, else False
    :param day_name: str
    :return: bool
    """

    return calendar.day_name[datetime.now().weekday()] == day_name


def get_current_day() -> str:
    """
    This function returns the current day
    :return: str
    """

    return calendar.day_name[datetime.now().weekday()]


def get_no_of_days_between_current_day_and_day(day_name: str) -> int:
    """
    This function returns the number of days between the current day and the day_name
    :param day_name: str
    :return: int
    """
    current_day = get_current_day()
    current_day_index = day_name_list.index(current_day)
    day_name_index = day_name_list.index(day_name)
    return day_name_index - current_day_index


def get_current_month_day_as_int() -> int:
    """
    This function returns the current date
    :return: str
    """
    return datetime.now().day


def get_last_day_of_month_as_int() -> int:
    """
    This function returns the last day of the current month
    :return: int
    """
    today = datetime.now()
    return calendar.monthrange(today.year, today.month)[1]


def get_current_month_range() -> tuple:
    """
    This function returns the first and last day of the current month
    :return: tuple
    """
    today = datetime.now()
    return calendar.monthrange(today.year, today.month)


def get_current_date() -> date:
    """
    This function returns the current date
    :return: datetime
    """
    return datetime.now().date()


def get_current_year() -> int:
    """
    This function returns the current year
    :return: int
    """
    return datetime.now().year


def get_current_month() -> int:
    """
    This function returns the current month
    :return: int
    """
    return datetime.now().month


def merge_time_str_datetime_date(time_str: str, day: date) -> datetime:
    """
    Merges a time string and a date object into a single formatted datetime string.

    Parameters
    ----------
    time_str : str
        The time string in the format "H:MMam/pm" (e.g., "7:30pm").
    day : datetime.date
        The date object representing the date.

    Returns
    -------
    str
        A formatted datetime string in the format "YYYY-MM-DD HH:MMam/pm".
    """
    date_time_series = datetime.strptime(time_str, "%I:%M%p")
    combined_datetime = datetime.combine(day, date_time_series.time())
    return combined_datetime


if __name__ == "__main__":
    print(match_current_day("Sunday"))
