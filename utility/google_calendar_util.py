"""
This module contains utility functions for adding events to Google Calendar.
"""

import datetime
from logging import getLogger

import pytz
from common_dto.events import CalendarDtoPickled
from gdrive_tool import my_google_calendar

logger = getLogger(__name__)

I_M_P = "%I:%M%p"

TI = "Asia/Kolkata"


def _add_event_to_google_calendar(
    series_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    series_description: str,
    image_url: str = "",
    event_id: str = "",
):
    """
    This function adds an event to Google Calendar.
    The event is created with the given series_name, start_time, end_time and series_description.

    Args:
        series_name (str): The name of the series.
        start_time (datetime.datetime): The start time of the event.
        end_time (datetime.datetime): The end time of the event.
        series_description (str): The description of the series.
    """
    google_calendar = my_google_calendar.GoogleCalendar()
    calendar_id: str = google_calendar.create_event_v2(
        summary=series_name,
        description=series_description,
        image_url=image_url,
        start_time=start_time,
        end_time=end_time,
        time_zone=TI,
        event_id=event_id,
    )
    if calendar_id is None:
        logger.warning("No Google Calendar ID found for series " + series_name)
    return calendar_id


# not being used for now don't use its
def add_event_for_a_week(series_list: list):
    """
    This function adds an event to Google Calendar for each series in the series_list.
    The event is created with the given series_name, start_time, end_time and series_description.
    The start_time and end_time are calculated based on the current date
    and the day_to_add in the series_list.
    The event is added to the calendar for the day_after_n_days.

    Args:
        series_list (list): A list of tuples.
        Each tuple contains the name of the series,
        the link to the series and the time of the show.
    """
    date_today = datetime.datetime.now().date()

    for series in series_list:
        summary = series[0]
        description = "Series"
        time_str = series[2]
        day_to_add = series[
            3
        ]  # 0 for today, 1 for tomorrow, 2 for day after tomorrow and so on
        day_after_n_days = date_today + datetime.timedelta(days=day_to_add)

        # parse 7:30pm today to datetime object using pytz and datetime

        datetime_series = datetime.datetime.strptime(time_str, I_M_P)
        combined_datetime = datetime.datetime.combine(
            day_after_n_days, datetime_series.time()
        )
        start_time = pytz.timezone(TI).localize(
            combined_datetime + datetime.timedelta(hours=1)
        )
        end_time = start_time + datetime.timedelta(hours=1)

        _add_event_to_google_calendar(summary, start_time, end_time, description)


def add_event_for_current_month(series_list: list):
    """
    This function adds an event to Google Calendar for each series in the series_list.
    The event is created with the given series_name, start_time, end_time and series_description.
    The start_time and end_time are calculated based on the current date
    and the day in the series_list.
    The event is added to the calendar for the day in the series_list.

    Args:
        series_list (list): A list of tuples.
        Each tuple contains the name of the series,
        the link to the series and the time of the show.
    """

    date_today = datetime.datetime.now().date()

    for series in series_list:
        summary = series[0]
        description = "Series"
        time_str = series[2]
        day = series[3]  # this is the exact day of the month
        day_of_the_series = date_today.replace(day=day)

        # parse 7:30pm today to datetime object using pytz and datetime
        date_time_series = datetime.datetime.strptime(time_str, I_M_P)
        combined_datetime = datetime.datetime.combine(
            day_of_the_series, date_time_series.time()
        )
        start_time = pytz.timezone(TI).localize(
            combined_datetime + datetime.timedelta(hours=1)
        )
        end_time = start_time + datetime.timedelta(hours=1)

        _add_event_to_google_calendar(summary, start_time, end_time, description)


# def add_event_from_data_series(series_list: list, image_mapping: dict):
#     """
#     This function adds an event to Google Calendar for each series in the series_list.
#     The event is created with the given series_name, start_time, end_time and series_description.
#     The start_time and end_time are calculated based on the day in the series_list
#     and the time of the show in the series_list.
#     The event is added to the calendar for the day in the series_list.
#
#     Args:
#         image_mapping:
#         series_list (list): A list of tuples.
#         Each tuple contains the name of the series,
#         the link to the series and the time of the show
#         and the day of the month.
#     """
#     for series in series_list:
#         summary = series[0]
#         description = "Series"
#         time_str = series[2]
#         day: datetime.date = series[3]  # this is the datetime.date
#
#         # parse 7:30pm today to datetime object using pytz and datetime
#         date_time_series = datetime.datetime.strptime(time_str, I_M_P)
#         combined_datetime = datetime.datetime.combine(day, date_time_series.time())
#         start_time = pytz.timezone(TI).localize(
#             combined_datetime + datetime.timedelta(hours=1)
#         )
#         end_time = start_time + datetime.timedelta(hours=1)
#         # print(summary,start_time,end_time,description)
#         image_url = ""
#         if series[1] in image_mapping:
#             image_url = image_mapping[series[1]]
#
#         _add_event_to_google_calendar(
#             summary, start_time, end_time, description, image_url
#         )


def add_event_from_data_series_v2(
    series_list: list[CalendarDtoPickled], image_mapping: dict
):
    """
    This function adds an event to Google Calendar for each series in the series_list.
    The event is created with the given series_name, start_time, end_time and series_description.
    The start_time and end_time are calculated based on the day in the series_list
    and the time of the show in the series_list.
    The event is added to the calendar for the day in the series_list.

    Args:
        image_mapping:
        series_list (list): A list of tuples.
        Each tuple contains the name of the series,
        the link to the series and the time of the show
        and the day of the month.
    """
    for series in series_list:
        summary = series.summary
        description = "Series"
        time_str = series.start_time
        day: datetime.date = series.start_date

        # parse 7:30pm today to datetime object using pytz and datetime
        date_time_series = datetime.datetime.strptime(time_str, I_M_P)
        combined_datetime = datetime.datetime.combine(day, date_time_series.time())
        start_time = pytz.timezone(TI).localize(
            combined_datetime + datetime.timedelta(hours=1)
        )
        end_time = start_time + datetime.timedelta(hours=1)
        # print(summary,start_time,end_time,description)
        image_url = ""
        if series.url in image_mapping:
            image_url = image_mapping[series.url]

        calendar_id: str | None = _add_event_to_google_calendar(
            summary, start_time, end_time, description, image_url, series.calendar_id
        )
        series.calendar_id = calendar_id


def delete_no_longer_existing_events(series_list_to_delete: list, image_mapping: dict):
    """
    This function deletes events from Google Calendar that are no longer existing.
    The events to be deleted are stored in the NO_LONGER_EXISTING_EVENTS list.
    """
    google_calendar = my_google_calendar.GoogleCalendar()
    for event in series_list_to_delete:
        summary = event[0]

        time_str = event[2]
        day: datetime.date = event[3]  # this is the datetime.date
        image_url = ""

        if event[1] in image_mapping:
            image_url = image_mapping[event[1]]

        # parse 7:30pm today to datetime object using pytz and datetime
        date_time_series = datetime.datetime.strptime(time_str, I_M_P)
        combined_datetime = datetime.datetime.combine(day, date_time_series.time())
        start_time = pytz.timezone(TI).localize(
            combined_datetime + datetime.timedelta(hours=1)
        )

        google_calendar.delete_event(
            start_date_to_update=start_time,
            summary=summary,
            image_url=image_url,
        )


def delete_no_longer_existing_events_v2(
    series_list_to_delete: list[CalendarDtoPickled], image_mapping: dict
):
    """
    This function deletes events from Google Calendar that are no longer existing.
    The events to be deleted are stored in the NO_LONGER_EXISTING_EVENTS list.
    """
    google_calendar = my_google_calendar.GoogleCalendar()
    for event in series_list_to_delete:
        google_calendar.delete_event(
            event_id=event.calendar_id,
            image_url=image_mapping[event.url],
            summary=event.summary,
        )


def get_calendar_ids(events) -> None:
    """
    This function returns a list of calendar IDs.
    """
    google_calendar = my_google_calendar.GoogleCalendar()

    for event in events:
        summary = event[0]

        time_str = event[2]
        day: datetime.date = event[3]  # this is the datetime.date

        # parse 7:30pm today to datetime object using pytz and datetime
        date_time_series = datetime.datetime.strptime(time_str, I_M_P)
        combined_datetime = datetime.datetime.combine(day, date_time_series.time())
        start_time = pytz.timezone(TI).localize(
            combined_datetime + datetime.timedelta(hours=1)
        )
        calendar_ids = google_calendar.get_calendar_id(
            start_date_to_update=start_time, summary=summary
        )
        print(calendar_ids)
