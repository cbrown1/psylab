# -*- coding: utf-8 -*-

# Copyright (c) 2010-2020 Christopher Brown
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
# contributions are welcome. Go to http://github.com/cbrown1/psylab/ 
# for more information and to contribute. Or send an e-mail to: 
# cbrown1@pitt.edu.
#

#from distutils.core import setup
from distutils.sysconfig import get_python_lib
import setuptools
#from setuptools import setup
import sys, os
import subprocess

out = subprocess.Popen(['python', 'psylab/version.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout,stderr = out.communicate()
version = str(stdout)

package_dir = { 'psylab': 'psylab', 
              }
package_data = {}

requires = ['numpy (>=1.2)',
            'scipy (>=0.12)',
            'matplotlib (>=1.2)',
            'pyaml',
            'yamlreader',
            'daiquiri',
            ]

packages = ['psylab{}'.format(p) for p in ['',
                                    '.config',
                                    '.data',
                                    '.folder',
                                    '.list_str',
                                    '.measurement',
                                    '.path',
                                    '.plot',
                                    '.signal',
                                    '.stats',
                                    '.time',
                                    ]
            ]
#packages.append('psylab_examples')

setuptools.setup(name="PsyLab",
      version=version,
      description="PsyLab: Psychophysics Lab",
      long_description="""\
 Psylab is a loose collection of modules useful for various aspects of running
 psychophysics experiments, although some might be more generally useful.""",
      author="Christopher Brown",
      author_email="cbrown1@pitt.edu",
      maintainer="Christopher Brown",
      maintainer_email="cbrown1@pitt.edu",
      url="http://www.github.com/cbrown1/psylab",
      packages = setuptools.find_packages(),
      package_dir = package_dir,
      package_data = package_data,
      install_requires = requires,
      platforms = ["any"],
      classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Scientific/Engineering",
        ],
     )
