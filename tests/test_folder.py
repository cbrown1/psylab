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
                          
                          
def test_cd():
    ref = "tests"
    with psylab.folder.cd(ref):
        path = os.getcwd()
    base = os.path.basename(path)
    assert ref == base


def test_concurrent_files_get_filenames():
    ref = ['0_jean', '0_took', '0_no', '0_white', '0_toys']

    f = psylab.folder.concurrent_files(concurrent_file_folders)
    ret = f.get_filenames(fmt='file')
    assert ref == ret


def test_concurrent_files_use():
    ref = '0_jean'
    f = psylab.folder.concurrent_files(concurrent_file_folders,
                                                   use={'0_name':'0_jean'}, # Only use name Jean
                                                   repeat=True,
                                                  )
    ret1 = f.get_filenames(fmt='file')
    ret2 = f.get_filenames(fmt='file')
    ret3 = f.get_filenames(fmt='file')
    assert ref == ret1[0] == ret2[0] == ret3[0] # Names should all be the same
    verbs = [ret1[1], ret2[1], ret3[1]]
    assert len(set(verbs)) == len(verbs) # Verbs should all be different


def test_concurrent_files_fullfile():
    f = psylab.folder.concurrent_files(concurrent_file_folders)
    ret1 = f.get_filenames(fmt='file')
    ref = os.path.join(f.path_list[0], ret1[0])
    f = psylab.folder.concurrent_files(concurrent_file_folders)
    ret2 = f.get_filenames()
    assert ref == ret2[0]


def test_concurrent_files_repeat():
    f_no_repeat = psylab.folder.concurrent_files(concurrent_file_folders)
    f_repeat = psylab.folder.concurrent_files(concurrent_file_folders,
                                                             repeat=True)
    for i in range(10):
        ret = f_no_repeat.get_filenames()
        ret = f_repeat.get_filenames()

    good = False
    try:
        ret = f_no_repeat.get_filenames() # Should raise StopIteration exception
    except StopIteration as e:
        good = True                       # So this is good
    assert good
    
    try:
        ret = f_repeat.get_filenames() # Should NOT raise StopIteration exception
    except StopIteration as e:
        assert False


def test_concurrent_files_text():
    ref = 'took'
    f = psylab.folder.concurrent_files(concurrent_file_folders,
                                                   text_file='tests/data/concurrent_files/concurrent_files.txt',
                                                   text_format='files,word',
                                                  )
    ret1 = f.get_filenames()
    ret2 = f.get_text(item='word', delim=",")
    print(ret2.split(",")[1])
    assert ref == ret2.split(",")[1]


def test_consecutive_files_get_filenames():
    ref = 'file1'
    f = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1')
    ret = f.get_filename(fmt='file')
    assert ref == ret


def test_consecutive_files_fullfile():
    ref = 'tests/data/consecutive_files/condition_1/file1'
    f = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1')
    ret = f.get_filename()
    assert ref == ret


def test_consecutive_files_text():
    ref = 'This is file 2 text.'
    f = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1',
                                                    text_file='tests/data/consecutive_files/consecutive_files.txt',
                                                    text_format='file,kw,sentence',
                                                   )
    ret1 = f.get_filename() # File1
    ret2 = f.get_filename() # File2
    ret3 = f.get_text(item='sentence')
    assert ref == ret3


def test_consecutive_files_range():
    ref = 'file2'
    f = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1',
                                                    file_range='2:3',
                                                   )
    ret = f.get_filename(fmt='file') # File2
    assert ref == ret


def test_consecutive_files_repeat():
    ref = 'file1'
    f_no_repeat = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1')
    f_repeat = psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1',
                                                    repeat=True,
                                                   )
    ret = f_no_repeat.get_filename()
    ret = f_no_repeat.get_filename()
    ret = f_no_repeat.get_filename()
    ret = f_repeat.get_filename()
    ret = f_repeat.get_filename()
    ret = f_repeat.get_filename()

    good = False
    try:
        ret = f_no_repeat.get_filename() # Should raise StopIteration exception
    except StopIteration as e:
        good = True                      # So this is good
    assert good
    
    try:
        ret = f_repeat.get_filename() # Should NOT raise StopIteration exception
    except StopIteration as e:
        assert False


def synched_consecutive_files_get_file():
    ref = 'file2'
    f = psylab.folder.synched_consecutive_files(
            psylab.folder.consecutive_files('tests/data/consecutive_files/condition_1'),
            psylab.folder.consecutive_files('tests/data/consecutive_files/condition_2'),
            psylab.folder.consecutive_files('tests/data/consecutive_files/condition_3'),
        )
    ret1 = f.get_filename('condition_1')
    ret2 = f.get_filename('condition_3')
    
    assert ref == ret2
