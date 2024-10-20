
import datetime

import pytz
from gdrive import my_google_calendar

TI = 'Asia/Kolkata'

def _add_event_to_google_calendar(series_name: str, start_time: datetime.datetime, end_time: datetime.datetime, series_description: str):
    google_calendar = my_google_calendar.GoogleCalendar()
    google_calendar.create_event(summary=series_name, description=series_description, start_time=start_time, end_time=end_time, time_zone=TI)
    return None


# not being used for now don't use its
def add_event_for_a_week(series_list: list):
    date_today = datetime.datetime.now().date()

    for series in series_list:

        summary = series[0]
        description = "Series"
        time_str = series[2]
        day_to_add = series[3] # 0 for today, 1 for tomorrow, 2 for day after tomorrow and so on
        day_after_n_days = date_today + datetime.timedelta(days=day_to_add)



        # parse 7:30pm today to datetime object using pytz and datetime

        datetime_series =  datetime.datetime.strptime(time_str, '%I:%M%p')
        combined_datetime = datetime.datetime.combine(day_after_n_days, datetime_series.time())
        start_time = pytz.timezone(TI).localize(combined_datetime + datetime.timedelta(hours=1))
        end_time = start_time + datetime.timedelta(hours=1)

        _add_event_to_google_calendar(summary, start_time, end_time, description)


def add_event_for_current_month(series_list: list):
    date_today = datetime.datetime.now().date()

    for series in series_list:

        summary = series[0]
        description = "Series"
        time_str = series[2]
        day = series[3] # this is the exact day of the month
        day_of_the_series = date_today.replace(day=day)

        # parse 7:30pm today to datetime object using pytz and datetime
        date_time_series =  datetime.datetime.strptime(time_str, '%I:%M%p')
        combined_datetime = datetime.datetime.combine(day_of_the_series, date_time_series.time())
        start_time = pytz.timezone(TI).localize(combined_datetime + datetime.timedelta(hours=1))
        end_time = start_time + datetime.timedelta(hours=1)

        _add_event_to_google_calendar(summary, start_time, end_time, description)