def return_no_longer_existing_event(old_events: list, new_events: list) -> list:
    """
    Compares two lists of events and returns a list of events from the old list
    whose titles are not present in the new events list.

    Parameters
    ----------
    old_events : list
        The list of old events
    new_events : list
        The list of new events

    Returns
    -------
    list
        A list of events from the old list that are no longer in the new list based on title
    """
    # Extract all titles from new_events
    new_titles = {_get_title_from_event(event) for event in new_events}

    # Return old events whose titles are not in new_titles
    deleted_events = [
        event for event in old_events if _get_title_from_event(event) not in new_titles
    ]

    return deleted_events


def _get_title_from_event(event: tuple) -> str:
    """
    Extracts the title from an event tuple.

    Parameters
    ----------
    event : tuple
        The event tuple

    Returns
    -------
    str
        The title of the event
    """
    if len(event) > 0 and isinstance(event[0], str):
        summary = event[0]
        actual_title = " - ".join(summary.split(" - ")[:-1])
        return actual_title
    return ""


def return_new_list_of_series_which_actually_is_update(
    series_list: list, old_series_list: list
) -> list:
    """
    Compares two lists of series and returns a list of series from the new list
    whose titles are not present in the old series list.

    Parameters
    ----------
    series_list : list
        The list of new series
    old_series_list : list
        The list of old series

    Returns
    -------
    list
        A list of series from the new list that are not in the old list based on title
    """

    # Return new series whose either are not in old list or titles or time or date do not match
    new_series = [event for event in series_list if event not in old_series_list]

    return new_series
