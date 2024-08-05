import unittest
import sys
import os

from wdc.helpers.subset import Subset

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc.coverage.args_formatter import Formatting


class TestAnsi(unittest.TestCase):
    """Tests for the ansi format"""

    def test_ansi_slice_output(self):
        out = Formatting.ansi_sliceformat("2021", "04", "09")
        # checking if date slice is formatted correctly
        self.assertEqual(out, "ansi(\"2021-04-09\")")

    def test_ansi_trim_output(self):
        out = Formatting.ansi_trimformat("2021", "04", "09", "2021", "05", "01")
        # checking if date trim is formatted correctly
        self.assertEqual(out, "ansi(\"2021-04-09\",\"2021-05-01\")")


class TestSubsetE(unittest.TestCase):
    """Tests for the E format"""

    def test_E_slice_output(self):
        out = Formatting.E_sliceformat(669960)
        # checking if E slice is formatted correctly
        self.assertEqual(out, "E(669960)")

    def test_E_trim_output(self):
        out = Formatting.E_trimformat(669960, 729960)
        # checking if E trim is formatted correctly
        self.assertEqual(out, "E(669960,729960)")


class TestSubsetN(unittest.TestCase):
    """Tests for the N format"""

    def test_N_slice_output(self):
        out = Formatting.N_sliceformat(4990200)
        # checking if N slice is formatted correctly
        self.assertEqual(out, "N(4990200)")

    def test_N_trim_output(self):
        out = Formatting.N_trimformat(4990200, 5015220)
        # checking if N trim is formatted correctly
        self.assertEqual(out, "N(4990200,5015220)")


class TestLat(unittest.TestCase):
    """Tests for the Lat format"""

    def test_Lat_slice_output(self):
        out = Formatting.Lat_sliceformat(60)
        # checking if Lat slice is formatted correctly
        self.assertEqual(out, "Lat(60)")

    def test_Lat_trim_output(self):
        out = Formatting.Lat_trimformat(60, 80)
        # checking if Lat trim is formatted correctly
        self.assertEqual(out, "Lat(60,80)")


class TestLon(unittest.TestCase):
    """Tests for the Lon format"""

    def test_Lat_slice_output(self):
        out = Formatting.Lon_sliceformat(60)
        # checking if Lat slice is formatted correctly
        self.assertEqual(out, "Lon(60)")

    def test_Lat_trim_output(self):
        out = Formatting.Lon_trimformat(60, 80)
        # checking if Lat trim is formatted correctly
        self.assertEqual(out, "Lon(60,80)")

class TestSubset(unittest.TestCase):
    """Tests for the Subsets"""

    def test_subsets_output(self):
        out = Formatting.subsets_format([Subset("ansi", "2014-09"), Subset("Lat", 20), Subset("Lon", 50)])

        self.assertEqual(out, 'ansi("2014-09"), Lat(20), Lon(50)')

#  Additional unit test cases for invalid date, latitude or longitude format, sprint#3
    # return "invalid date format"
    def test_ansi_slice_output(self):
        out = Formatting.ansi_sliceformat("2021", "13", "09")
        # checking if date slice is formatted correctly
        self.assertEqual(out, "ansi(\"2021-13-09\")")
    
    # return "invalid date format"
    def test_ansi_trim_output(self):
        out = Formatting.ansi_trimformat("2021", "04", "09", "2021", "05", "40")
        # checking if date trim is formatted correctly
        self.assertEqual(out, "ansi(\"2021-04-09\",\"2021-05-40\")")

class TestLat(unittest.TestCase):
    """Tests for the Lat format"""

    def test_Lat_slice_output(self):
        out = Formatting.Lat_sliceformat(100)
        # checking if Lat slice is formatted correctly
        self.assertEqual(out, "Lat(100)")

    def test_Lat_trim_output(self):
        out = Formatting.Lat_trimformat(-100, 80)
        # checking if Lat trim is formatted correctly
        self.assertEqual(out, "Lat(-100,80)")

class TestLon(unittest.TestCase):
    """Tests for the Lon format"""

    def test_Lat_slice_output(self):
        out = Formatting.Lon_sliceformat(200)
        # checking if Lat slice is formatted correctly
        self.assertEqual(out, "Lon(200)")

    def test_Lat_trim_output(self):
        out = Formatting.Lon_trimformat(-200, 80)
        # checking if Lat trim is formatted correctly
        self.assertEqual(out, "Lon(-200,80)")

if __name__ == '__main__':
    unittest.main()
