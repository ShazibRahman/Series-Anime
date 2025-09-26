import pathlib

import ujson as json

DATA_DIRECTORY = pathlib.Path(__file__).parent.parent.joinpath("data")
series_list_data = DATA_DIRECTORY.joinpath("data.pickle")

if not series_list_data.exists():
    series_list_data.touch()


def read_json_file():
    """
    Reads the given file and returns its content as a JSON object.

    If the file does not exist or its content is not valid JSON,
    the function will return an empty list.
    """
    try:
        with open(series_list_data, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(repr(e))
        return {}


def write_json_file(data, indent=4):
    with open(series_list_data, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)
