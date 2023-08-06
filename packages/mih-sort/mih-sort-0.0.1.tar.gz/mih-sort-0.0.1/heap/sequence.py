# encoding: utf-8

import math
import numpy as np


class Sequence(object):

    
    def __init__(self, values=[]):

        self._seq  = np.array(values)



    def index(self, value):

        return np.where(self._seq == value)[0][0]



    def tail_index(self):

        return math.floor((len(self._seq)+1)/2) - 1 



    def tail(self):

        return self._seq[self.tail_index()]



    def last(self):

        return self._seq[-1]



    def last_drop(self):

        self._seq = self._seq[:-1]



    def __getitem__(self, key):

        return self._seq[key]



    def __setitem__(self, key, value):

        self._seq[key] = value



    def append(self, value):

        self._seq = np.concatenate((self._seq, [value]))



    def __repr__(self):

        return '\n'.join([v.__repr__() for v in self._seq])
