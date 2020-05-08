#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
#import re
#import csv
import yaml
#from yamlreader import data_merge
#import numpy as np
import argparse
#import fileinput
import daiquiri
#import itertools
import datetime
#import dateutil
#import operator

from . import list_str


class stimuli():
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
                                  'stim': {'IEEE': {datetime.date(2019, 12, 1): '1-100,321-400',
                                                    datetime.date(2019, 12, 2): '101-320'}}}}}
    """

    data = None # The yaml data object

    def yml_load(self, file_path=None):
        if not file_path:
            file_path = self.file_path
        else:
            self.file_path = file_path
        self.logger.debug("Reading yml file: {}".format(file_path))

        with open(file_path) as fh:
            data = yaml.full_load(fh)
        self.data = data
        return data


    def yml_write(self, file_path=None, data=None):
        if not file_path:
            file_path = self.file_path
        if not data:
            data = self.data

        with open(file_path,'w') as fh: 
            ret = yaml.dump(data, fh)
        return ret


    def __init__(self, file_path, debug=False):

        if debug:
            daiquiri.setup(level=5)
            self.logger = daiquiri.getLogger(__name__)
        else:
            daiquiri.setup(level=50)
            self.logger = daiquiri.getLogger(__name__)

        self.file_path = file_path
        self.data = self.yml_read(file_path)

        self.logger.debug("Check for single occurences: {}".format(self.single))
        self.logger.debug("Check for capitalization: {}".format(self.capitalization))

        if sentence_delims:
            self.sentence_delims = [d.strip("'\"") for d in sentence_delims.split(",")]
            self.logger.debug('Overwrote sentence_delims with command line variable: {}'.format(sentence_delims))
        elif self.meta.has_key('sentence_delims'):
            self.sentence_delims = [d.strip("'\"") for d in self.meta['sentence_delims'].split(",")]
            self.logger.debug('Overwrote sentence_delims with metadata variable: {}'.format(self.meta['sentence_delims']))
        else:
            self.logger.debug('Using default sentence_delims variable: {}'.format(",".join(self.sentence_delims)))

        # Process acronyms in reverse priority order, so that higher priorities overwrite lower
        if self.meta.has_key(self.acronym_vars_metavarname):
            for key,val in self.meta[self.acronym_vars_metavarname].iteritems():
                self.acronyms[key] = val
                self.logger.debug('Found acronym in default metadata variable acronym_vars. acronym: {}; phrase: {}'.format(key, val))
        if acronym_metavar:
            if self.meta.kas_key(acronym_metavar):
                for key, val in self.meta[acronym_metavar].iteritems():
                    self.acronyms[key] = val
                    self.logger.debug('Found acronym in metadata variable (from command line) {}. acronym: {}; phrase: {}'.format(acronym_metavar, key, val))
        if acronyms:
            for key, val in acronyms.iteritems():
                self.acronyms[key] = val
                self.logger.debug('Found acronym in command line variable. acronym: {}; phrase: {}'.format(key, val))

        if template: # First priority is template at command line
            self.template = template
            self.logger.debug('Found template in command line: {}'.format(self.template))
        elif template_metavar and self.meta.kas_key(template_metavar): # Next priority is metavar specified by command line
            self.template = self.meta[template_metavar]
            source = 'metadata variable (from command line)'
            self.logger.debug('Found template in metadata variable (from command line): {}'.format(self.template))
        else: # Last priority is default metadata variable
            self.template = self.meta[self.acronym_template_metavarname]
            source = 'default metadata variable'
            self.logger.debug('Found template in default metadata variable: {}'.format(self.template))

        self.body = self.process(body)

    """
                 'subjects': {'815': {'notes': ['first note', 'second note'],
                                      'stim': {'IEEE': {datetime.date(2019, 12, 1): '1-100,321-400',
                                                        datetime.date(2019, 12, 2): '101-320'}}}}}
    """

    def get_stim_used_for_subject(self, id, corpus):
        stim_data = self.data['subjects'][id]['stim']
        stim_list = []
        for stim_key, stim_vals in stim_data.items():
            if stim_key == corpus:
                for session_key, session_vals in stim_vals.items():
                    stim_list.append(session_vals)
                break
        stim_str = lists.list_to_str( lists.str_to_list(",".join(stim_list)).sort() )
        return 


    def set_stim_used_for_subject(self, id, corpus, stim, force=False):
        stim_list = []
        stim_request = lists.str_to_list(stim)
        for stim_key, stim_vals in self.data['subjects'][id]['stim'].items():
            # Get any used stim from this corpus for this subject
            if stim_key == corpus:
                for session_key, session_vals in stim_vals.items():
                    stim_list.append(session_vals)
                break
        if stim_list:
            # This subject has heard some stim from this corpus. Check if current stim clash.
            stim_used = lists.str_to_list(",".join(stim_list)).sort()
            overlap = list(set(stim_request) & set(stim_used))
            if len(overlap) > 0:
                stim_used_str = lists.str_to_list(self.list_to_str(stim_used))
                overlap_str = lists.list_to_str(overlap)
                raise Exception("Conflict detected!\n\nParticipant: {}\nCorpus: {}\nRequested: {}\nPrevious: {}\nOverlap: {}\n\nSet force to True to override".format(id, corpus, stim, stim_used_str, overlap_str))
        # Check if there is an entry for today, append if so.
        today = datetime.date.today()
        stim_request_str = lists.list_to_str( stim_request )
        if today in self.data['subjects'][id]['stim'][corpus].keys():
            stim_used = self.data['subjects'][id]['stim'][corpus][today]
            stim_this = ",".join(stim_used, stim_request_str)
            stim_this = lists.list_to_str( lists.str_to_list(stim_this) ) # Ensure str is compact (eg., take care of '1-100,101-200')
        else:
            stim_this = stim_request_str
        self.data['subjects'][id]['stim'][corpus][today] = stim_this


if __name__ == "__main__":

    def add_bool_arg(parser, name, default=False, help=None):
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument('--' + name, dest=name, action='store_true', help=help)
        group.add_argument('--no-' + name, dest=name, action='store_false')
        parser.set_defaults(**{name:default})

    parser = argparse.ArgumentParser(description = "Database manager for subject exposure to speech stimuli")
    parser.add_argument("-f", "--file", default=None, type=str,
                        help="the path to the database yml file")
    parser.add_argument("-d", "--debug", default=False, action='store_true',
                        help="Include switch to enable debugging output. Default = no debugging")
    parser.add_argument("-i", "--id", default=None, type=str,
                        help="Subject ID")
    parser.add_argument("-c", "--corpus", default=None, type=str,
                        help="Stimulus corpus to use")
    parser.add_argument("-s", "--set", default=None, type=str,
                        help="Set a range of stimuli for a subject")
    parser.add_argument("-t", "--stim", default=None, type=str,
                        help="Stimulus range (used with --set)")
    parser.add_argument("-g", "--get", default=True, action='store_true',
                        help="Get list of stimuli used by a subject")
    args = parser.parse_args()

    stim = stimuli(args.file, args.debug)

    if args.get:
        ret = stim.get_stim_used_for_subject(id=args.id, corpus=args.corpus)
        print(ret)
    elif args.set:
        ret = stim.set_stim_used_for_subject(id=args.id, corpus=args.corpus, stim=args.stim)
        stim.yml_write()

