#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
import yaml
from yamlreader import data_merge
import numpy as np
import argparse
import fileinput
import daiquiri
import itertools
import datetime
import dateutil
import operator

from . import lists

class subjects():
    """ Simple class to manage subject information, IRB protocols and the consenting process 
    
        The yaml db should look like this:

            subjects:
                815:                            # Unique subject ID
                    demographic:                # Demo data, including NIH ethnic categories, useful for reporting
                        name: first last
                        dob: 1990-01-01
                        ethnic: white
                        hispanic: not hispanic
                    info:                       # A custom dict to hold any additional subject info you need
                        email: person@domain.tld # Use 

                    protocols:                  # The protocols this subject has been consented for, and the date of the consenting
                        EAS: 2019-12-01
                        SUCLE: 2019-12-02
                    experiments:                # The experiments this subject has participated in, and the date of participation
                        exp_1: 2019-12-01       # Useful for participants section of manuscripts: search for exp name < today
                        exp_2: 2019-12-02
                    notes:                      # Any notes, with date entered as the key
                        2019-12-01_1: first note
                        2019-12-01_2: second note
            protocols:                          # Available protocols, with approval and expiration dates, and a list of old expirations
                EAS: 
                    Approved: 2019-10-01
                    Expires: 2020-09-30
                    OldExpires: 
                      - 2018-09-30
                      - 2019-09-30
                SUCLE: 
                    Approved: 2019-08-01
                    Expires: 2020-07-31
                    OldExpires: 
                        - 2019-07-31
            experiments:                        # Available experiments, with the protocol it is under, and data collection start and end dates
                exp_1: 
                    protocol: EAS
                    started: 2019-11-20
                    ended: 
                exp_2: 
                    protocol: SUCLE
                    started: 2019-12-01
                    ended: 
            prototypes: 
                protocols: 
                    Approved: datetime.date
                    Expires: datetime.date
                experiments: 
                    protocol: data_list
                    started: datetime.date
                    ended: datetime.date
                subjects: 
                    demographics: 
                        name: str
                        dob: datetime.date
                        ethnic: data_list
                        hispanic: data_list
                    info: 
                        email: string
                        status: data_list
                        audio_l_125: int
                        audio_l_500: int
                        audio_l_750: int
                        audio_l_1000: int
                        audio_l_1500: int
                        audio_l_2000: int
                        audio_l_3000: int
                        audio_l_4000: int
                        audio_l_6000: int
                        audio_l_8000: int
                        audio_r_125: int
                        audio_r_500: int
                        audio_r_750: int
                        audio_r_1000: int
                        audio_r_1500: int
                        audio_r_2000: int
                        audio_r_3000: int
                        audio_r_4000: int
                        audio_r_6000: int
                        audio_r_8000: int

                data_lists: 
                    subject_info: 
                        status:
                            - Normal Hearing
                    demographics:
                        ethnic: 
                            - native
                            - asian
                            - pacific
                            - black
                            - white
                            - mixed/other
                        hispanic: 
                            - hispanic
                            - not hispanic
                            - unknown



        Which gets parsed to this:

          {'protocols': {'EAS':   {'Approved':    datetime.date(2019, 10, 1),
                                   'Expires':     datetime.date(2020, 9, 30),
                                   'OldExpires': [datetime.date(2018, 9, 30),
                                                  datetime.date(2019, 9, 30)]},
                                   'Created':     datetime.date(2017, 10, 1)
                         'SUCLE': {'Approved':    datetime.date(2019, 8, 1),
                                   'Expires':     datetime.date(2020, 7, 31),
                                   'OldExpires': [datetime.date(2019, 7, 31)]}},
                                   'Created':     datetime.date(2018, 8, 1)
           'subjects': {'815': {'info':         {'dob': datetime.date(1990, 1, 1),
                                                 'email': 'person@domain.tld',
                                                 'ethnic': 'white',
                                                 'hispanic': 'not hispanic',
                                                 'name': 'first last'},
                                'experiments':  {'exp_1': datetime.date(2019, 12, 1),
                                                 'exp_2': datetime.date(2019, 12, 2)},
                                'notes':        {'2019-12-01_1': 'first note',
                                                 '2019-12-01_2': 'second note'},
                                'protocols':    {'EAS': datetime.date(2019, 12, 1),
                                                 'SUCLE': datetime.date(2019, 12, 2)}}
                      }}
              """

    data = None # The yaml data object

    ethnic = ['native',
              'asian',
              'pacific',
              'black',
              'white',
              'mixed/other',
              ]

    hispanic = ['hispanic',
                'not hispanic',
                'unknown',
               ]

    gender = ['male',
             'female',
             ]

    data_fmt = "%Y-%m-%d"

    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq,
           '!=': operator.ne,
          }

    # Print warning for any protocols that have expiration dates that are this many days away or less
    # Set to 0 for no warnings
    # TODO: Add this check to __init__
    protocol_warning_days = 60


    def __init__(self, source_files, acronyms=None, template=None, acronym_metavar=None, template_metavar=None, capitalization=True, sentence_delims=None, single=True, debug=False):

        if debug:
            daiquiri.setup(level=5)
            self.logger = daiquiri.getLogger(__name__)
        else:
            daiquiri.setup(level=50)
            self.logger = daiquiri.getLogger(__name__)
        self.meta,body = self.init_source_files(source_files)
        self.single = single
        self.capitalization = capitalization
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
    {'815': {'info':         {'dob': datetime.date(1990, 1, 1),
                              'email': 'person@domain.tld',
                              'ethnic': 'white',
                              'hispanic': 'not hispanic',
                              'name': 'first last'},
             'experiments':  {'EAS_1': datetime.date(2019, 12, 1),
                              'EAS_2': datetime.date(2019, 12, 2)},
             'notes':        {'2019-12-01_1': 'first note',
                              '2019-12-01_2': 'second note'},
             'protocols':    {'EAS': datetime.date(2019, 12, 1),
                              'SUCLE': datetime.date(2019, 12, 2)}}
           }
    """

    def subject_get_unique_id(self):
        ids = list(self.data['subjects'].keys())
        # Find the first (smallest) integer not in list
        id = next(itertools.filterfalse(set(ids).__contains__, itertools.count(1)))
        return id


    def subject_get_consent_date(self, id, protocol):
      """Return the date that a specified participant was consented on a specified protocol
      """
        consent_data = self.data['subjects'][id]['consent']
        ret = None
        for this_protocol in consent_data.keys():
            if this_protocol == protocol:
                ret = data[id]['consent'][protocol]
                break
        return ret


    def subject_get_protocols(self, id):
        """Return the protocols that a specified participant has been consented for

            For a given id, returns a dict with protocol names as keys, and formatted dates as vals
        """
        consent_data = self.data['subjects'][id]['consent']
        ret = {}
        for this_protocol, this_date in consent_data.items():
            ret[this_protocol] = this_date.strftime(self.date_fmt)
        return ret


    def subject_get_experiments(self, id, protocol=None):
        """Return the experiments that a specified participant has participated in

            For a given id, returns a dict with experiment names as keys, and formatted dates as vals
        """
        consent_data = self.data['subjects'][id]['consent']
        ret = {}
        for this_protocol, this_date in consent_data.items():
            ret[this_protocol] = this_date.strftime(self.date_fmt)
        return ret


    def subject_create(self, id=None, overwrite=False):
        """Adds a participant to the subjects database
           # TODO: Check that experiment is not ended
           # TODO: Check that protocol is not expired
        """

        if not id:
            id = self.subject_get_unique_id()
        elif id in self.data['subjects'].keys():
            raise Exception("Subject ID found in database: {:}".format(id))




    def subject_add_experiment(self, id, experiment, date=None, overwrite=False):
        """Adds an experiment to the list of experiments participated in by a given subject
           # TODO: Check that experiment is not ended
           # TODO: Check that protocol is not expired
        """

      #if id in self.data['subjects'].keys():


      pass


    def subject_add_protocol(self, id, protocol, date=None, overwrite=False):
        """Adds an experiment to the list of experiments participated in by a given subject
           # TODO: Check that experiment is not ended
           # TODO: Check that protocol is not expired
        """

      #if id in self.data['subjects'].keys():


      pass


    def subject_filter(self, filters=None, sublist=None):
        """Returns a subset of participants that meet the specified criteria

            filters should be a dict in which the keys are one of:
                info
                consent
                experiments
                protocols

            # TODO: Look at fnmatch for wildcards:
            # import fnmatch
            # lst = ['this','is','just','a','test']
            # filtered = fnmatch.filter(lst, 'th?s')

            and the vals are 3-element tuples in which the first element is the name of a 
            variable (or '*' for any variable), the second is one of the following operators:

                '<'  - is less than                (numbers, dates)
                '>'  - is greater than             (numbers, dates)
                '<=' - is less than or equal to    (numbers, dates)
                '>=' - is greater than or equal to (numbers, dates)
                '='  - is equal to                 (numbers, dates, strings)
                '!=' - is not equal to             (numbers, dates, strings)
                '~'  - contains                    (strings)
                '~@' - contains, ignore case       (strings)
                '=@' - is equal to, ignore case    (strings)

            and the third is a value. 

            An example of a filters dict:
                filters = {
                           'consent':      ('EAS', '<', '2019-12-01'), # Only subjects consented before Dec 1
                           'info':         ('gender', '=', 'male'), # Only males
                           'notes':        ('*', '~', 'CAB')        # Any note that contains 'CAB'
                          }
        """

        ret = {}
        for id, data in self.data['subjects'].items():
            if not sublist or (id in sublist.keys()):
                keep = False
                for filt_key, filt_vals in filters.items():
                    vals = []
                    if filt_vals[0] == "*":
                        for key in data[filt_key].keys():
                            vals.append(key)
                    else:
                        vals.append(data[filt_key][filt_vals[0]])
                    this_op = filt_vals[1]
                    try:
                        this_ref = datetime.datetime.strptime(filt_vals[2], self.date_fmt)
                    except ValueError:
                        this_ref = filt_vals[2]
                    for this_val in vals:
                        if this_op in self.ops.keys():
                            if self.ops[this_op](this_val, this_ref):
                                keep = True
                                break
                        elif this_op == "~":
                            if this_ref in this_val 
                                keep = True
                                break
                        elif this_op == "~@":
                            if this_ref.lower() in this_val.lower()
                                keep = True
                                break
                        elif this_op == "=@":
                            if this_ref.lower() == this_val.lower()
                                keep = True
                                break
                        else:
                            raise Exception("Unknwon operator: {}".format(this_op))
                    if keep:
                        break
                if keep:
                    ret[id] = data
        return ret


    def protocol_create(self, protocol, created=None, approved=None, expires=None):
      """Adds a protocol to the protocols list
          
          Default dates are:

            created: today
            approved: today
            expires: 1 year from today
      """
      if protocol in self.data['protocols'].keys():
          info = self.data['protocols'][protocol]
          raise Exception("Protocol exists!\n\nProtocol: {}\nCreated: {}\nApproved: {}\nExpires: {}\n\nNo action taken.".format(protocol, 
                                                                                                                                info['Created'], 
                                                                                                                                info['Approved'],
                                                                                                                                info['Expires'] ))
      # Ensure all times are datetime objects, convert from strings if needed
      # If dates are not given, assume created and approved today & expires 1 year from now
      if not created:
          created_obj = datetime.datetime.now() #.strftime(self.date_fmt)
      else:
          if isinstance(created, str):
              created_obj = datetime.datetime.strptime(created, self.date_fmt)
          else:
              created_obj = created
      if not approved:
          approved_obj = created_obj
      else:
          if isinstance(approved, str):
              approved_obj = datetime.datetime.strptime(approved, self.date_fmt)
          else:
              approved_obj = approved
      if not expires:
          expires_obj = approved.replace(year=approved_obj.year+1)
      else:
          if isinstance(expires, str):
              expires_obj = datetime.datetime.strptime(expires, self.date_fmt)
          else:
              expires_obj = expires

      self.data['protocols'][protocol] = {
                                          "Created": created_obj, 
                                          "Approved": approved_obj,
                                          "Expires": expires_obj,
                                          "OldExpires": [None],
                                         }


    def protocol_update(self, protocol, approved, expires=None):
      """Update specified protocol with new approved and expires dates
      """
      if protocol not in self.data['protocols'].keys():
          raise Exception("Protocol does not exist!\n\nProtocol: {}\n\nNo action taken.".format( protocol ))

      if isinstance(approved, str):
          approved_obj = datetime.datetime.strptime(approved, self.date_fmt)
      else:
          approved_obj = approved
      if not expires:
          expires_obj = approved.replace(year=approved_obj.year+1)
      else:
          if isinstance(expires, str):
              expires_obj = datetime.datetime.strptime(expires, self.date_fmt)
          else:
              expires_obj = expires
      # Save the expires date for posterity
      if len(OldExpires) == 1 and OldExpires[0] == None:
          # OldExpires is empty (ie., it contains only a None)
          self.data['protocols'][protocol]['OldExpires'][0] = self.data['protocols']['protocol']['Expires']
      else:
          # Not empty. Just append
          self.data['protocols'][protocol]['OldExpires'].append(self.data['protocols']['protocol']['Expires'])
      # Update the approved and expires dates
      self.data['protocols'][protocol]['Approved'] = approved_obj
      self.data['protocols'][protocol]['Expires'] = expires_obj


    def experiment_create(self, experiment, protocol, started=None):
        """Adds an experiment

                exp_1: 
                  protocol: EAS
                  started: 2019-11-20
                  ended: 
        """
        if experiments in self.data['experiments'].keys():
          info = self.data['experiments'][experiment]
          raise Exception("Experiment exists!\n\nExperiment: {}\nProtocol: {}\nstarted: {}\n\nNo action taken.".format(experiment, 
                                                                                                                       info['protocol'], 
                                                                                                                       info['started'] ))
        if protocol not in self.data['protocol'].keys():
          raise Exception("Experiment protocol does not exist!\n\nExperiment: {}\nProtocol: {}\n\nNo action taken.".format(experiment, protocol))

        if not started:
          started_obj = datetime.datetime.now() #.strftime(self.date_fmt)
        else:
          if isinstance(started, str):
              started_obj = datetime.datetime.strptime(started, self.date_fmt)
          else:
              started_obj = started

        self.data['experiment'][experiment] = {
                                             "protocol": protocol, 
                                             "started": started_obj,
                                             "ended": None,
                                            }

    def experiment_end(end, experiment ended=None):

        if not ended:
            ended_obj = datetime.datetime.now() #.strftime(self.date_fmt)
        else:
            if isinstance(ended, str):
                ended_obj = datetime.datetime.strptime(ended, self.date_fmt)
            else:
                ended_obj = ended

        if self.data['experiment'][experiment]['ended']:
          raise Exception("Experiment is already ended!\n\nExperiment: {}\nProtocol: {}\nEnded: {}\nRequested End: {}\n\nNo action taken.".format(experiment, 
                                                                                                                                                  protocol,
                                                                                                                                                  self.data['experiment'][experiment]['ended'],
                                                                                                                                                  ended_obj))
        self.data['experiment'][experiment]['ended'] = ended_obj


if __name__ == "__main__":

    def add_bool_arg(parser, name, default=False, help=None):
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument('--' + name, dest=name, action='store_true', help=help)
        group.add_argument('--no-' + name, dest=name, action='store_false')
        parser.set_defaults(**{name:default})

    parser = argparse.ArgumentParser(description = "Simple pandoc preprocessor script to process acronyms. Use the acronym throughout your document, and this preprocessor will replace the first occurence with text specified in the template. By default, an acronym will be replaced with only the phrase (not the template) when there is only 1 occurence of the acronym. Also by default, the phrase will be capitalized using sentence case when it begins a sentence.")
    parser.add_argument("-o", "--output", default=None, type=str,
                        help="the path to the output md file. If ommitted, write to stdout")
    parser.add_argument("-d", "--debug", default=False, action='store_true',
                        help="Include switch to enable debugging output. Default = no debugging")

    add_bool_arg(parser, 'capitalization', default=True, help="Check to see if each phrase begins a sentence and should be capitalized. Default = True")

    parser.add_argument("-C", "--sentence_delims", default=None, type=str,
                        help="A comma-delimited string specifying characters to interpret as sentence delimiters. Only used when capitalization is True. By default the chars '.', '!', '?', and '\n' are used. If you include this argument, only the items in your list will be checked. eg., --sentence_delims '.,!,?,\n'")
    parser.add_argument("-s", "--single", default=True, action='store_true',
                        help="If True, and only one occurence of an acronym is found, replace with phrase, not template. Default = True")
    parser.add_argument("-m", "--template_metavar", default=None, type=str,
                        help="A string specifying the name of the metadata variable in which to look for the template string. default = acronyms_template")
    parser.add_argument("-v", "--acronym_metavar", default=None, type=str,
                        help="A string specifying the name of the metadata variable in which to look for the acronym/phrase pairs (as a dict). default = acronyms_vars")
    parser.add_argument("-t", "--template", default=None, type=str,
                        help="A string specifying the template to use. There are two variables available: $acronym and $phrase. A typical template might be '$phrase ($acronym)'")
    parser.add_argument("-a", "--acronyms", default=None, type=str, action='append',
                        help="A comma-separated list of acronym:phrase variable pairs, themselves delimited with a colon: acro1:phrase1,acro2:phrase2")
    parser.add_argument("source_files", nargs='+', type=str,
                        help="the path to the source md file or files, or - for stdin") # Returns a list
    args = parser.parse_args()

    acronyms = {}
    if args.acronyms:
        for pair in args.acronyms:
            acro,phrase = pair.split(":")
            acronyms[acro] = phrase.strip("'\"")

    preproc = preproc_acronyms(args.source_files, acronyms=acronyms, template=args.template, single=args.single, capitalization=args.capitalization, acronym_metavar=args.acronym_metavar, template_metavar=args.template_metavar, debug=args.debug, sentence_delims=args.sentence_delims)

    delim = "---" + os.linesep
    # Create new file. The metadata here is ugly but usable
    new_file = delim + yaml.safe_dump(preproc.meta) + delim + preproc.body

    if args.output:
        with open(args.output, "w") as f:
            f.write(new_file)
            f.flush()
    else:
        print(new_file)
