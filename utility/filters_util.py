import logging
import re

series_filter = {"plain_filter": set(), "regex_filter": set()}

series_filter["plain_filter"].add("The Last of Us - 2xSpecial".lower())
series_filter["plain_filter"].add("Andor - 2xSpecial - Season 2".lower())

series_filter["regex_filter"].add(r"-\s(\d+xspecial)\s-")


def filter_series(series_name: str) -> bool:
    # Check plain filters
    for series in series_filter["plain_filter"]:
        if series in series_name.lower():
            logging.info(f"Filtered out {series_name}")
            return True

    # Check regex filters
    for pattern in series_filter["regex_filter"]:
        match = re.search(pattern, series_name.lower())

        if match:
            logging.info(f"Filtered out {series_name}")
            return True

    return False


if __name__ == "__main__":
    result = filter_series(
        "Chainsaw Man - 1xSpecial - Chainsaw Man – The Movie: Reze Arc"
    )
    print(result)  # Should be True now
