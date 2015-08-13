# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 16:40:41 2014

@author: code-breaker
"""

import time

class timer():
    """ Simple timer class
        
        Use to easily time blocks of code:
        
        >>> with timer():
                for i in range(1000):
                    for j in range(1000):
                        k = j*i

        0.166001081467
        >>> 
        
        Found at:
        http://mrooney.blogspot.com/2009/07/simple-timing-of-python-code.html
    """
    def __enter__(self): self.start = time.time()
    def __exit__(self, *args): print(time.time()) - self.start
