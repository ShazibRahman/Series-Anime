def return_no_longer_existing_event(old_events: list, new_events: list) -> list:
    """
    Compares two lists of events and returns a list of events that are present in the old list but not in the new list.

    Parameters
    ----------
    old_events : list
        The list of old events
    new_events : list
        The list of new events

    Returns
    -------
    list
        A list of events that are present in the old list but not in the new list
    """
    deleted_events = [event for event in old_events if event not in new_events]
    return deleted_events
