"""
A module for Adding Anime from next episode to google calendar.
"""

import logging
import os
import time

import log.logconfig  # noqa # pylint: disable=unused-import
from utility import time_utility
from utility.add_event_to_google_calendar import add_event_from_data_series
from utility.clean_up import clean_up
from utility.file_data_utility import check_if_events_already_added_for_the_month
from utility.get_series_data import get_series_for_year
from utility.login import login_user

LOGIN_URL = "https://next-episode.net/userlogin"
USERNAME = os.getenv("next_user")
PASSWORD = os.getenv("next_password")

if __name__ == "__main__":
    start_time = time.time()
    logging.info("Starting the script")

    # page_content = s.get("https://next-episode.net/calendar").text
    # series_data = get_series_data_for_current_day(page_content)

    # if len(series_data) == 0:
    #     print("No series today")
    #     DesktopNotification("No Series Today", "No Series Today", "")
    #
    # for series in series_data:
    #     image_url = get_image_from_url(s, series[1])
    #     DesktopNotification(series[0], series[2], str(image_url))

    # Check if events are already added for the month, allowed dates are 1st and 15th of the month
    # if 1st or 15th of the month is not passed, then events are not added for the month
    # if events are missed for 1st or 15th of the month, then they are added very next available day after 1st or 15th

    if not check_if_events_already_added_for_the_month(time_utility.get_current_date()) or True:
        start_time = time.time()
        s = login_user(USERNAME, PASSWORD, LOGIN_URL)
        clean_up()

        print("Getting series for the year")
        # print( get_series_for_year(s, time_utility.get_current_year()))
        for data in get_series_for_year(s, 2025):
            add_event_from_data_series(data)


    logging.info("Finished the script in %s secs", time.time() - start_time)
