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
