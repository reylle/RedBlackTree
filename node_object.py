class Node:
    def __init__(self, parent, left, right, color, key):
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color
        self.key = key

    def get_parent(self):
        return self.parent

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_color(self):
        return self.color

    def get_key(self):
        return self.key

    def set_parent(self, parent):
        self.parent = parent

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_color(self, color):
        self.color = color

    def set_key(self, key):
        self.key = key

    # Find the node with the maximum key of this node
    def find_max(self):
        node = self
        while node.get_right() is not None:
            node = node.get_right()
        return node

    # Find the node with the minimum key of this node
    def find_min(self):
        node = self
        while node.get_left() is not None:
            node = node.get_left()
        return node

    def get_grand_parent(self):
        parent = self.get_parent()

        if parent is None:
            return None
        return parent.get_parent()

    def get_sibling(self):
        parent = self.get_parent()

        if parent is None:
            return None

        if self == parent.get_left():
            return parent.get_right()
        else:
            return parent.get_left()

    def get_uncle(self):
        parent = self.get_parent()
        grand_parent = self.get_grand_parent()

        if grand_parent is None:
            return None
        return parent.get_sibling()

    def replace(self, node):
        if self.get_parent() is None:
            self.set_key(node.get_key())
            self.set_left(node.get_left())
            self.set_right(node.get_right())
            self.set_color(node.get_color())
        else:
            if node is not None:
                node.set_parent(self.get_parent())
            if self == self.get_parent().get_left():
                self.get_parent().set_left(node)
            else:
                self.get_parent().set_right(node)
            self.set_parent(None)
            self.set_right(None)
            self.set_left(None)
