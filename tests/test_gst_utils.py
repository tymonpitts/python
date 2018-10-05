import datetime

import gst_utils


def test_get_period():
    start, end = gst_utils.get_period(datetime.date(2018, 10, 3))
    assert start == datetime.date(2018, 10, 1)
    assert end == datetime.date(2019, 4, 1)

    start, end = gst_utils.get_period(datetime.date(2019, 1, 3))
    assert start == datetime.date(2018, 10, 1)
    assert end == datetime.date(2019, 4, 1)

    start, end = gst_utils.get_period(datetime.date(2018, 9, 3))
    assert start == datetime.date(2018, 4, 1)
    assert end == datetime.date(2018, 10, 1)


def test_get_previous_period():
    start, end = gst_utils.get_previous_period(datetime.date(2018, 10, 3))
    assert start == datetime.date(2018, 4, 1)
    assert end == datetime.date(2018, 10, 1)

    start, end = gst_utils.get_previous_period(datetime.date(2019, 1, 3))
    assert start == datetime.date(2018, 4, 1)
    assert end == datetime.date(2018, 10, 1)

    start, end = gst_utils.get_previous_period(datetime.date(2018, 9, 3))
    assert start == datetime.date(2017, 10, 1)
    assert end == datetime.date(2018, 4, 1)
