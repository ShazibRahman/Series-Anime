"""
A module for Adding Anime from next episode to google calendar.
"""

import logging
import os
import time
from datetime import datetime

import dotenv

# Move all import statements here
from utility import time_utility
from utility.add_event_to_google_calendar import (
    add_event_from_data_series,
    delete_no_longer_existing_events,
)
from utility.get_series_data import get_series_for_year, NO_LONGER_EXISTING_EVENTS
from utility.lock_manager import lock_manager_decorator
from utility.login import login_user
from utility.pickle_utility import (
    get_pickled_stored_record,
    save_pickled_record,
    get_picked_series_data,
    save_picked_series_data,
)
from log.logconfig import logger  # noqa: F401

dotenv.load_dotenv()


LOGIN_URL = os.getenv("next_login_url")
USERNAME = os.getenv("next_user")
PASSWORD = os.getenv("next_password")
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CUR_DIR)


@lock_manager_decorator(os.path.join(CUR_DIR, "series.lock"))
def main():
    """Main function to execute the script for adding anime events to Google Calendar."""

    start_time = time.time()
    s = login_user(USERNAME, PASSWORD, LOGIN_URL)
    # clean_up()
    pickled_record = get_pickled_stored_record()

    series_old_data = get_picked_series_data()

    print("Getting series for the year")

    current_year = time_utility.get_current_year()
    current_month = datetime.now().month

    # Get series for the current year
    for data in get_series_for_year(s, current_year, pickled_record, series_old_data):

        add_event_from_data_series(data)

    month_limiter = -7 + current_month
    next_year = current_year + 1
    print("Getting series for the next year")
    for data in get_series_for_year(
        s, next_year, pickled_record, series_old_data, month_limiter
    ):  # till the month limiter

        add_event_from_data_series(data)

    save_pickled_record(pickled_record)

    save_picked_series_data(series_old_data)

    if NO_LONGER_EXISTING_EVENTS:
        logging.info(
            "No longer existing events size: %d", len(NO_LONGER_EXISTING_EVENTS)
        )
        print(NO_LONGER_EXISTING_EVENTS)
        delete_no_longer_existing_events(NO_LONGER_EXISTING_EVENTS)
    else:
        logging.info("No events to delete.")

    logging.info("Finished the script in %.2f secs", time.time() - start_time)


if __name__ == "__main__":

    main()
