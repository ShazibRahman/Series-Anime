"""
This module contains functions for checking if events have already been added for the month.
"""

import datetime
import io

import json
import pathlib
from json import JSONDecodeError

DATA_FOLDER = pathlib.Path(__file__).parent.parent.joinpath("data")

if not DATA_FOLDER.exists():
    DATA_FOLDER.mkdir()

EVENTS_FILE = DATA_FOLDER.joinpath("events.json")


def __read_json_file(file_path):
    """
    Reads the given file and returns its content as a JSON object.

    If the file does not exist or its content is not valid JSON,
    the function will return an empty list.
    """
    try:
        with io.open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, JSONDecodeError) as e:
        print(repr(e))
        return []


def __write_json_file(file_path, data):
    with io.open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def check_if_events_already_added_for_the_month(month: datetime.date) -> bool:
    """
    This function checks if the events have already been added for the month.
    :param month: datetime.date
    :return: bool
    """
    allowed_dates = [month.replace(day=1), month.replace(day=15)]
    events: list = __read_json_file(EVENTS_FILE)

    # Check if events for allowed dates are already added
    for allowed_date in allowed_dates:
        if str(allowed_date) not in events and allowed_date <= month:
            events.append(str(allowed_date))
            __write_json_file(EVENTS_FILE, events)
            return False

    return True


if __name__ == "__main__":
    print(
        check_if_events_already_added_for_the_month(
            datetime.datetime.now().date().replace(day=16)
        )
    )
