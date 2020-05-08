# PsyLab - Psychophysics Lab

## News

- Version 1.0.2 (2020-03-22)
	- psylab.list -> psylab.list_str -> (currently) psylab.string
	- Added class string.reverse_template
	- Added functions time.seconds_to_time, time.time_to_seconds
	- Improved setup.py
	    - Added install_requires
	    - Improved version info sharing between setup.py and psylab module

- Version 1.0.0 (2019-09-11)
    - Significant reorganization, with all tools submodules moved to root, and _tools suffix removed:
	    - psylab.tools.config_tools -> psylab.config
	    - psylab.tools.data_tools -> psylab.data
	    - psylab.tools.folder_tools -> psylab.folder
	    - psylab.tools.list_tools -> psylab.list
	    - psylab.tools.measurement_tools -> psylab.measurement
	    - psylab.tools.path_tools -> psylab.path
	    - psylab.tools.plot_tools -> psylab.plot
	    - psylab.tools.stats_tools -> psylab.stats
	    - psylab.tools.time_tools -> psylab.time
	    - psylab.signal -> psylab.signal # No change

- Version 0.3.8 (2014-04-02)
  - Fix: Added dependencies to fix easy_install error

- Version 0.3.7 (2014-04-02)
  - First Pypi release

- Version 0.1.0 (2012-06-30)
  - First offical release
