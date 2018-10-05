import datetime

from typing import Tuple


def get_period(date=None):
    # type: (datetime.date) -> Tuple[datetime.date, datetime.date]
    """ get the current GST period start and end dates based on the provided
    date which defaults to today

    end dates are exclusive
    """
    date = date or datetime.date.today()
    if date.month <= 3:
        start = datetime.date(date.year - 1, 10, 1)
        end = datetime.date(date.year, 4, 1)
    elif date.month >= 10:
        start = datetime.date(date.year, 10, 1)
        end = datetime.date(date.year + 1, 4, 1)
    else:
        start = datetime.date(date.year, 4, 1)
        end = datetime.date(date.year, 10, 1)

    return start, end


def get_previous_period(date=None):
    # type: (datetime.date) -> Tuple[datetime.date, datetime.date]
    """ get the previous GST period start and end dates based on the provided
    date which defaults to today

    end dates are exclusive
    """
    date = date or datetime.date.today()
    if date.month <= 3:
        start = datetime.date(date.year - 1, 4, 1)
        end = datetime.date(date.year - 1, 10, 1)
    elif date.month >= 10:
        start = datetime.date(date.year, 4, 1)
        end = datetime.date(date.year, 10, 1)
    else:
        start = datetime.date(date.year - 1, 10, 1)
        end = datetime.date(date.year, 4, 1)

    return start, end
