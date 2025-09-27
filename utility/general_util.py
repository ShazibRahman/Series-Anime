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
