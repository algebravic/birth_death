"""
Evolving Binary trees.
"""
from typing import List, Tuple
from random import random
from collections import Counter

class TreeNode:

    pass

class TreeNode:

    def __init__(self, slot: int, parent: TreeNode | None):

        self._slots = [None, None]
        self._parent = parent
        self._height = 0 if parent is None else parent._height + 1
        self._slot = slot

    @property
    def slot(self, num: int) -> TreeNode | None:

        return self._slots[num]

    def grow(self, slot: int) -> TreeNode | None:
        """
        Grow a tree in the slot
        """
        if self._slots[slot] is None:
            self._slots[slot] = TreeNode(slot, self)
            return self._slots[slot]
        else:
            return None

    @property
    def is_empty(self):

        return all((val is None for val in self._slots))

    def shrink(self) -> TreeNode | None:

        if self.is_empty:
            if self._parent is not None:
                self._parent._slots[self._slot] = None
            return self._parent
        return None

    @property
    def height(self) -> int:

        return self._height
    
def _del_sub(node: TreeNode):

    for ind in range(2):

        if node._slots[ind] is not None:
            _del_sub(node._slots[ind])

    del node

class BinaryTree:
    """
    A class of evolving binary trees.
    """

    def __init__(self, probs: float | List[float]):
        if isinstance(probs, float):
            self._probs = [probs, probs]
        else:
            self._probs = probs

        self._root = TreeNode(0, None)

        self._leaves = [self._root]
        self._height = 0

    def __del__(self):

        _del_sub(self._root)

    def move(self):
        """
        Make one transition.
        """
        newleaves = []
        parents = []
        # The height is the maximum height of the leaves
        for leaf in self._leaves:
            for ind in range(2):
                if random() < self._probs[ind]:
                    newleaf = leaf.grow(ind)
                    if newleaf is not None:
                        newleaves.append(newleaf)
            parent = leaf.shrink() # not None indicates death
            if parent is not None:
                if not any((_ is parent for _ in parents)):
                    parents.append(parent)
                del leaf
        self._leaves = newleaves + parents
        if self._root.is_empty: # back at start
            self._height = 0
        else:
            self._height = max((_.height for _ in self._leaves))

    @property
    def height(self):

        return self._height

    @property
    def is_root(self):

        return self._height == 0

def simulate(prob: float, height_bound: int, tries: int) -> Tuple[List[int], int]:
    """
    Simulate the birth/death process with an absorbing state of height_bound.
    return the list of transit times for the recurrent states, plus the number
    of absorbed.
    """

    transit = []
    absorbed = 0

    for ind in range(tries):

        tree = BinaryTree(prob)
        count = 0
        while True:
            tree.move()
            count += 1
            if tree.height == 0:
                transit.append(count)
                break
            elif tree.height >= height_bound:
                absorbed += 1
                break
        del tree
    return Counter(transit), absorbed
