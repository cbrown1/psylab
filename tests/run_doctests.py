import sys, os
sys.path.append(os.path.join("..","src"))

import doctest, pal

doctest.testmod(pal)
