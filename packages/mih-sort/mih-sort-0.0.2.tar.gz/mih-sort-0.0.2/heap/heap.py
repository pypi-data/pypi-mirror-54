# encoding: utf-8

import numpy   as np
import _pickle as pickle

from .node     import NodeBinary
from .sequence import Sequence


class Heap(object):


    def __init__(self, key, value):

        self._heap = NodeBinary(key=key)
        self._heap.value = value

        self._seq  = Sequence([self._heap])



    def swap(self):

        pass



    def tune_up(self, node):

        pass



    def tune_down(self, node):

        pass



    def tune_init(self):

        for i in range(self._seq.tail_index(),-1,-1):
            self.tune_down(self._seq[i])



    def tune(self, node):

        if node.root():
            self.tune_down(node)

        elif node.leaf():
            self.tune_up(node)



    def add(self, value):

        pass



    def delete(self):

        pass



    def save(self, fn):

        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)



    def load(self, fn):

        with open(fn, 'rb') as f:
            d = pickle.load(f)
            self.__dict__.update(d)





class HeapPair(Heap):



    def tune_down(self, node):

        nodes = [node]

        while(nodes):

            n = nodes.pop()
            nodes.extend(self.swap_down(n))



    def tune_up(self, node):

        nodes = [node]

        while(nodes):

            n = nodes.pop()
            nodes.extend(self.swap_up(n))
         


    def add(self, key, value):

        # new node
        node_parent = self._seq.tail()
        node        = NodeBinary(parent=node_parent, key=key)
        node.value  = value

        # refresh node parent
        node_parent.children.append(node)

        # refresh heap
        self._seq.append(node)

        # tune
        self.tune_up(node)



    def delete(self, key):

        node = self[key]

        # update seq
        idx = self._seq.index(node)
        node_last = self._seq.last()
        self._seq[idx] = node_last
        self._seq.last_drop()

        # update descendant info
        node_last.parent.children = [n for n in node_last.parent.children
                                       if n != node_last and n != node]

        # update tree
        node_last.parent   = node.parent
        node_last.children = [n for n in node.children if n != node_last]

        # update ancestor and descendant info
        if node.parent:
            if node.parent.child_left == node:
                node.parent.child_left = node_last
            else:
                node.parent.child_right = node_last

        for n in node.children:
            n.parent = node_last

        # update root
        if node_last.root():
            self._heap = node_last

        # tune
        self.tune(node_last)



    def __getitem__(self, key):

        for node in self._seq:
            if key == node.key:
                return node

        return None



    def update(self, key, value):

        node = self[key]
        node.value += value

        self.tune(node)

        return node
