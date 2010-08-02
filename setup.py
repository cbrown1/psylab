# -*- coding: utf-8 -*-

from distutils.core import setup
import sys
sys.path.append("src")

import pal
version = pal.__version__

packages = ['pal'+p for p in ['', '.signal', '.dataview',
                                '.stats', '.misc', '.array']]

setup(name='PAL',
      version=version,
      description='PsychoAcoustics Lab',
      author='Christopher Brown, Joseph Ranweiler',
      author_email='c-b@asu.edu',
      maintainer='Christopher Brown',
      maintainer_email='c-b@asu.edu',
      url='',
      package_dir = {'pal': 'src/pal'},
      packages = packages,
      platforms = ['any'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering',
        ],
     )
