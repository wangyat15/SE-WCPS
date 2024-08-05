from enum import Enum


class Action(str, Enum):
    """Class that represents the actions with datacubes
    """
    # these actions were seen in the Jupyter notebook examples
    ADD = '+'
    SUB = '-'
    MULT = '*'
    DIV = '/'
    ENCODE = 'encode'
    AVG = 'avg'
    MIN = 'min'
    MAX = 'max'
    REFACTOR = 'refactor'
    SUBINDEX = 'subindex'
    
    def __str__(self):
        return self.value
