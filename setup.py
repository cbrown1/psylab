# -*- coding: utf-8 -*-

# Copyright (c) 2010-2014 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other 
# contributions are welcome. Go to http://code.google.com/p/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

#from distutils.core import setup
from distutils.sysconfig import get_python_lib
from setuptools import setup
import sys, os
import psylab
version = psylab.__version__

package_dir = { 'psylab': 'psylab', 
              }
package_data = {'psylab': [ 'subject_manager/*.ui',
                            'subject_manager/*.sql',
                            'subject_manager/images/*.*',
                            'misc/*.csl',
                          ],
                }

requires = ['numpy (>=1.2)',
            'scipy (>=0.12)',
            'matplotlit (>=1.2)',
            ]

packages = ['psylab%s' % (p) for p in ['',
                                    '.io',
                                    '.dataview',
                                    '.gustav',
                                    '.gustav.methods',
                                    '.gustav.frontends',
                                    '.tools',
                                    '.signal',
                                    '.stats',
                                    '.subject_manager',
                                    ]
            ]
#packages.append('psylab_examples')

requires=[
'numpy (>=1.2)',
'scipy (>=0.12)',
'matplotlib (>=1.1)',
]

setup(name='PsyLab',
      version=version,
      description='PsyLab: Psychophysics Lab',
      long_description='''\
 Psylab is a loose collection of modules useful for various aspects of running
 psychophysics experiments, although some might be more generally useful.''',
      author='Christopher Brown',
      author_email='cbrown1@pitt.edu',
      maintainer='Christopher Brown',
      maintainer_email='cbrown1@pitt.edu',
      url='http://www.psylab.us',
      packages = packages,
      package_dir = package_dir,
      package_data = package_data,
      requires = requires,
      platforms = ['any'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering',
        ],
     )
