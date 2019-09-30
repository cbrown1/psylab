# -*- coding: utf-8 -*-

import psylab

conf_file = "tests/data/test_settings.conf"

def test_get_str():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = "This is a multi-word string"
    ret = machine.get_str('param_str')
    assert ret == ref
    return

def test_get_bool():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = True
    ret = machine.get_bool('param_bool')
    assert ret == ref
    return

def test_get_float():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = 3.141592653
    ret = machine.get_float('param_float')
    assert ret == ref
    return

def test_get_int():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = 44100
    ret = machine.get_int('param_int')
    assert ret == ref
    return

def test_get_list_float():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = [0.,1.4,6.666667]
    ret = machine.get_list_float('param_list_floats')
    assert ret == ref
    return

def test_get_list_int():
    machine=psylab.config.local_settings(conf_file=conf_file)
    machine.machine = 'test.machine'
    ref = [0,500,2]
    ret = machine.get_list_int('param_list_ints')
    assert ret == ref
    return

