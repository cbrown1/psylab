#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
#import re
#import csv
import yaml
from yamlreader import data_merge
import numpy as np
import argparse
#import fileinput
import daiquiri
#import itertools
import datetime
#import dateutil
#import operator

from . import string


class stimulus_manager():
    """ Simple class to manage speech stimulus presentation to participants, to avoid repeated exposure across experiments
    
        The yaml db should look like this:

            subjects:
                '815':
                    stim:
                        IEEE: 
                            2019-12-01: 1-100,321-400
                            2019-12-02: 101-320
                    notes:
                        - first note
                        - second note
            corpuses:
                IEEE: 720
                CUNY: 860
                CID: 100
                CNC: 1050
                HINT: 250
                SPINLO: 200
                SPINHI: 200

        Which gets parsed to this:

            {'corpuses': {'CID': 100,
                          'CNC': 1050,
                          'CUNY': 860,
                          'HINT': 250,
                          'IEEE': 720,
                          'SPINHI': 200,
                          'SPINLO': 200},
             'subjects': {'815': {'notes': ['first note', 'second note'],
                                  'stim': {'IEEE': {2019-12-01: '1-100,321-400',
                                                    2019-12-02: '101-320'}}}}}
    """

    data = None # The yaml data object

    date_fmt = "%Y-%M-%d" # Date format


    def __init__(self, file_path=None, debug=False):

        if debug:
            daiquiri.setup(level=5)
            self.logger = daiquiri.getLogger(__name__)
        else:
            daiquiri.setup(level=50)
            self.logger = daiquiri.getLogger(__name__)

        if file_path:
            self.file_path = file_path
            self.data = self.load(file_path)

#        self.logger.debug("Check for single occurences: {}".format(self.single))
#        self.logger.debug("Check for capitalization: {}".format(self.capitalization))


    def load(self, file_path=None):
        if not file_path:
            file_path = self.file_path
        else:
            self.file_path = file_path

        self.logger.debug("Reading yml file: {}".format(file_path))
        with open(file_path) as fh:
            data = yaml.full_load(fh)
        self.data = data
        return data


    def save(self, file_path=None, data=None):
        if not file_path:
            file_path = self.file_path
        if not data:
            data = self.data

        self.logger.debug("Writing yml file: {}".format(file_path))
        with open(file_path,'w') as fh: 
            ret = yaml.dump(data, fh)
        return ret


    def stim_get_used_for_subject(self, subj_id, corpus=None):
        """Returns stimuli used by specified subject

            If subject is not found, None is returned
            If Corpus is not found for subject, an empty list is returned
            Otherwise, the stim as a print-style string is returned
            If no corpus is specified, the stim dict is returned
        """

        if subj_id in self.data['subjects'].keys():
            # This subject exists. Look for stim
            stim_data = self.data['subjects'][subj_id]['stim']
            if corpus:
                stim_list = []
                for stim_key, stim_vals in stim_data.items():
                    if stim_key == corpus:
                        # Corpus exists for this subject. Grab existing used stim
                        for session_key, session_vals in stim_vals.items():
                            stim_list.append(session_vals)
                        break
                if stim_list:
                    # Stim were found. Return consolidated list ('1-10,11-20' -> '1-20') 
                    stim_str = string.list_to_str( string.str_to_list(",".join(stim_list)) )
                    return stim_str
                else:
                    # stim_list is empty; no stim. Return empty list
                    return []
            else:
                # No corpus specified. Return entire dict
                return stim_data
        else:
            return None


    def stim_set_used_for_subject(self, subj_id, corpus, stim, date=None, overwrite=False):
        """Adds tokens to the used list for specified corpus and subject

            stim should be a print-range style string, like '1-100'

            subj_id should be a unique subject identifier

            corpus should be the name of a stimulus corpus, and listed in corpuses 

        """
        stim = stim.replace(":","-")
        stim_list = []

        if date:
            this_date = datetime.strptime(date_string, self.date_fmt)
        if not date:
            date = datetime.date.today()

        if corpus in self.data['corpuses'].keys():
            if subj_id in self.data['subjects'].keys():
                # Subject exists in db. Append data
                stim_request = string.str_to_list(stim)
                for stim_key, stim_vals in self.data['subjects'][subj_id]['stim'].items():
                    # Get any used stim from this corpus for this subject
                    if stim_key == corpus:
                        for session_key, session_vals in stim_vals.items():
                            stim_list.append(session_vals)
                        break
                if stim_list:
                    # Subject has heard some stim from this corpus. Check if current stim clash.
                    stim_used = string.str_to_list(",".join(stim_list))
                    overlap = list(set(stim_request) & set(stim_used))
                    if not overwrite and len(overlap) > 0:
                        # Conflict detected. Raise an exception
                        stim_used_str = string.list_to_str(stim_used)
                        overlap_str = string.list_to_str(overlap)
                        raise Exception("Conflict detected!\n\nParticipant: {}\nCorpus: {}\nRequested: {}\nExisting: {}\nConflicting: {}\n\nSet overwrite to True to force change".format(subj_id, corpus, stim, stim_used_str, overlap_str))
                else:
                    # Subject has not heard this corpus before. Create empty dict, so it can be appended below
                    self.data['subjects'][subj_id]['stim'][corpus] = {}

                # Check if there is an entry for today, append if so.
                stim_request_str = string.list_to_str( stim_request )
                if date in self.data['subjects'][subj_id]['stim'][corpus].keys():
                    # Subject has heard this corpus on this date. Append current stim to existing
                    stim_used = self.data['subjects'][subj_id]['stim'][corpus][date]
                    stim_this = ",".join((stim_used, stim_request_str))
                    stim_this = string.list_to_str( string.str_to_list(stim_this) ) # Ensure str is compact (eg., take care of '1-100,101-200')
                else:
                    # Subject has not heard this corpus on this day, create
                    stim_this = stim_request_str
                # Insert / overwrite stim from this day
                self.data['subjects'][subj_id]['stim'][corpus][date] = stim_this
            else:
                # Subject does not exist. Create
                stim_this = {'notes': [], 'stim': {corpus: {date: stim}}}
                self.data['subjects'][subj_id] = stim_this
        else:
            raise Exception("Error: Corpus does not exist: {}".format(corpus))


    def corpus_get_list(self):
        return list(self.data['corpuses'].keys())


    def corpus_get_n(self, corpus):
        return self.data['corpuses'][corpus]


    def corpus_add(self, corpus, n, overwrite=False):
        if not overwrite and corpus in self.data['corpuses'].keys():
            raise Exception("Error: Corpus already exists: {}".format(corpus))
        else:
            self.data['corpuses'][corpus] = n

    def create_new_db(self, file_name):
        db_prototype = {'corpuses': {},
                        'subjects': {},
                        }
        self.save(file_path=file_name, data=db_prototype)
