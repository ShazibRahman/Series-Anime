from datetime import datetime
import calendar

day_name_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


# suppose I pass sunday as the day_name to the function match_current_day(day_name: str) -> bool
def match_current_day(day_name: str) -> bool:
    """
    This function takes a day_name and returns True if the day_name matches the current day, else False
    :param day_name: str
    :return: bool
    """

    return calendar.day_name[datetime.now().weekday()] == day_name


def get_current_day() -> str:
    """
    This function returns the current day
    :return: str
    """

    return calendar.day_name[datetime.now().weekday()]

def get_no_of_days_between_current_day_and_day(day_name: str) -> int:
    """
    This function returns the number of days between the current day and the day_name
    :param day_name: str
    :return: int
    """
    current_day = get_current_day()
    current_day_index = day_name_list.index(current_day)
    day_name_index = day_name_list.index(day_name)
    return day_name_index - current_day_index



if __name__=="__main__":
  # print(  match_current_day("Sunday")) # returns True if today is Sunday, else False
  #
  # print(get_current_day()) # returns the current day

  print(get_no_of_days_between_current_day_and_day("Saturday")) # returns the number of days between the current day and Sunday
