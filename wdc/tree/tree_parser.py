from .query_tree import Node
from .query_tree import QueryTree
from ..action import Action


def iterate_tree(node: 'Node', datacubes: set, encodes: set, indexes: set, execution_lines: list, num=0):
    """
    Recursive process of going through a tree

    Args:
        node (Node): current node
        datacubes (set): the set of pairs of datacubes' names and their coverage names 
        encodes (set): set of encodes to check only one encoding
        indexes (dict): dictionary of (name, index) for every datacube
        execution_lines (list): lines to execute that will be formed by this function
        num (int): index variable
        
    Raises:
        AttributeError: The error of the wrong order of queries
    """
    if node.action is None:
        cube = node.cube
        # Digits case
        if str.isnumeric(cube.name) or (cube.name.count('.') == 1
                                        and cube.name.replace('.', '', 1).isnumeric()):
            execution_lines.append(f"$f{num} := {cube.name}")
            return
        datacubes.add((cube.name, cube.coverage_name))
        if not cube.index is None:
            indexes[cube.name] = cube.index
            execution_lines.append(f'$f{num} := ${cube.name}[ $index{cube.name}]')
        else:
            execution_lines.append(f'$f{num} := ${cube.name}')
    # Binary operator
    elif node.action in [Action.ADD, Action.SUB, Action.MULT, Action.DIV]:
        left_size = node.children[0].size
        execution_lines.append(f'$f{num} := ' + '(' + f'$f{num + 1}' + ')' + node.action +
                               '(' + f'$f{num + left_size + 1}' + ')')
        iterate_tree(node.children[0],
                     datacubes, encodes, indexes, execution_lines, num + 1)
        iterate_tree(node.children[1],
                     datacubes, encodes, indexes, execution_lines, num + left_size + 1)
    # Aggregate queries
    elif node.action in [Action.MAX, Action.MIN, Action.AVG]:
        index = ""
        if not (node.params is None) and 'slice' in node.params:
            index = f"[{node.params['slice']}]"
        execution_lines.append(f'$f{num} := {str(node.action)}(($f{num+1}){index})')
        iterate_tree(node.children[0], datacubes, encodes, indexes, execution_lines, num + 1)
        return
    # Refactor query
    elif node.action is Action.REFACTOR:
        line = f'$f{num} := ' + '{ '
        prefix = 0
        order = []
        len_params = len(node.params)
        for i in range(len_params):
            el = node.params[i]
            line += el[0] + ": "
            line += f"$f{num + 1 + prefix}"
            if i != len_params - 1:
                line += '; '
            order.append((node.children[i].root, prefix + 1 + num))
            prefix += node.children[i].root.size
        line += ' }'
        execution_lines.append(line)
        for el in order:
            iterate_tree(el[0], datacubes, encodes, indexes, execution_lines, el[1])
    elif node.action is Action.SUBINDEX:
        indexes[f"f{num}"] = node.params['index']
        execution_lines.append(f'$f{num} := $f{num + 1}[ $indexf{num}]')
        iterate_tree(node.children[0], datacubes, encodes, indexes, execution_lines, num + 1)
    # Encode
    elif node.action == Action.ENCODE:
        encodes.add(node.params['encode format'])
        iterate_tree(node.children[0], datacubes, encodes, indexes, execution_lines, num)
    else:
        raise AttributeError("This action is not implemented yet")


def make_process_query_from_tree(tree: 'QueryTree') -> str:
    """
    Creates query string according to syntax of rasdaman 

    Args:
        tree (QueryTree): a tree to be processed

    Raises:
        AttributeError: Error of placement of arguments

    Returns:
        str: query output
    """
    datacubes = set()
    encodes = set()
    indexes = {}
    execution_lines = []
    iterate_tree(tree.root, datacubes, encodes, indexes, execution_lines)
    query = ""
    if len(encodes) > 1:
        raise AttributeError("Multiple encodes are not supported")
    if len(encodes) == 1 and tree.root.action != Action.ENCODE:
        raise AttributeError("The encode should be the last operation")
    i = 0
    datacubes = sorted(list(datacubes))
    #For part
    for el in datacubes:
        i += 1
        if len(query) == 0:
            query += 'for '
        else:
            query += '    '
        query += f'${el[0]} in ({el[1]})'
        if i != len(datacubes):
            query += ','
        query += '\n'
    first_index = True
    i = 0
    #Index part
    for el in datacubes:
        if el[0] not in indexes:
            continue
        i += 1
        if first_index:
            query += f'    let $index{el[0]} := [{indexes[el[0]]}]'
        else:
            query += f'        $index{el[0]} := [{indexes[el[0]]}]'
        if i != len(datacubes) or len(execution_lines) > 0:
            query += ','
        query += '\n'
        first_index = False
        indexes.pop(el[0])
    i = 0
    len_indexes = len(list(indexes))
    for el in sorted(list(indexes)):
        
        i += 1
        if first_index:
            query += f'    let $index{el} := [{indexes[el]}]'
        else:
            query += f'        $index{el} := [{indexes[el]}]'
        if i != len_indexes or len(execution_lines) > 0:
            query += ','
        query += '\n'
        first_index = False
    #Execution part
    execution_lines = execution_lines[::-1]
    for i in range(len(execution_lines)):
        line = execution_lines[i]
        if first_index: 
            query += "     let " + line
        else:
            query += "        " + line
        first_index = False
        if i != len(execution_lines) - 1:
            query += ','
        query += '\n'
    #Return part
    query += '    return '
    if len(encodes) != 0:
        query += f'encode($f0, "{list(encodes)[0]}")'
    else:
        query += '$f0'
    return query
