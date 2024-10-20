import logging

from utility import time_utility
from utility.add_event_to_google_calendar import add_event
from utility.clean_up import clean_up
from utility.login import login
from utility.get_series_data import get_series_data_for_current_day, \
    get_series_data_for_today_and_next_no_of_days
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
    print(series_data)
    if len(series_data) == 0:
        print("No series today")
        DesktopNotification("No Series Today","No Series Today","")



    for series in series_data:
        image_url = get_image_from_url(s,series[1])
        print(image_url)

        DesktopNotification(series[0],series[2],str(image_url))

    no_of_days_btw_current_day_and_saturday = time_utility.get_no_of_days_between_current_day_and_day("Saturday")

    if no_of_days_btw_current_day_and_saturday>0:
        series_data = get_series_data_for_today_and_next_no_of_days(page_content, no_of_days_btw_current_day_and_saturday)
        print(series_data)
        add_event(series_data)




