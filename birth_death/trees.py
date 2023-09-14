"""
Evolving Binary trees.
"""
from typing import List, Tuple, Iterable
from random import random
from collections import Counter
from itertools import chain

class TreeNode:

    pass

OPERATION = Tuple[str, TreeNode] | Tuple[str, TreeNode, int]

class TreeNode:

    def __init__(self, slot: int, parent: TreeNode | None):

        self._slots = [None, None]
        self._parent = parent
        self._height = 0 if parent is None else parent._height + 1
        self._slot = slot

    def empties(self) -> Iterable[int]:
        """
        Sequence of empty slots.
        """
        yield from ((ind for ind, val in enumerate(self._slots)
                     if val is None))

    def grow(self, slot: int) -> TreeNode | None:
        """
        Grow a tree in the slot, if possible and return
        the new tree.  Otherwise return None.
        """
        if self._slots[slot] is None:
            self._slots[slot] = TreeNode(slot, self)
            return self._slots[slot]
        else:
            return None

    @property
    def is_empty(self):

        return all((val is None for val in self._slots))

    def shrink(self) -> Iterable[OPERATION]:
        """
        If this node is should be deleted, modify
        the parent pointer (if any) to be None,
        and return the parent.  Otherwise return None.
        """
        parent = self._parent
        if parent is not None:
            parent._slots[self._slot] = None
        return parent

    @property
    def height(self) -> int:

        return self._height
    
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
        self._maxleaves = 1

    def _process(self, leaf: TreeNode) -> Iterable[OPERATION]:
        for ind in leaf.empties():
            if random() <= self._probs[ind]:
                yield ('a', (leaf, ind)) # add a new node at leaf[ind]
        if leaf.is_empty and leaf is not self._root:
            yield ('d', leaf) # delete this node
        
    def move(self):
        """
        Make one transition.
        """
        newleaves = []
        parents = []
        # Note: list is important
        # We must process everything before doing surgery
        for op, args in list(chain(*map(self._process, self._leaves))):
            if op == 'a':
                leaf, ind = args
                node = leaf.grow(ind)
                if node is not None:
                    newleaves.append(node)
            elif op == 'd':
                parent = args.shrink()
                if (parent is not None
                    and not any((_ is parent for _ in parents))):
                    parents.append(parent)
                del args
            else:
                raise ValueError(f"Illegal operation {op}")
        self._leaves = newleaves + parents
        self._maxleaves = max(self._maxleaves, len(self._leaves))
        if self._root.is_empty: # back at start
            self._height = 0
        else:
            self._height = max((_.height for _ in self._leaves))

    @property
    def maxleaves(self):
        """
        The maximum number of leaves during simulation
        """
        return self._maxleaves
    
    @property
    def height(self):

        return self._height

    @property
    def is_root(self):

        return self._height == 0

def one_sim(prob: float, height_bound) -> Tuple[str, int] | str:
    tree = BinaryTree(prob)
    count = 0
    while True:
        tree.move()
        count += 1
        if tree.is_root:
            return ('r', count), tree.maxleaves
        elif tree.height >= height_bound:
            return ('a', count), tree.maxleaves
    del tree
    
def simulate(prob: float, height_bound: int, tries: int) -> Tuple[List[int], int]:
    """
    Simulate the birth/death process with an absorbing state of height_bound.
    return the list of transit times for the recurrent states, plus the number
    of absorbed.
    """
    stats, leaves = zip(*(one_sim(prob, height_bound)
        for _ in range(tries)))
    return Counter(stats), Counter(leaves)
