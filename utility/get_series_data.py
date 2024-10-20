from bs4 import BeautifulSoup
from bs4.element import Tag



def get_series_data_for_current_day(page_content: str) -> list:
    soup = BeautifulSoup(page_content, 'html.parser')
    today_anchor: Tag = soup.find('a', {'name': 'today'})
    if today_anchor:
        parent = today_anchor.parent

        shows = parent.find_all('div', class_='cal_name')
        times = parent.find_all('div', class_='cal_more')
        return [(show.find('a').text, _modify_link(show.find('a')['href']), time.find('div', class_='h').text) for show, time in zip(shows, times)]
    else:
        return []


# not being used don't use it for now
def get_series_data_for_today_and_next_no_of_days_within_a_week(page_content: str, no_of_days: int) -> list:
    soup = BeautifulSoup(page_content, 'html.parser')
    today_anchor: Tag = soup.find('a', {'name': 'today'})
    series_data = []
    day_data:Tag
    if today_anchor:
        parent = today_anchor.parent
        day_data = parent
        print(day_data)


        shows = day_data.find_all('div', class_='cal_name')
        times = day_data.find_all('div', class_='cal_more')
        days_to_add_in_time = [0] * len(shows)
        series_data.extend([(show.find('a').text, _modify_link(show.find('a')['href']), time.find('div', class_='h').text,day) for show, time,day in zip(shows, times, days_to_add_in_time)])
        print(series_data)
    for i in range(1, no_of_days+1):
        day_data = day_data.next_sibling.next_sibling # noqa
        shows = day_data.find_all('div', class_='cal_name')
        times = day_data.find_all('div', class_='cal_more')
        days_to_add_in_time = [i] * len(shows)
        series_data.extend([(show.find('a').text, _modify_link(show.find('a')['href']), time.find('div', class_='h').text,day) for
                      show, time,day in zip(shows, times,days_to_add_in_time)])



    return series_data


def get_series_data_for_the_current_month_btw_start_date_end_date(page_content: str,start_date,end_date) -> list:
    print(start_date,end_date)
    soup = BeautifulSoup(page_content, 'html.parser')
    spans = soup.find_all('span')
    series_data = []

    for span in spans:
        if span.string and span.string.strip().isdigit():  # Check if the span contains a number (the day)
            day = span.string.strip()
            if start_date <= int(day) <= end_date:
                day_data_td = span.parent.parent
                shows = day_data_td.find_all('div', class_='cal_name')
                times = day_data_td.find_all('div', class_='cal_more')
                day_list = [int(day)] * len(shows)
                series_data.extend([(show.find('a').text, _modify_link(show.find('a')['href']), time.find('div', class_='h').text,day) for show, time,day in zip(shows, times,day_list)])


    return series_data





def _modify_link(link: str) -> str:
    return f"https:{link}"