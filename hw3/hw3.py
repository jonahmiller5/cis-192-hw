'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 5
'''

'''
In all functions below, the keyword "pass" is used to 
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''


class Node:
    def __init__(self, key):
        '''
        Construct an instance of the Node class
        args: 
            key: the key for the node
        '''
        self.key = key

        self.parent = None
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        '''
        Construct an instance of the BST class
        args: None
        Note: the BST should be initially empty
        '''
        self.size = 0
        self.root = None
        self.next = None


    def isempty(self):
        '''
        Whether the tree is empty
        args: None
        ret: 
            True if the tree is empty, False otherwise
        '''
        return self.size == 0


    def add(self, key):
        '''
        Add a node to the BST with a given key
        args:
            key: the key to insert in the dictionary
        ret: None

        Notes: if the key is already in the BST, you
        must silently ignore it (i.e., without raising
        an exception). If you are interested, you may 
        want to look into issuing a warning.
        '''
        if isinstance(key, int):
            if self.root is None:
                self.root = Node(key)
                self.size = 1
            else:
                b = self.add_rec(self.root, key)
                if b:
                    self.size = self.size + 1


    def add_rec(self, root, key):
        if root is None or not isinstance(key, int):
            return False

        if root.key == key:
            return False

        if key < root.key:
            if root.left is None:
                n = Node(key)
                root.left = n
                n.parent = root
                return True

            return self.add_rec(root.left, key)

        if key > root.key:
            if root.right is None:
                n = Node(key)
                root.right = n
                n.parent = root
                return True

            return self.add_rec(root.right, key)


    def delete(self, key):
        '''
        Remove the node with a matching key from the BST
        args:
            key: the key to delete
        ret: None

        Notes: if the key is not present in the BST, you 
        must raise a ValueError exception with a descriptive
        message.
        '''

        if not self.size or not isinstance(key, int):
            raise ValueError('Key to be deleted does not exist in BST')

        removal = self.find_node(self.root, key)

        if removal is None:
            raise ValueError('Key to be deleted does not exist in BST')

        self.size = self.size - 1

        p = removal.parent

        if removal.left is not None and removal.right is not None:
            trailing = self.delete_rec(removal)

            p = trailing.parent

            trailing.parent = None
            if p.left == trailing:
                p.left = None
            else:
                p.right = None

        elif removal.left is not None:
            if removal == self.root:
                self.root = removal.left
                self.root.parent = None
                removal.left = None

            else:
                removal.left.parent = p

                if p.right == removal:
                    p.right = removal.left

                else:
                    p.left = removal.left

                removal.parent = None
                removal.left = None


        elif removal.right is not None:
            if removal == self.root:
                self.root = removal.right
                self.root.parent = None
                removal.right = None

            else:
                removal.right.parent = p

                if p.right == removal:
                    p.right = removal.right
                else:
                    p.left = removal.right

                removal.parent = None
                removal.right = None

        else:
            if removal == self.root:
                self.root = None
                removal.left = None
                removal.right = None

            else:
                if p.left == removal:
                    p.left = None
                else:
                    p.right = None

    
    def delete_rec(self, deletion):
        successor = self.find_successor(deletion)

        if deletion is None:
            return deletion

        if successor is None:
            return deletion

        deletion.key = successor.key

        return self.delete_rec(successor)


    def find_node(self, root, key):
        if root is None or not isinstance(key, int):
            return None

        if key == root.key:
            return root

        if key < root.key:
            return self.find_node(root.left, key)

        if key > root.key:
            return self.find_node(root.right, key)


    def find_successor(self, curr):
        if not isinstance(curr, Node):
            return curr

        prekey = curr.key

        if curr.right is not None:
            curr = curr.right
            curr = self.subtree_min(curr)
        elif curr.parent is not None:
            while curr.key > curr.parent.key:
                curr = curr.parent
                if curr.parent is None:
                    break
            curr = curr.parent

        if curr is None or curr.key == prekey:
            return None

        return curr


    def subtree_min(self, root):
        if root is None:
            raise ValueError('Illegal Argument for subtree_min')

        prekey = root.key

        while root.left is not None:
            root = root.left

        return root


    def __iter__(self):
        '''
        Return an iterator for in-order traversal of the BST keys
        args: None
        ret:
            The iterator

        Note: Since the BST will be an iterator itself, you
        should return self. However, make sure to also initialize
        the appropriate structures.
        '''
        curr = self.root

        if curr is not None:
            while curr.left is not None:
                curr = curr.left
            
        self.next = curr

        return self


    def __next__(self):
        '''
        Implement the next() functionality of the iterator
        args: None
        ret:
            The next value of the iterator

        Note: this should work in conjunction with __iter__
        to appropriately manage the state. Don't forget
        to raise the appropriate exception when iteration
        over the tree terminates.
        '''
        result = self.next
        if result is None:
            raise StopIteration('Reached end of tree')

        self.next = self.find_successor(result)

        return result.key


    def __contains__(self, key):
        '''
        Whether the given key is in the BST
        args:
            key: the key to search for
        ret:
            True if the key is in the BST, false otherwise
        '''
        return self.find_node(self.root, key) is not None


    def __len__(self):
        '''
        The number of elements in the BST
        args: None
        ret: 
            The number of elements in the BST

        Note: you should avoid traversing the BST in this function
        '''
        return self.size


def main():
    '''
    Use this for testing! Make sure to be thorough and test for 
    corner cases. There are many corner cases to look out for
    when working with trees!
    '''
    my_tree = BST()
    my_tree.add(None)
    my_tree.add(5)
    my_tree.add(10)
    my_tree.add(1)
    my_tree.add(2)
    my_tree.add(0)
    my_tree.add(7)
    my_tree.add(11)
    my_tree.add(25)
    my_tree.add(8)
    my_tree.add(6)
    my_tree.add(-1)
    my_tree.add(3)
    print('Size Before:', len(my_tree))
    # print(5 in my_tree)
    # my_tree.delete(None)
    # print('Size After:', len(my_tree))
    # print(my_tree.root.key)
    # print(my_tree.root.right.key)
    # print(my_tree.root.left.key)
    # print(my_tree.root.left.left.key)
    # print(my_tree.root.left.right.key)
    # print(my_tree.root.right.left)
    # print(my_tree.root.right.right.key)
    
    # print(5 in my_tree)
    s = my_tree.root.left.left.left
    # while s is not None:
    #     print(s.key)
    #     s = my_tree.find_successor(s)
    # print(list(my_tree))
    for elem in my_tree:
        # assert elem in my_tree
        print(elem)
    

if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw3.py
    '''
    main()


