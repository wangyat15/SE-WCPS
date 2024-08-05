import unittest
import time
import hashlib

# Need to add the .. folder to PATH to access a module via tests folder
import sys
import os

from wdc.helpers.subset import Subset

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc import Datacube


class TestDatacubePrimary(unittest.TestCase):
    """Class containing tests for actions on the datacube"""
    def test_add_output(self):
        initial_number = Datacube.counter
        a = Datacube()
        b = Datacube()
        c = a + b
        self.assertEqual(str(a.get_tree()), f"c{initial_number}")
        self.assertEqual(str(b.get_tree()), f"c{initial_number+1}")
        self.assertEqual(str(c.get_tree()), f"(c{initial_number})+(c{initial_number+1})")

    def test_sub_output(self):
        initial_number = Datacube.counter
        a = Datacube()
        b = Datacube()
        c = a - b
        self.assertEqual(str(a.get_tree()), f"c{initial_number}")
        self.assertEqual(str(b.get_tree()), f"c{initial_number+1}")
        self.assertEqual(str(c.get_tree()), f"(c{initial_number})-(c{initial_number+1})")

    def test_mult_output(self):
        initial_number = Datacube.counter
        a = Datacube()
        b = Datacube()
        c = a * b
        self.assertEqual(str(a.get_tree()), f"c{initial_number}")
        self.assertEqual(str(b.get_tree()), f"c{initial_number+1}")
        self.assertEqual(str(c.get_tree()), f"(c{initial_number})*(c{initial_number+1})")

    def test_div_output(self):
        initial_number = Datacube.counter
        a = Datacube()
        b = Datacube()
        c = a / b
        self.assertEqual(str(a.get_tree()), f"c{initial_number}")
        self.assertEqual(str(b.get_tree()), f"c{initial_number+1}")
        self.assertEqual(str(c.get_tree()), f"(c{initial_number})/(c{initial_number+1})")
    
    def test_equation_output(self):
        initial_number = Datacube.counter
        a = Datacube()
        b = Datacube()
        c = a + b
        d = c * c
        self.assertEqual(str(a.get_tree()), f"c{initial_number}")
        self.assertEqual(str(b.get_tree()), f"c{initial_number+1}")
        self.assertEqual(str(c.get_tree()), f"(c{initial_number})+(c{initial_number+1})")
        self.assertEqual(str(d.get_tree()), f"((c{initial_number})+(c{initial_number+1}))*((c{initial_number})+(c{initial_number+1}))")
    
    def test_equation_performance(self):
        REPEATS = 100000
        TIME_BOUND = 1.0
        # The time bound could be changed as the exact environment could be slower
        start_time = time.time()
        a = Datacube()
        b = Datacube()
        for _ in range(REPEATS):
            a = a + b
        end_time = time.time()
        self.assertLess(end_time - start_time, TIME_BOUND)

    def test_fetch(self):
        # The hash of data that is supposed to be in this test
        FETCH_HASH = '50479dd364f2d9d64f186279bb35ea00e8e739c01fe88f70c4f9e79943fa0e39'
        # Fetching data
        a = Datacube(index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ])
        b = Datacube(index=[
                Subset("ansi", "2021-04-09"),
                Subset("E", 670000, 679000),
                Subset("N", 4990220, 4993220),
            ])
        c = (a + b).encode("image/png")
        # Calculating hash and comparing it
        hash_object = hashlib.sha256()
        hash_object.update(str(c.fetch()).encode('utf-8'))
        self.assertEqual(hash_object.hexdigest(), FETCH_HASH)


if __name__ == '__main__':
    unittest.main()
