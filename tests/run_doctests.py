import sys, os
sys.path.append(os.path.join("..","src"))

import doctest, psylab

doctest.testmod(psylab)
