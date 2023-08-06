# encoding: utf-8

import numpy as np

from .heap import Heap
from .heap import HeapPair


class HeapBrother(Heap):


    pass




class HeapBrotherPair(HeapBrother, HeapPair):


    pass




class HeapBrotherPairMax(HeapBrotherPair):


    def swap(self, node):

        # update tree
        ancestor         = node.parent
        descendant_left  = node.child_left.children
        descendant_right = node.child_right.children

        nodes        = np.array([node, node.child_left, node.child_right])
        nodes_values = [n.value for n in nodes]

        idx = np.argsort(nodes_values)[::-1]
        
        root, left, right = nodes[idx]

        root.parent = ancestor
        root.setas_leaf()
        root.children.append(left)
        root.children.append(right)

        left.parent    = root
        left.children  = descendant_left
        
        right.parent   = root
        right.children = descendant_right

        # update ancestor and descendant info
        if ancestor:
            if ancestor.child_left == node:
                ancestor.child_left = root
            else:
                ancestor.child_right = root

        for n in descendant_left:
            n.parent = left

        for n in descendant_right:
            n.parent = right

        # update seq
        nodes_index = [self._seq.index(n) for n in nodes]
        nodes       = nodes[idx]
        self._seq[nodes_index] = nodes

        # update root
        if root.root():
            self._heap = root

        return root, idx



    def swap_down(self, node):

        if node.leaf():
            return []

        elif node.left_only():

            if node.value >= node.child_left.value:
                return []
            else:
                # update root
                if node.root():
                    self._heap = node.child_left

                # update seq
                nodes       = [node, node.child_left]
                nodes_index = [self._seq.index(n) for n in nodes]
                nodes       = nodes[::-1]
                self._seq[nodes_index] = nodes

                # update tree
                ancestor   = node.parent
                descendant = node.child_left.children

                # update ancestor and descendant info
                if ancestor:
                    if ancestor.child_left == node:
                        ancestor.child_left = node.child_left
                    else:
                        ancestor.child_right = node.child_left

                for n in descendant:
                    n.parent = node

                # update tree
                node.child_left.parent = ancestor
                node.child_left.setas_leaf() 
                node.child_left.children.append(node)

                node.parent   = node.child_left
                node.children = descendant

                return [node]

        else:
            root, idx = self.swap(node)

            tbd = []
            if 1 != idx[1]:
                tbd.append(root.child_left)
            if 2 != idx[2]:
                tbd.append(root.child_right)

            return tbd



    def swap_up(self, node):

        if not node or node.root():
            return []

        elif node.parent.left_only():

            if node.parent.value >= node.value:
                return []
            else:
                node_parent = node.parent

                # update root
                if node_parent.root():
                    self._heap = node

                # update seq
                nodes       = [node_parent, node]
                nodes_index = [self._seq.index(n) for n in nodes]
                nodes       = nodes[::-1]
                self._seq[nodes_index] = nodes

                # update tree
                ancestor   = node_parent.parent
                descendant = node.children
                node.setas_root()
                node.setas_leaf()

                # update ancestor and descendant info
                if ancestor:
                    if ancestor.child_left == node_parent:
                        ancestor.child_left = node
                    else:
                        ancestor.child_right = node

                node_parent.setas_root()

                for n in descendant:
                    n.parent = node_parent

                # update tree
                node_parent.children = descendant

                node.child_left      = node_parent
                node.parent          = ancestor

                node_parent.parent   = node

                return [node.child_left]

        else:
            root, idx = self.swap(node.parent)

            tbd = []
            if 0 != idx[0]:
                tbd.append(root)
            if 1 != idx[1]:
                tbd.append(root.child_left)
            if 2 != idx[2]:
                tbd.append(root.child_right)

            return tbd



    def tune(self, node):

        if node.root():
            self.tune_down(node)

        elif node.leaf():
            self.tune_up(node)

        elif node.child_left and node.child_left.value >= node.value:
            self.tune_down(node)

        elif node.child_right and node.child_right.value >= node.value:
            self.tune_down(node)

        else:
            self.tune_up(node)
