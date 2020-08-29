'''
Ryan Balog
CS2420
Project 5
'''

from recursioncounter import RecursionCounter


class Node:
    '''Object that holds data and the nex left/right nodes'''

    def __init__(self, data, left_child=None, right_child=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.height = 0

    def is_leaf(self):
        '''checks if node is a leaf'''
        return self.left_child is None and self.right_child is None

    def update_height(self):
        '''update node height'''
        if self.is_leaf():
            return 0
        elif self.left_child is not None and self.right_child is None:
            return self.left_child.height + 1
        elif self.right_child is not None and self.left_child is None:
            return self.right_child.height + 1
        elif self.right_child is not None and self.left_child is not None:
            if self.right_child.height > self.left_child.height:
                return self.right_child.height + 1
            else:
                return self.left_child.height + 1

    def __str__(self):
        '''returns node data and node height'''
        return f"{self.data} ({self.height})"


class BinarySearchTree:
    '''Hold node objects'''

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def add(self, data):
        '''add an item to the tree'''
        self.root = self.add_helper(self.root, data)
        return None

    def add_helper(self, cursor, data):
        '''helps the add function'''
        RecursionCounter()
        if cursor is None:
            return Node(data)
        if data == cursor.data:
            return None
        if data > cursor.data:
            cursor.right_child = self.add_helper(cursor.right_child, data)
            cursor.height = cursor.update_height()
        
        else:
            cursor.left_child = self.add_helper(cursor.left_child, data)
            cursor.height = cursor.update_height()
        return cursor

    def find(self, data):
        '''searches for node.data in tree'''
        if self.root is None:
            return None
        elif data == self.root.data:
            return self.root

        return self.find_helper(self.root, data)

    def find_helper(self, cursor, data):
        RecursionCounter()

        if data == cursor.data:
            return cursor
        elif data < cursor.data:
            if cursor.left_child is None:
                return None
            else:
                return self.find_helper(cursor.left_child, data)
        else:
            if cursor.right_child is None:
                return None
            else:
                return self.find_helper(cursor.right_child, data)

    def remove(self, data):
        '''removes node from tree'''
        self.root = self.remove_helper(self.root, data)

    def remove_helper(self, cursor, data):
        RecursionCounter()

        if cursor == None:
            return None
        elif cursor.data == data:
            if cursor.is_leaf():
                return None
            if cursor.right_child is None and cursor.left_child is not None:
                cursor.height -= cursor.update_height()
                return cursor.left_child
            if cursor.left_child is None and cursor.right_child is not None:
                cursor.height -= cursor.update_height()
                return cursor.right_child
            if cursor.left_child is not None and cursor.right_child is not None:
                temp = cursor.right_child
                while temp.left_child is not None:
                    temp = temp.left_child
                cursor.data = temp.data
                cursor.right_child.height -= cursor.right_child.update_height()
                cursor.right_child = self.remove_helper(
                    cursor.right_child, temp.data)
        elif data > cursor.data:
            cursor.right_child = self.remove_helper(cursor.right_child, data)
        elif data < cursor.data:
            cursor.left_child = self.remove_helper(cursor.left_child, data)
        cursor.height = cursor.update_height()
        return cursor

    def preorder(self):
        output = []
        if self.root is None:
            return output

        return self.preorder_helper(self.root, output)

    def preorder_helper(self, cursor, output):
        RecursionCounter()
        output.append(cursor.data)

        if cursor.left_child is not None:
            self.preorder_helper(cursor.left_child, output)
        if cursor.right_child is not None:
            self.preorder_helper(cursor.right_child, output)
        return output

    def height(self):
        if self.root is None:
            return -1
        return self.root.height

    def __str__(self):
        return self.print_helper(self.root, 0)

    def print_helper(self, cursor, offset):
        RecursionCounter()

        whitespace = offset * "  "
        new = offset + 2
        output = whitespace + str(cursor)

        if cursor.is_leaf():
            print(output + "[leaf]")
        elif cursor.left_child is None:
            print(output)
            print((new * "  ") + "[Empty]")

        else:
            print(output)

        if cursor.left_child is not None:
            self.print_helper(cursor.left_child, new)
            if cursor.right_child is None:
                print((new * "  ") + "[Empty]")
        if cursor.right_child is not None:
            self.print_helper(cursor.right_child, new)

        return "\n"

    def __len__(self):
        self.length = 0
        if self.root is None:
            return self.length

        return self.length_helper(self.root)

    def length_helper(self, cursor):
        RecursionCounter()

        if cursor.left_child is not None:
            self.length_helper(cursor.left_child)
        if cursor.right_child is not None:
            self.length_helper(cursor.right_child)

        self.length += 1
        return self.length

    def inorder(self):
        '''outputs a list of the binary tree in sequential order'''
        new_order = []
        if self.root is None:
            return new_order

        return self.inorder_helper(self.root, new_order)

    def inorder_helper(self, cursor, new_order):
        '''helps with recursion to perform inorder traversal'''
        RecursionCounter()


        if cursor.left_child is not None:
            self.inorder_helper(cursor.left_child, new_order)
        new_order.append(cursor.data)
        if cursor.right_child is not None:
            self.inorder_helper(cursor.right_child, new_order)
        return new_order

    def rebalance_tree(self):
        lyst = self.inorder()

        mid = (0 + len(lyst)) // 2
        new = BinarySearchTree()
        new.add(lyst[mid])
        self.rebalance_tree_helper(lyst[0:mid], new)
        self.rebalance_tree_helper(lyst[mid+1:], new)
        self.root = new.root

        return


    def rebalance_tree_helper(self, new_lyst, new):
        RecursionCounter()

        if len(new_lyst) is not 0:
            if len(new_lyst) <= 1:
                mid = 0
            else:
                mid = (0 + len(new_lyst)) // 2
            new.add(new_lyst[mid])
            if len(new_lyst) > 1:
                self.rebalance_tree_helper(new_lyst[0:mid], new)
                self.rebalance_tree_helper(new_lyst[mid+1:], new)
        return new

