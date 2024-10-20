import logging

from utility import time_utility
from utility.add_event_to_google_calendar import add_event_for_a_week, add_event_for_current_month
from utility.clean_up import clean_up
from utility.file_data_utility import check_if_events_already_added_for_the_month
from utility.login import login
from utility.get_series_data import get_series_data_for_current_day, \
    get_series_data_for_today_and_next_no_of_days_within_a_week, \
    get_series_data_for_the_current_month_btw_start_date_end_date
from utility.get_image_from_url import get_image_from_url
from utility.Notification import DesktopNotification
import log.logconfig # noqa

import os


LOGIN_URL = "https://next-episode.net/userlogin"
USERNAME =  os.getenv("next_user")
PASSWORD = os.getenv("next_password")


if __name__ == "__main__":
    logging.info("Starting the script")

    clean_up()


    s = login(USERNAME,PASSWORD,LOGIN_URL)
    page_content = s.get("https://next-episode.net/calendar").text
    series_data = get_series_data_for_current_day(page_content)
    if len(series_data) == 0:
        print("No series today")
        DesktopNotification("No Series Today","No Series Today","")

    for series in series_data:
        image_url = get_image_from_url(s,series[1])
        print(image_url)

        DesktopNotification(series[0],series[2],str(image_url))


    # perform this only if today is the first day
    if not check_if_events_already_added_for_the_month(time_utility.get_current_date()):
        series_data_to_add_to_calendar = get_series_data_for_the_current_month_btw_start_date_end_date(page_content, *time_utility.get_current_month_range())
        add_event_for_current_month(series_data_to_add_to_calendar)







