import node_object


class RedBlackTree:
    # Iniate the RBTree with a black node
    def __init__(self, root):
        self.root = node_object.Node(None,
                                     None,
                                     None,
                                     'BLACK',
                                     root)

    def get_root(self):
        return self.root

    def set_root(self, root):
        self.root = root

    def delete_node(self, node):
        if node is None:
            return
        # Binary Tree method, delete a node that have 2 non-leaf children,
        # replacing it's value with rightest node value from the left subtree
        # or the leftest node value from the right subtree
        # After this replacement, the method will be call again to address the issue of deleting a node with at most
        # one non-leaf child
        if node.get_left() is not None and node.get_right() is not None:
            # in-order predecessor
            new_node = node.get_left().find_max()
            # in-order successor
            # new_node = node.get_right().find_min()
            node.set_key(new_node.get_key())
            self.delete_node(new_node)
        else:
            if node.get_right() is None:
                child = node.get_left()
            else:
                child = node.get_right()
            # Deleting root with no child
            if child is None and node.get_parent() is None:
                self.set_root(None)
            else:
                # Node is RED
                if node.get_color() == 'RED':
                    self.delete_case(node, 1)
                # Node is BLACK
                else:
                    if child is None:
                        parent = node.get_parent()
                        sibling = node.get_sibling()
                        # Delete node
                        if node == node.get_parent().get_left():
                            node.get_parent().set_left(None)
                        else:
                            node.get_parent().set_right(None)
                        node.set_parent(None)
                        # Similar to case 4 but the node is deleted first
                        if node.get_color() == 'BLACK':
                            if sibling is not None:
                                parent.set_color('BLACK')
                                sibling.set_color('RED')
                            else:
                                self.delete_case(node.get_parent(), 2)
                    else:
                        # Replace it with it's child
                        node.replace(child)
                        # If child is RED and node is BLACK,
                        # no property will be affected if the child is changed to BLACK
                        if child.get_color() == 'RED':
                            child.set_color('BLACK')
                        # Otherwise a sequency of fixes will be tried to address the 'double black' problem
                        else:
                            # If the node was the root and had a BLACK child, just replacing it solved
                            # so the opposite case is considered
                            if child.get_parent() is not None:
                                self.delete_case(child, 2)

    def delete_case(self, node, case_type):
        # Just delete the node
        if case_type == 1:
            if node.get_right() is None:
                child = node.get_left()
            else:
                child = node.get_right()
            # Has no child
            if child is None:
                if node == node.get_parent().get_left():
                    node.get_parent().set_left(None)
                else:
                    node.get_parent().set_right(None)
            else:
                # If it have a child and it's RED, the child will be BLACK,
                # so replacing it won't change any property
                node.replace(child)
        # If parent is BLACK and sibling is RED, rotate and paint
        elif case_type == 2:
            if node.get_parent().get_color() == 'BLACK' and \
                    node.get_sibling().get_color() == 'RED':
                if node == node.get_parent().get_left():
                    self.rotate_left(node.get_parent())
                else:
                    self.rotate_right(node.get_parent())
                node.get_parent().set_color('RED')
                node.get_sibling().set_color('BLACK')
            self.delete_case(node, 3)
        elif case_type == 3:
            sibling = node.get_sibling()
            if sibling.get_left() is not None and sibling.get_right() is not None:
                if node.get_parent().get_color() == 'BLACK' and sibling.get_color() == 'BLACK' \
                        and sibling.get_left().get_color() == 'BLACK' and sibling.get_right().get_color() == 'BLACK':
                    sibling.set_color('RED')
                    self.delete_case(node.get_parent(), 1)
                else:
                    self.delete_case(node, 4)
        elif case_type == 4:
            sibling = node.get_sibling()
            if node.get_parent().get_color() == 'RED' and sibling.get_color() == 'BLACK' \
                    and sibling.get_left().get_color() == 'BLACK' and sibling.get_right().get_color() == 'BLACK':
                sibling.set_color('RED')
                node.get_parent().set_color('BLACK')
            else:
                self.delete_case(node, 5)
        elif case_type == 5:
            sibling = node.get_sibling()
            if node == node.get_parent().get_left():
                sibling.get_left().set_color('BLACK')
                self.rotate_right(sibling)
            else:
                sibling.get_right().set_color('BLACK')
                self.rotate_left(sibling)
            self.delete_case(node, 6)
        elif case_type == 6:
            sibling = node.get_sibling()
            sibling.set_color(node.get_parent().get_color())
            node.get_parent().set_color('BLACK')
            if node == node.get_parent().get_left():
                sibling.get_right().set_color('BLACK')
                self.rotate_left(node.get_parent())
            else:
                sibling.get_left().set_color('BLACK')
                self.rotate_right(node.get_parent())

    def export(self):
        root = self.get_root()
        if root is not None:
            nodes = [self.get_root()]
            self.generate_nodes_list(nodes, 0)
        else:
            nodes = []

        edges = []
        for node in nodes:
            parent = node.get_key()
            left = node.get_left()
            if left is None:
                left = -1
            else:
                left = left.get_key()
            edges += [[parent, left]]
            right = node.get_right()
            if right is None:
                right = -1
            else:
                right = right.get_key()
            edges += [[parent, right]]

        return nodes, edges

    def generate_nodes_list(self, nodes, index):
        if nodes[index].get_key() >= 0:
            left = nodes[index].get_left()
            if left is not None:
                nodes += [left]
            right = nodes[index].get_right()
            if right is not None:
                nodes += [right]
            if index < len(nodes) - 1:
                self.generate_nodes_list(nodes, index + 1)

    def insert_node(self, key):
        if key >= 0 and self.search(key) is None:
            node = node_object.Node(None, None, None, 'RED', key)
            self.insert_recursive(self.get_root(), node)
            self.insert_repair(node)

    # Insert the new node according to the binary tree rule
    def insert_recursive(self, root, node):
        if root is None:
            self.set_root(node)
            return
        if node.get_key() < root.get_key():
            if root.get_left() is not None:
                self.insert_recursive(root.get_left(), node)
                return
            else:
                root.set_left(node)
        else:
            if root.get_right() is not None:
                self.insert_recursive(root.get_right(), node)
                return
            else:
                root.set_right(node)

        node.set_parent(root)

    # Check which case is appropriate to solve a possible break of the RBTree's rules
    def insert_repair(self, node):
        if node.get_parent() is not None and node.get_uncle() is not None:
            if node.get_parent().get_color() == 'BLACK':
                return
            elif node.get_uncle().get_color() == 'RED':
                self.insert_case(node, 1)
                return
        self.insert_case(node, 2)
        self.root.set_color('BLACK')

    def insert_case(self, node, case_type):
        # Change descendants colors
        if case_type == 1:
            node.get_parent().set_color('BLACK')
            node.get_uncle().set_color('BLACK')
            node.get_grand_parent().set_color('RED')
            self.insert_repair(node.get_grand_parent())
        # Rotate to re-organize the color from the actual parent and uncle, which are opposite
        elif case_type == 2:
            parent = node.get_parent()
            grand_parent = node.get_grand_parent()

            if parent is None or grand_parent is None:
                return

            if node == parent.get_right() and parent == grand_parent.get_left():
                self.rotate_left(parent)
                node = node.get_left()
            elif node == parent.get_left() and parent == grand_parent.get_right():
                self.rotate_right(parent)
                node = node.get_right()

            self.insert_case(node, 3)
        # Rotate again, to finally change the new node to it's grand parent position,
        # and change colors to address the previous issue
        elif case_type == 3:
            parent = node.get_parent()
            grand_parent = node.get_grand_parent()

            if node == parent.get_left():
                self.rotate_right(grand_parent)
            else:
                self.rotate_left(grand_parent)

            parent.set_color('BLACK')
            grand_parent.set_color('RED')

    def rotate_left(self, node):
        new_root = node.get_right()
        if new_root is None:
            return
        temp = new_root.get_left()
        new_root.set_left(node)
        node.set_right(temp)
        parent = node.get_parent()
        if parent is None:
            self.set_root(new_root)
            new_root.set_parent(None)
        else:
            new_root.set_parent(parent)
            if parent.get_left() == node:
                parent.set_left(new_root)
            else:
                parent.set_right(new_root)
        node.set_parent(new_root)

    def rotate_right(self, node):
        new_root = node.get_left()
        if new_root is None:
            return
        temp = new_root.get_right()
        new_root.set_right(node)
        node.set_left(temp)
        parent = node.get_parent()
        if parent is None:
            self.set_root(new_root)
            new_root.set_parent(None)
        else:
            new_root.set_parent(parent)
            if parent.get_left() == node:
                parent.set_left(new_root)
            else:
                parent.set_right(new_root)
        node.set_parent(new_root)

    def search(self, key):
        node = self.get_root()
        if node is None:
            return None
        while key != node.get_key():
            if key < node.get_key():
                node = node.get_left()
            else:
                node = node.get_right()
            if node is None:
                return None
        return node
