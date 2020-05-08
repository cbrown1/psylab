# -*- coding: utf-8 -*-

import psylab


def test_str_to_list():
    ref = [1,2,3,4,8,10,11,12,50]
    ret = psylab.string.str_to_list('1-4,8,10-12,50')
    assert all([a == b for a, b in zip(ref, ret)])


def test_list_to_str():
    ref = '0:3,7,9:11,49'
    ret = psylab.string.list_to_str([0, 1, 2, 3, 7, 9, 10, 11, 49])
    assert ref == ret


def test_reverse_template():
    variables = ["%album", "%track", "%title", "%artist", "%time"]
    haystack = "01. (00:00:00) Crown of the Valley - Jets to Brazil - Orange Rhyming Dictionary"
    template = "%track. (%time) %title - %artist - %album"
    rt = psylab.string.reverse_template()
    track_info = rt.process(haystack, template, variables)
    assert track_info[0][0] == "%track"
    assert track_info[0][1] == "01"
    assert track_info[1][0] == "%time"
    assert track_info[1][1] == "00:00:00"
    assert track_info[2][0] == "%title"
    assert track_info[2][1] == "Crown of the Valley"
    assert track_info[3][0] == "%artist"
    assert track_info[3][1] == "Jets to Brazil"
    assert track_info[4][0] == "%album"
    assert track_info[4][1] == "Orange Rhyming Dictionary"

