"""
A module for Adding Anime from next episode to google calendar.
"""

import logging
import os
import time
from datetime import datetime

import dotenv
from common_dto.events import CalendarDtoPickled

# Move all import statements here
from utility import time_utility
from utility.general_util import get_anime_urls_from_events_v2
from utility.google_calendar_util import (
    add_event_from_data_series_v2,
    delete_no_longer_existing_events_v2,
)
from utility.get_series_data import get_series_for_year, NO_LONGER_EXISTING_EVENTS
from utility.lock_manager import lock_manager_decorator
from utility.login import login_user_httpx
from utility.pickle_utility import (
    get_picked_series_data,
    save_picked_series_data,
)
from utility.get_image_from_url import download_image_from_urls
from utility.series_to_image_mapping import SeriesToImageMapping
from log.logconfig import logger  # noqa: F401

dotenv.load_dotenv()


LOGIN_URL = os.getenv("next_login_url", "")
USERNAME = os.getenv("next_user", "")
PASSWORD = os.getenv("next_password", "")
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CUR_DIR)


@lock_manager_decorator(os.path.join(CUR_DIR, "series.lock"))
def main():
    """Main function to execute the script for adding anime events to Google Calendar."""

    start_time = time.time()
    s = login_user_httpx(USERNAME, PASSWORD, LOGIN_URL)

    # return
    # clean_up()
    series_old_data: dict[str, list[CalendarDtoPickled]] = get_picked_series_data()

    print("Getting series for the year")

    current_year = time_utility.get_current_year()
    current_month = datetime.now().month

    images_mapping = SeriesToImageMapping()

    # Get series for the current year
    for data in get_series_for_year(s, current_year, series_old_data):
        anime_url = get_anime_urls_from_events_v2(data)

        download_image_from_urls(anime_url)

        add_event_from_data_series_v2(data, images_mapping.get_mapping())

    month_limiter = -7 + current_month
    next_year = current_year + 1
    print("Getting series for the next year")
    for data in get_series_for_year(
        s, next_year, series_old_data, month_limiter
    ):  # till the month limiter

        anime_url = get_anime_urls_from_events_v2(data)

        download_image_from_urls(anime_url)

        add_event_from_data_series_v2(data, images_mapping.get_mapping())

    save_picked_series_data(series_old_data)

    if NO_LONGER_EXISTING_EVENTS:
        logging.info(
            "No longer existing events size: %d", len(NO_LONGER_EXISTING_EVENTS)
        )
        print(NO_LONGER_EXISTING_EVENTS)
        delete_no_longer_existing_events_v2(
            NO_LONGER_EXISTING_EVENTS, images_mapping.get_mapping()
        )
    else:
        logging.info("No events to delete.")

    images_mapping.save_mapping()

    logging.info("Finished the script in %.2f secs", time.time() - start_time)


if __name__ == "__main__":

    main()
