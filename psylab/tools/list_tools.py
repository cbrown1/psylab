# -*- coding: utf-8 -*-

from functools import reduce
import numpy as np

def str_to_list(s):
    """Translate a print-range style string to a list of integers

      The input should be a string of comma-delimited values, each of
      which can be either a number, or a colon-delimited range. If the
      first token in the list is the string "random" or "r", then the
      output list will be randomized before it is returned ("r,1:10").

      >>> str_to_list('1:5, 20, 22')
      [1, 2, 3, 4, 5, 20, 22]
    """
    s = s.strip()
    randomize = False
    if s.count(":"):
        tokens = [x.strip().split(":") for x in s.split(",")]
    else:
        tokens = [x.strip().split("-") for x in s.split(",")]

    if tokens[0][0] in ["random","r","rand"]:
        randomize = True
        tokens = tokens[1:]

    # Translate ranges and enumerations into a list of int indices.
    def parse(x):
        if len(x) == 1:
            if x == [""]:  # this occurs when there are trailing commas
                return []
            else:
                #return map(int, x)
                return [int(x[0])]
        elif len(x) == 2:
            a,b = x
            return range(int(a), int(b)+1)
        else:
            raise ValueError

    result = list()
    for tok in tokens:
        result += parse(tok)

    if randomize:
        np.random.shuffle(result)

    return result


def list_to_str(data):
    """Translate a list of integers to a print-range style string

      The input should be a list or array of integers, and the output
      will be a string of comma-delimited values, each of
      which will be either a number, or a colon-delimited range.

      >>> list_to_str([1,2,3,4,12,14,15,16])
      '1:4,12,14:16'
    """
    data = np.array(data)
    runs = np.split(data, np.where(np.diff(data) != 1)[0]+1)
    str = []
    for run in runs:
        if run.size == 1:
            str.append("{:}".format(run[0]))
        else:
            str.append("{:}:{:}".format(run[0], run[-1]))
    return ",".join(str)
