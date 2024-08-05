from numbers import Number

from wdc.coverage.args_formatter import Formatting
from wdc.helpers.subset import Subset
from .tree.query_tree import QueryTree
from .action import Action
from .connection.requester import ClientRequest
from .tree.tree_parser import make_process_query_from_tree
from typing import List

class Datacube:
    """
    Datacube python object based on rasdaman datacubes
    Uses tree-like data structure to store operations like +, avg, ...
    """
    counter = 0  # Class attribute to enumerate new datacubes

    def __init__(self, link='https://ows.rasdaman.org/rasdaman/ows',
                 index:List[Subset]=None, coverage_name="S2_L2A_32631_TCI_60m") -> None:
        
        if index == None:
            self.index = index
        else:
            self.index = Formatting.subsets_format(index)
            

        self.__tree = QueryTree(self)
        self.coverage_name = coverage_name
        self.requester = ClientRequest()
        self.name = f'c{Datacube.counter}'
        Datacube.counter += 1
        self.link = link

    def get_tree(self) -> QueryTree:
        """
        Getter of tree of a Datacube representing the datacube's operation tree
        Args:
            Nil 
        Returns:
            QueryTree: 
        """
        return self.__tree

    def set_tree(self, tree: QueryTree):
        """
        Setter of tree of a Daracube

        Args:
            tree (QueryTree): incoming tree
        Returns:
            Nil 
        """
        self.__tree = tree

    @classmethod
    def __from_tree(cls, tree: QueryTree):
        cube = Datacube()
        cube.set_tree(tree)
        return cube

    @classmethod
    def cast_to_datacube(cls, other):
        """
        Method that converts an object to a datacube. Used to support operations with constants
        """
        datacube = Datacube()
        datacube.name = str(other)
        return datacube

    def __add__(self, other) -> 'Datacube':
        """
        Method for addition operation on datacubes

        Args:
            other: Another datacube object to perform addition operation
        Returns:
            datacube
        """
        if isinstance(other, Number):
            other = Datacube.cast_to_datacube(other)
        elif not isinstance(other, Datacube):
            raise ValueError("Adding a Datacube to an unsupported type")
        new_tree = self.__tree.merge_to(other.get_tree(), action=Action.ADD)
        return Datacube.__from_tree(new_tree)

    def __sub__(self, other) -> 'Datacube':
        """
        Method for substraction operation on datacubes

        Args:
            other: Another datacube object to perform substraction operation
        Returns:
            datacube
        """
        if isinstance(other, Number):
            other = Datacube.cast_to_datacube(other)
        elif not isinstance(other, Datacube):
            raise ValueError("Substituting a Datacube an to unsupported type")
        new_tree = self.__tree.merge_to(other.get_tree(), action=Action.SUB)
        return Datacube.__from_tree(new_tree)

    def __mul__(self, other) -> 'Datacube':
        """
        Method for multiplication operation on datacubes

        Args:
            other: Another datacube object to perform multiplication operation
        Returns:
            datacube
        """
        if isinstance(other, Number):
            other = Datacube.cast_to_datacube(other)
        elif not isinstance(other, Datacube):
            raise ValueError("Multiplying a Datacube an to unsupported type")
        new_tree = self.__tree.merge_to(other.get_tree(), action=Action.MULT)
        return Datacube.__from_tree(new_tree)

    def __truediv__(self, other) -> 'Datacube':
        """
        Method for division operation on datacubes

        Args:
            other: Another datacube object to perform division operation
        Returns:
            datacube
        """
        if isinstance(other, Number):
            other = Datacube.cast_to_datacube(other)
        elif not isinstance(other, Datacube):
            raise ValueError("Dividing a Datacube to an unsupported type")
        new_tree = self.__tree.merge_to(other.get_tree(), action=Action.DIV)
        return Datacube.__from_tree(new_tree)

    def avg(self, index: str) -> 'Datacube':
        """
        Return a datacube that has aggregate query as the last operation

        Args:
            index (str, optional): index for aggregate query. Defaults to empty List.
        Returns:
            _type_: datacube
        """
        if index == "":
            return Datacube.__from_tree(self.__tree.append_action(action=Action.AVG))
        new_tree = self.__tree.append_action(action=Action.AVG,
            params={"slice": index})
        return Datacube.__from_tree(new_tree)

    def min(self, index: List[Subset] = []) -> 'Datacube':
        """
        Return a datacube that has aggregate query as the last operation

        Args:
            index (str, optional): index for aggregate query. Defaults to empty List.
        Returns:
            _type_: datacube
        """
        if index == []:
            return Datacube.__from_tree(self.__tree.append_action(action=Action.MIN))
        new_tree = self.__tree.append_action(action=Action.MIN,
            params={"slice": Formatting.subsets_format(index)})
        return self.__from_tree(new_tree)

    def max(self, index: List[Subset] = []) -> 'Datacube':
        """
        Return a datacube that has aggregate query as the last operation

        Args:
            index (str, optional): index for aggregate query. Defaults to empty List.
        Returns:
            _type_: datacube
        """
        if index == []:
            return Datacube.__from_tree(self.__tree.append_action(action=Action.MAX))
        new_tree = self.__tree.append_action(action=Action.MAX,
            params={"slice": Formatting.subsets_format(index)})
        return self.__from_tree(new_tree)

    def encode(self, encode_format: str) -> 'Datacube':
        """
        Encode the final result to the desired format

        Args:
            encode_format (str): encode format (img/png, text/csv, ...)
        Returns:
            Datacube: the datacube after applying encode
        """
        new_tree = self.__tree.append_action(action=Action.ENCODE,
                                             params={"encode format": encode_format})
        return self.__from_tree(new_tree)

    def __getitem__(self, index: List[Subset]) -> 'Datacube':
        """
        Subindex operation, datacube['a(p1), b(p2:p3), c(p4:p5)']

        Args:
            index (str): the string that defines subindex
        """
        index = Formatting.subsets_format(index)

        new_tree = self.__tree.append_action(action=Action.SUBINDEX,
                                             params={"index": index})
        return Datacube.__from_tree(new_tree)

    @classmethod
    def refactor(cls, axes):
        """
        Create new datacube with specified indices

        Args:
            axes (list): list of pairs (str, Datacube) name of a new axis and datacube for an axis
        """
        params = []
        trees = []
        for el in axes:
            params.append((el[0], el[1].name))
            trees.append(el[1].get_tree())
        return Datacube.__from_tree(QueryTree.unite_trees(trees,
                                                          action=Action.REFACTOR, params=params))


    def fetch(self):
        """
        Fetching and loading data from a server according to the qurrent request 

        Returns:
            data: the context of a request
        """
        return self.requester.evaluate_query(make_process_query_from_tree(self.get_tree()))
    
