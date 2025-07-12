"""
A module for Adding Anime from next episode to google calendar.
"""

import logging
import os
import time
from datetime import datetime

# Move all import statements here
from log import logconfig  # disable=unused-import
from utility import time_utility
from utility.add_event_to_google_calendar import add_event_from_data_series
from utility.file_data_utility import check_if_events_already_added_for_the_month
from utility.get_series_data import get_series_for_year
from utility.lock_manager import lock_manager_decorator
from utility.login import login_user
from utility.pickle_utility import get_pickled_stored_record, save_pickled_record

LOGIN_URL = "https://next-episode.net/userlogin"
USERNAME = os.getenv("next_user")
PASSWORD = os.getenv("next_password")
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CUR_DIR)


@lock_manager_decorator(os.path.join(CUR_DIR, "series.lock"))
def main():
    """Main function to execute the script for adding anime events to Google Calendar."""
    start_time = time.time()

    if not check_if_events_already_added_for_the_month(time_utility.get_current_date()) or True:
        start_time = time.time()
        s = login_user(USERNAME, PASSWORD, LOGIN_URL)
        # clean_up()
        pickled_record = get_pickled_stored_record()

        print("Getting series for the year")

        current_year = time_utility.get_current_year()
        current_month = datetime.now().month

        # Get series for the current year
        for data in get_series_for_year(s, current_year, pickled_record):

            add_event_from_data_series(data)

        # If the current month is after September, get series for the next year
        if current_month > 9:  # After September
            next_year = current_year + 1
            print("Getting series for the next year")
            for data in get_series_for_year(s, next_year, pickled_record):

                add_event_from_data_series(data)

        save_pickled_record(pickled_record)

    logging.info("Finished the script in %s secs", time.time() - start_time)


if __name__ == "__main__":

    piclded = {}
    main()
