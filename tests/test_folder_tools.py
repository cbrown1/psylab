# -*- coding: utf-8 -*-

import os
import numpy as np
import numpy.testing as np_testing
import psylab

concurrent_file_folders = [
                          'tests/data/concurrent_files/0_name', 
                          'tests/data/concurrent_files/1_verb',
                          'tests/data/concurrent_files/2_number',
                          'tests/data/concurrent_files/3_color',
                          'tests/data/concurrent_files/4_object'
                          ]

def test_concurrent_files_get_filenames():
    ref = ['0_jean', '0_took', '0_no', '0_white', '0_toys']

    f = psylab.tools.folder_tools.concurrent_files(concurrent_file_folders,
                          )
    ret = f.get_filenames(fmt='file')
    assert ref == ret


def test_concurrent_files_use():
    ref = ['0_jean', '0_took', '0_no', '0_white', '0_toys']
    f = psylab.tools.folder_tools.concurrent_files(concurrent_file_folders,
                                                   use={'0_name':'0_jean'}, # Only use name Jean
                                                   repeat=True,
                                                  )
    ret1 = f.get_filenames(fmt='file')
    ret2 = f.get_filenames(fmt='file')
    ret3 = f.get_filenames(fmt='file')
    assert ref[0] == ret1[0] == ret2[0] == ret3[0]
    assert not ref[1] == ret1[1] == ret2[1] == ret3[1]


def test_concurrent_files_fullfile():
    f = psylab.tools.folder_tools.concurrent_files(concurrent_file_folders)
    ret1 = f.get_filenames(fmt='file')
    ref = os.path.join(f.path_list[0], ret1[0])
    f = psylab.tools.folder_tools.concurrent_files(concurrent_file_folders)
    ret2 = f.get_filenames()
    assert ref == ret2[0]


def test_concurrent_files_text():
    ref = 'took'
    f = psylab.tools.folder_tools.concurrent_files(concurrent_file_folders,
                                                   text_file='tests/data/concurrent_files/concurrent_files.txt',
                                                   text_format='files,word',
                                                  )
    ret1 = f.get_filenames()
    ret2 = f.get_text(item='word', delim=",")
    print(ret2.split(",")[1])
    assert ref == ret2.split(",")[1]

