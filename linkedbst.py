"""
File: linkedbst.py
Author: Ken Lambert
"""


from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from time import time
import random



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def Tree(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            inner = top.left
            while not inner.right == None:
                parent = inner
                inner = inner.right
            top.data = inner.data
            if parent == top:
                top.left = inner.left
            else:
                parent.right = inner.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        removed = None
        root = BSTNode(None)
        root.left = self._root
        parent = root
        direction = 'L'
        inner = self._root
        while not inner == None:
            if inner.data == item:
                removed = inner.data
                break
            parent = inner
            if inner.data > item:
                direction = 'L'
                inner = inner.left
            else:
                direction = 'R'
                inner = inner.right

        # Return None if the item is absent
        if removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not inner.left == None \
                and not inner.right == None:
            Tree(inner)
        else:

            # Case 2: The node has no left child
            if inner.left == None:
                child = inner.right

                # Case 3: The node has no right child
            else:
                child = inner.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = child
            else:
                parent.right = child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = root.left
        return removed

    def replace(self, item, child):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                data = probe.data
                probe.data = child
                return data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        This is height method
        """
        def height1(iteration):
            if iteration is None:
                return 0
            else:
                return 1 + max(height1(iteration.left), height1(iteration.right))

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def height_search(node):
            """_summary_

            Args:
                node (_type_): _description_
            """
            if node is None:
                return 0
            return 1 + max(height_search(node.left), height_search(node.right))
        return height_search(self._root) <= 2 * log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        def find_range(node, low, height, arrays):
            if node is None:
                return None
            if low <= node.data <= height:
                find_range(node.left, low, height, arrays)
                arrays.append(node.data)
                find_range(node.right, low, height, arrays)
            elif node.data < low:
                find_range(node.right, low, height, arrays)
            else:
                find_range(node.left, low, height, arrays)
        arr = []
        find_range(self._root, low, high, arr)
        return arr

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_balanced_tree(items):
            if not items:
                return None
            middle = len(items) // 2
            root = BSTNode(items[middle])
            root.left = build_balanced_tree(items[:middle])
            root.right = build_balanced_tree(items[(middle + 1):])
            return root

        items = list(self)
        self._root = build_balanced_tree(items)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def successor_find(node, item, inner):
            """_summary_
            Args:
                node (_type_): _description_
                item (_type_): _description_
                inner (_type_): _description_
            """
            if node is None:
                return inner
            if node.data > item:
                inner = node.data
                return successor_find(node.left, item, inner)
            else:
                return successor_find(node.right, item, inner)
        return successor_find(self._root, item, None)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def predecessor_find(node, item, inner):
            """_summary_
            Args:
                node (_type_): _description_
                item (_type_): _description_
                predecessor (_type_): _description_
            """
            if node is None:
                return inner
            if node.data < item:
                inner = node.data
                return predecessor_find(node.right, item, inner)
            elif node.data >= item:
                return predecessor_find(node.left, item, inner)
        return predecessor_find(self._root, item, None)


    def demo_bst(self, filepath):
        """
        This is demo_bst method
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            arr = [word.strip() for word in f]
        start = time()
        print("Case 1")
        for _ in range(10000):
            iter = random.choice(arr)
        end = time()
        print(f"This case working {round(end - start, 4)} sec")

        print("\n\nCase 2")
        start = time()
        for _ in range(10000):
            iter = random.choice(arr)
        end = time()
        print(f"This case working {round(end - start, 4)} sec")

        print("\n\nCase 3")
        random.shuffle(arr)
        start = time()
        for _ in range(10000):
            word = random.choice(arr)
        end = time()
        print(f"This case working {round(end - start, 4)} sec")

        print("\n\nCase 4")
        self.rebalance()
        start = time()
        for _ in range(10000):
            word = random.choice(arr)
        end = time()
        print(f"This case working {round(end - start, 4)} sec")


if __name__ == '__main__':
    result = LinkedBST()
    print(result.demo_bst('words.txt'))
