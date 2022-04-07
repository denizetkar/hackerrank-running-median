class Node:
    def __init__(self, val):
        self.height = 0
        self.balance = 0
        self.val = val
        self.left = None
        self.right = None

        # Augmented with self duplicate values as well as the same for the whole subtree
        self.val_cnt = 1
        self.subtree_cnt = 0


class AVLTree:
    def __init__(self, cmp=lambda x, y: x < y):
        self.root = None
        self.cmp = cmp

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.val_cnt + self.root.subtree_cnt

    @staticmethod
    def _update(node: Node):
        left_height = -1 if node.left is None else node.left.height
        right_height = -1 if node.right is None else node.right.height
        node.height = 1 + max(left_height, right_height)
        node.balance = right_height - left_height
        # Also update the augmented fields
        left_subtree_cnt = 0 if node.left is None else node.left.val_cnt + node.left.subtree_cnt
        right_subtree_cnt = 0 if node.right is None else node.right.val_cnt + node.right.subtree_cnt
        node.subtree_cnt = left_subtree_cnt + right_subtree_cnt

    @staticmethod
    def _left_rotate(node: Node) -> Node:
        new_parent = node.right
        node.right = new_parent.left
        new_parent.left = node
        AVLTree._update(node)
        AVLTree._update(new_parent)
        return new_parent

    @staticmethod
    def _right_rotate(node: Node) -> Node:
        new_parent = node.left
        node.left = new_parent.right
        new_parent.right = node
        AVLTree._update(node)
        AVLTree._update(new_parent)
        return new_parent

    @staticmethod
    def _left_left_case(node: Node) -> Node:
        return AVLTree._right_rotate(node)

    @staticmethod
    def _left_right_case(node: Node) -> Node:
        node.left = AVLTree._left_rotate(node.left)
        return AVLTree._left_left_case(node)

    @staticmethod
    def _right_right_case(node: Node) -> Node:
        return AVLTree._left_rotate(node)

    @staticmethod
    def _right_left_case(node: Node) -> Node:
        node.right = AVLTree._right_rotate(node.right)
        return AVLTree._right_right_case(node)

    @staticmethod
    def _balance(node: Node) -> Node:
        if node.balance == -2:
            # Left heavy
            if node.left.balance <= 0:
                return AVLTree._left_left_case(node)
            else:
                return AVLTree._left_right_case(node)
        elif node.balance == 2:
            # Right heavy
            if node.right.balance >= 0:
                return AVLTree._right_right_case(node)
            else:
                return AVLTree._right_left_case(node)
        else:
            return node

    def _contains(self, node: Node, val) -> bool:
        if node is None:
            return False

        if self.cmp(val, node.val):
            return self._contains(node.left)
        if self.cmp(node.val, val):
            return self._contains(node.right)
        return True

    def __contains__(self, val) -> bool:
        return self._contains(self.root, val)

    def _add(self, node: Node, val) -> Node:
        if node is None:
            return Node(val)
        if self.cmp(val, node.val):
            node.left = self._add(node.left, val)
        elif self.cmp(node.val, val):
            node.right = self._add(node.right, val)
        else:
            node.val_cnt += 1

        AVLTree._update(node)
        return AVLTree._balance(node)

    def add(self, val):
        self.root = self._add(self.root, val)

    @staticmethod
    def _find_leftmost(node: Node) -> Node:
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _find_rightmost(node: Node) -> Node:
        while node.right is not None:
            node = node.right
        return node

    def _remove(self, node: Node, val) -> Node:
        if node is None:
            return None
        if self.cmp(val, node.val):
            node.left = self._remove(node.left, val)
        elif self.cmp(node.val, val):
            node.right = self._remove(node.right, val)
        else:
            node.val_cnt -= 1
            if node.val_cnt <= 0:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                if node.left.height > node.right.height:
                    successor = AVLTree._find_rightmost(node.left)
                    node.val = successor.val
                    node.val_cnt = successor.val_cnt
                    successor.val_cnt = 0
                    node.left = self._remove(node.left, successor.val)
                else:
                    successor = AVLTree._find_leftmost(node.right)
                    node.val = successor.val
                    node.val_cnt = successor.val_cnt
                    successor.val_cnt = 0
                    node.right = self._remove(node.right, successor.val)

        AVLTree._update(node)
        return AVLTree._balance(node)

    def remove(self, val):
        self.root = self._remove(self.root, val)

    @staticmethod
    def _kth_val(node: Node, k: int):
        if node is None:
            return None
        left_subtree_cnt = 0 if node.left is None else node.left.val_cnt + node.left.subtree_cnt

        if k < left_subtree_cnt:
            return AVLTree._kth_val(node.left, k)
        if k >= left_subtree_cnt + node.val_cnt:
            return AVLTree._kth_val(node.right, k - (left_subtree_cnt + node.val_cnt))
        return node.val

    def kth_val(self, k: int):
        if k < 0 or k >= len(self):
            return None
        return AVLTree._kth_val(self.root, k)
