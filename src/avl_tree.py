"""AVL tree used for patient records (key = Patient ID).

An AVL tree is a BST that keeps itself balanced: for every node, the heights
of the left and right subtrees differ by at most 1. Because of this the height
stays O(log n), so search / insert take O(log n) even if IDs arrive in sorted order.
"""


class AVLNode:
    def __init__(self, key, data):
        self.key = key        # e.g. Patient ID
        self.data = data      # the record stored for that ID
        self.left = None
        self.right = None
        self.height = 1       # a single node has height 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.rotations = 0    # counted only so the demo can show balancing

    # ---------- helpers ----------
    def _height(self, node):
        return node.height if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        # > 1 means left-heavy, < -1 means right-heavy
        return self._height(node.left) - self._height(node.right)

    # ---------- rotations ----------
    def _rotate_right(self, y):
        #       y            x
        #      / \          / \
        #     x   C   ->   A   y
        #    / \              / \
        #   A   B            B   C
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        self.rotations += 1
        return x

    def _rotate_left(self, x):
        #     x                y
        #    / \              / \
        #   A   y     ->     x   C
        #      / \          / \
        #     B   C        A   B
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        self.rotations += 1
        return y

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:                                   # left-heavy
            if self._balance_factor(node.left) < 0:       # left-right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)               # left-left case

        if balance < -1:                                  # right-heavy
            if self._balance_factor(node.right) > 0:      # right-left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)                # right-right case

        return node

    # ---------- insert ----------
    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            self.size += 1
            return AVLNode(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data          # same ID again: update the record
            return node
        return self._rebalance(node)  # fix balance on the way back up

    # ---------- search ----------
    def search(self, key):
        """Return the record for key, or None if it is not present."""
        node = self.root
        while node:
            if key == node.key:
                return node.data
            node = node.left if key < node.key else node.right
        return None

    # ---------- traversal ----------
    def inorder(self):
        """Left, node, right: gives (key, data) pairs in sorted key order."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.data))
            self._inorder(node.right, result)

    def height(self):
        return self._height(self.root)
