import unittest
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc.connection.requester import ClientRequest


class TestGetCapabilities(unittest.TestCase):
    def test_get_capabilites_output(self):
        request = ClientRequest()
        response = request.get_capabilities()
        # checking if the status_code = 200 which means successful, else error
        self.assertEqual(response.status_code, 200, "Error in get_capabilities") 
        
        
class TestDescribeCoverage(unittest.TestCase):
    def test_describe_coverage_output(self):
        request = ClientRequest()
        cov_id = "S2_L2A_32631_TCI_60m"
        response = request.describe_coverage(cov_id)
        # checking if the status_code = 200 which means successful, else error
        self.assertEqual(response.status_code, 200, "Error in describe_coverage")


class TestGetSubsetCoverage(unittest.TestCase):
    def test_get_subset_coverage_output(self):
        request = ClientRequest()
        cov_id = "S2_L2A_32631_TCI_60m"
        subsets = ["ansi(\"2021-04-09\")", "E(669960,729960)", "N(4990200,5015220)"]
        response = request.get_subset_coverage(cov_id, subsets, "jpeg")
        # checking if the status_code = 200 which means successful, else error
        self.assertEqual(response.status_code, 200, "Error in get_subset_coverage") 


if __name__ == '__main__':
    unittest.main()
