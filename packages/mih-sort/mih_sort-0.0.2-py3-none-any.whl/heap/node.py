# encoding: utf-8

import json


class Node(object):


    def __init__(self, parent=None, key=None):

        self.reset()

        self.parent   = parent
        self.key      = key



    def reset(self):

        self.setas_root()

        self.key      = None
        self.value    = 0

        self.setas_leaf()



    def setas_root(self):

        self.parent   = None



    def setas_leaf(self):

        self.children = {}



    def root(self):

        return self.parent is None



    def leaf(self):

        return not bool(self.children)



    def meaningless(self):

        return 0 == self.value



    def __repr__(self):

        return ', '.join((str(id(self.parent)),
                         str(self.key),
                         str(self.value),
                         str(self.root()),
                         str(self.leaf()),
                         json.dumps({
                             k:id(v) for k, v in self.children.items()
                         }, ensure_ascii=False)))





class NodeBinary(Node):


    def __init__(self, parent=None, key=None):

        super(NodeBinary, self).__init__(parent, key)



    def setas_leaf(self):

        self.children = []


    @property
    def child_left(self):

        try:
            return self.children[0]
        except:
            return None



    @child_left.setter
    def child_left(self, node):

        try:
            self.children[0] = node
        except:
            self.children.append(node)



    @property
    def child_right(self):

        try:
            return self.children[1]
        except:
            return None



    @child_right.setter
    def child_right(self, node):

        try:
            self.children[1] = node
        except:
            self.children.append(node)



    def left_only(self):

        return 1 == len(self.children)



    def __repr__(self):

        return ', '.join((str(id(self.parent)),
                          str(id(self)),
                          str(self.key),
                          str(self.value),
                          str(self.root()),
                          str(self.leaf()),
                          json.dumps([id(v) for v in self.children], ensure_ascii=False)))
                          #self.children.__repr__()))
