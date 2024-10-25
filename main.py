import logging
import os

import log.logconfig  # noqa
from utility import time_utility
from utility.Notification import DesktopNotification
from utility.add_event_to_google_calendar import add_event_from_data_series
from utility.clean_up import clean_up
from utility.file_data_utility import check_if_events_already_added_for_the_month
from utility.get_image_from_url import get_image_from_url
from utility.get_series_data import get_series_data_for_current_day, \
    get_series_for_year
from utility.login import login

LOGIN_URL = "https://next-episode.net/userlogin"
USERNAME = os.getenv("next_user")
PASSWORD = os.getenv("next_password")

if __name__ == "__main__":
    logging.info("Starting the script")

    s = login(USERNAME, PASSWORD, LOGIN_URL)
    page_content = s.get("https://next-episode.net/calendar").text
    series_data = get_series_data_for_current_day(page_content)

    if len(series_data) == 0:
        print("No series today")
        DesktopNotification("No Series Today", "No Series Today", "")

    for series in series_data:
        image_url = get_image_from_url(s, series[1])
        DesktopNotification(series[0], series[2], str(image_url))

    # Check if events are already added for the month, allowed dates are 1st and 15th of the month
    # if 1st or 15th of the month is not passed, then events are not added for the month
    # if events are missed for 1st or 15th of the month, then they are added very next available day after 1st or 15th

    # perform this only if today is the first day
    if not check_if_events_already_added_for_the_month(time_utility.get_current_date()) or True:
        # series_data_to_add_to_calendar = \
        #     get_series_data_for_the_current_month_btw_start_date_end_date(page_content,
        #     *time_utility.get_current_month_range())
        # add_event_for_current_month(series_data_to_add_to_calendar)
        # cleaning the image directory only once the events are added for the month
        # reduce the number of times the image directory is cleaned and new images are downloaded
        clean_up()

        print("Getting series for the year")
        # print( get_series_for_year(s, time_utility.get_current_year()))
        for data in get_series_for_year(s, time_utility.get_current_year()):
            add_event_from_data_series(data)
    #     add_event_from_data_series_async(get_series_for_year(s, time_utility.get_current_year()))
