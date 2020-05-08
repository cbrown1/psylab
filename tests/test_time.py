# -*- coding: utf-8 -*-

import psylab

def test_get_week_number():
    date = "2020-01-07"
    weekn = psylab.time.get_week_number(date)
    assert weekn == '02'

def test_seconds_to_time():
    sec = 223.004
    strtime = psylab.time.seconds_to_time(sec)
    assert strtime == "00:03:43.004"

def test_time_to_seconds():
    strtime = "22:00:27"
    sec = psylab.time.time_to_seconds(strtime)
    assert sec == 79227.0

