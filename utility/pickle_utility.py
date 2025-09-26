import pickle
import pathlib

from .time_utility import get_current_year, get_current_month

DATA_DIRECTORY = pathlib.Path(__file__).parent.parent.joinpath("data")
DATA_FILE = DATA_DIRECTORY.joinpath("data.pickle")

series_list_data = DATA_DIRECTORY.joinpath("series_list_data.pickle")

if not DATA_FILE.exists():
    DATA_FILE.touch()


def clean_old_data(data: dict):
    """
    Clean old data from the given dictionary by deleting
    the keys for previous years and previous months of the current year.
    """
    current_year: int = get_current_year()
    current_month: int = get_current_month()
    keys = list(data.keys())

    for key in keys:
        month, year = [int(i) for i in key.split("_")]

        if year < current_year:
            del data[key]
        elif year == current_year:
            if month < current_month:
                del data[key]

    return


def get_pickled_stored_record() -> dict:
    """
    Retrieves the stored record from the pickle file.

    Returns
    -------
    dict
        The stored record
    """

    with open(DATA_FILE, "rb") as file:
        try:
            data = pickle.load(file)
        except Exception as e:
            print(e)
            data = {}
    return data


def save_pickled_record(data: dict):
    """
    Saves the given data to a pickle file.

    Parameters
    ----------
    data : dict
        The data to be saved

    Returns
    -------
    None
    """
    with open(DATA_FILE, "wb") as file:
        clean_old_data(data)
        pickle.dump(data, file)


def get_picked_series_data():
    """
    Retrieves the series data from the pickle file.

    Returns
    -------
    dict
        The series data
    """
    with open(series_list_data, "rb") as file:
        try:
            data = pickle.load(file)
        except Exception as e:
            print(e)
            data = {}
    return data


def save_picked_series_data(data: dict):
    """
    Saves the given series data to a pickle file.

    Parameters
    ----------
    data : dict
        The series data to be saved

    Returns
    -------
    None
    """
    with open(series_list_data, "wb") as file:
        clean_old_data(data)
        pickle.dump(data, file)
