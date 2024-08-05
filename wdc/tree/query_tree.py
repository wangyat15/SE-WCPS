class QueryTree:
    """Class for saving operations under datacubes as a tree of actions
    This class uses Node class for nodes, every leaf denotes a valid datacube.
    This QueryTree is optimised for duplication, as each node might store duplicates in children.
    For example, c.merge_to(c) will not copy a tree.
    """

    def __init__(self, cube=None) -> None:
        self.root = Node(cube)

    def merge_to(self, other: 'QueryTree', action: str, params=None) -> 'QueryTree':
        """
        Merge current tree to other tree by making one new root, that refers to previous trees

        Args:
            other (QueryTree): other QueryTree
            action (str): char symbol of actions like + - * / ...
            params (dict): dictionary of parameters for a new action
        Returns:
            QueryTree: The result of a merge 
        """
        new_root = Node(action=action, params=params)
        new_root.children = [self.root, other.root]
        result = QueryTree()
        result.root = new_root
        result.root.size = self.root.size + other.root.size + 1
        return result

    def append_action(self, action: str, params=None) -> 'QueryTree':
        """
        Append new action on top of a tree

        Args:
            action (str): unary action like scale, encode, ...
            params (dict): dictionary of parameters for a new action
        Returns:
            QueryTree: The result of append
        """
        old_root = self.root
        new_root = Node(action=action, params=params)
        new_root.children = [old_root]
        result = QueryTree()
        result.root = new_root
        result.root.size = self.root.size + 1
        return result

    @classmethod
    def unite_trees(cls, trees: list, action: str, params=None) -> 'QueryTree':
        """
        Append new action on top of several trees

        Args:
            trees (list): list of trees
            action (str): unary action like scale, encode, ...
            params (dict): dictionary of parameters for a new action
        Returns:
            QueryTree: The result of append
        """
        new_root = Node(action=action, params=params)
        new_root.children = trees
        result = QueryTree()
        result.root = new_root
        result.root.size = 1
        for child in new_root.children:
            result.root.size += child.root.size
        return result
    
    @classmethod
    def recursive_string(cls, node: 'Node'):
        """
        Making a string with the help of dfs of a tree
        """
        if node.action is not None and node.action in '+-*/':
            return ('(' + cls.recursive_string(node.children[0]) + ')' + node.action + '('
                    + cls.recursive_string(node.children[1]) + ')')
        elif node.action is None:
            return node.cube.name
        else:
            return f"{node.action}"

    def __str__(self):
        return QueryTree.recursive_string(self.root)


class Node:
    """
    Class that is used to represent nodes in a QueryTree class
    """

    def __init__(self, cube=None, action: str = None, params=None) -> None:
        self.action = action
        self.cube = cube
        self.children = []
        self.params = params
        if params is not None:
            self.params = params.copy()
        self.size = 1

    def copy(self) -> 'Node':
        """
        Make a non-leaf copy of this node
        Returns:
            Node: New node with a copy of the list the children 
        """
        node = Node(self.cube, self.action, self.params)
        node.children = self.children.copy()
        node.size = self.size

        return node

    def is_leaf(self):
        return self.action is None
