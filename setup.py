# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import setup
import sys
sys.path.append("src")

import pal
version = pal.__version__

packages = ['pal%s' % (p) for p in ['',
                                    '.array',
                                    '.dataview',
                                    '.exper',
                                    '.hardware',
                                    '.misc',
                                    '.signal',
                                    '.stats']]
requires=[
'numpy (>=1.2)',
]

setup(name='PAL',
      version=version,
      description='PsychoAcoustics Lab',
      long_description='''\
 A loose collection of modules useful for various aspects of running psychoacoustics
 experiments, although several will be more generally useful.''',
      author='Christopher Brown, Joseph Ranweiler',
      author_email='c-b@asu.edu',
      maintainer='Christopher Brown',
      maintainer_email='c-b@asu.edu',
      url='http://www.gitorious.com/pal',
      package_dir = {'pal': 'src/pal'},
      packages = packages,
      requires = requires,
      platforms = ['any'],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering',
        ],
     )
