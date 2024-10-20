import datetime
import io

import json
import pathlib

DATA_FOLDER = pathlib.Path(__file__).parent.parent.joinpath('data')
EVENTS_FILE = DATA_FOLDER.joinpath('events.json')
def __read_json_file(file_path):
    try:
        with io.open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError or json.decoder.JSONDecodeError:
        return []


def __write_json_file(file_path, data):
    with io.open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)




def check_if_events_already_added_for_the_month( month: datetime.date) -> bool:
    """
    This function checks if the events have already been added for the month
    :param month: int
    :return: bool
    """
    events:list = __read_json_file(EVENTS_FILE)
    if str(month) in events:
        return True
    else:
        events.append(str(month))
        __write_json_file(EVENTS_FILE, events)
        return False

if __name__ == "__main__":
    print(    check_if_events_already_added_for_the_month(datetime.datetime.now().date()))
