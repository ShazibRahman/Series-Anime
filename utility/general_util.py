import datetime

from common_dto.events import CalendarDtoPickled


def get_anime_url_from_events(events: list) -> list:
    """
    Extracts and returns a list of anime URLs from the given list of events.

    Parameters
    ----------
    events : list
        A list of event dictionaries, each containing an 'anime_url' key.

    Returns
    -------
    list
        A list of anime URLs extracted from the events.
    """
    return [
        event[1] for event in events if len(event) > 1 and isinstance(event[1], str)
    ]


def get_anime_urls_from_events_v2(events: list[CalendarDtoPickled]) -> list:
    """
    Extracts and returns a list of anime URLs from the given list of CalendarDtoPickled events.

    Parameters
    ----------
    events : list[CalendarDtoPickled]
        A list of CalendarDtoPickled objects, each containing an 'anime_url' attribute.

    Returns
    -------
    list
        A list of anime URLs extracted from the events.
    """
    return [event.url for event in events if event.url is not None and event.url != ""]


def clean_not_existing_series_data_from_image_mapping(
    image_dict: dict, series_dict: dict
) -> list[str]:
    """
    Cleans the image dictionary by removing entries that do not exist in the series dictionary.

    Parameters
    ----------
    image_dict : dict
        The dictionary containing image mappings.
    series_dict : dict
        The dictionary containing series data.

    Returns
    -------
    None
    """

    print("Cleaning series data from image mappings...")
    keys = set()
    for values in series_dict.values():
        for event in values:
            keys.add(event[1])

    keys_in_image_dict = list(image_dict.keys())
    keys_to_be_deleted = []

    for key in keys_in_image_dict:
        if key not in keys:
            # del image_dict[key]
            keys_to_be_deleted.append(key)

    print(keys_to_be_deleted)

    return keys_to_be_deleted


def clean_not_existing_series_data_from_image_mapping_v2(
    image_dict: dict[str, str], series_dict: dict[str, list[CalendarDtoPickled]]
) -> list[str]:
    """
    Cleans the image dictionary by removing entries that do not exist in the series dictionary.

    Parameters
    ----------
    image_dict : dict
        The dictionary containing image mappings.
    series_dict : dict
        The dictionary containing series data.

    Returns
    -------
    None
    """

    print("Cleaning series data from image mappings...")
    keys = set()
    for values in series_dict.values():
        for event in values:
            keys.add(event.url)

    keys_in_image_dict = list(image_dict.keys())
    keys_to_be_deleted = []

    for key in keys_in_image_dict:
        if key not in keys:
            # del image_dict[key]
            keys_to_be_deleted.append(key)

    print(keys_to_be_deleted)

    return keys_to_be_deleted


def merge_time_str_datetime_date(
    time_str: str, day: datetime.date
) -> datetime.datetime:
    """
    Merges a time string and a date object into a single formatted datetime string.

    Parameters
    ----------
    time_str : str
        The time string in the format "H:MMam/pm" (e.g., "7:30pm").
    day : datetime.date
        The date object representing the date.

    Returns
    -------
    str
        A formatted datetime string in the format "YYYY-MM-DD HH:MMam/pm".
    """
    date_time_series = datetime.datetime.strptime(time_str, "%I:%M%p")
    combined_datetime = datetime.datetime.combine(day, date_time_series.time())
    return combined_datetime


def event_key(event: CalendarDtoPickled):
    return event.summary, event.start_time, event.start_date


def fill_new_series_list_calendar_ids(
    series_old_data: dict[str, list[CalendarDtoPickled]],
    key: str,
    new_series_data: list[CalendarDtoPickled],
) -> list[CalendarDtoPickled]:
    """
    update the new

    Parameters
    ----------
    series_old_data : dict
        The dictionary containing old series data.
    key : str
        The key for which the series data needs to be updated.
    new_series_data : list
        The new series data to be added.

    Returns
    -------
    None
    """

    old_list = series_old_data[key]

    old_lookup = {event_key(e): e for e in old_list}

    for new_event in new_series_data:
        k = event_key(new_event)
        if k in old_lookup:
            old_event = old_lookup[k]
            new_event.calendar_id = old_event.calendar_id

    return new_series_data
