# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import psylab

filename = "/some/path/to/a/filename.ext"

def test_get_fileext():
    ref = ".ext"
    ret = psylab.path.get_fileext(filename)
    assert ret == ref
    return

def test_get_filebase():
    ref = "filename"
    ret = psylab.path.get_filebase(filename)
    assert ret == ref
    return

def test_get_filename():
    ref = "filename.ext"
    ret = psylab.path.get_filename(filename)
    assert ret == ref
    return

def test_get_path():
    ref = "/some/path/to/a"
    ret = psylab.path.get_path(filename)
    assert ret == ref
    return
