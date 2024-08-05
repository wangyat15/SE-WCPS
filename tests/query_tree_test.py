import unittest

# Need to add the .. folder to PATH to access a module via tests folder
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc import Datacube


class TestQueryTree(unittest.TestCase):
    def test_reference_validness(self):
        a = Datacube().get_tree()
        b = Datacube().get_tree()
        c = a.merge_to(b, '+')
        tmp = str(c)
        a = Datacube().get_tree()
        b = Datacube().get_tree()
        # Making random actions with a and b trees
        for _ in range(10):
            a = a.merge_to(b, '/')
            b = b.merge_to(a, '*')
        # Checking, that the result of going through a c is not changed
        self.assertEqual(tmp, str(c))


if __name__ == '__main__':
    unittest.main()
