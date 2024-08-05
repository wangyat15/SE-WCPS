import unittest
import sys
import os
import requests

# Add wdc to the PATH in order to import this
current_directory = os.path.dirname(os.path.abspath(__file__))
sprint_1_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(sprint_1_directory)

from wdc import Datacube


class ComparisonTest(unittest.TestCase):
    """
    Tests from https://standards.rasdaman.com/demo_jupyter-python.html
    They compare old evalution with new evaluation, to ensure correctness
    """

    def test_temporal_change_analysis(self):
        # original query
        service_endpoint = "https://ows.rasdaman.org/rasdaman/ows"
        query = '''
for $c in (S2_L2A_32631_B01_60m) 
return 
  encode((0.20*(35.0 + ((float) $c[ ansi( "2021-04-09" )])))[ E( 669960:729960 ), N( 4990200:5015220 )], "image/jpeg")
   '''
        response = requests.post(service_endpoint, data={'query': query},
                                 verify=False, timeout=20)
        # our query
        a = Datacube(coverage_name='S2_L2A_32631_B01_60m', index='ansi( "2021-04-09" ), \
                    E( 669960:729960 ), N( 4990200:5015220 )')
        b = ((a + 35.0) * 0.2).encode("image/jpeg")
        self.assertEqual(response.content, b.fetch())

    def test_refactor(self):
        # original query
        service_endpoint = "https://ows.rasdaman.org/rasdaman/ows"
        query = '''
for $c in (S2_L2A_32631_B08_10m),
    $d in (S2_L2A_32631_B04_10m),
    $e in (S2_L2A_32631_B03_10m)
let $cutOut := [ ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 ) ]
return
  encode({red:   $c[ $cutOut ] / 17.0; green: $d[ $cutOut ] / 17.0; blue:  $e[ $cutOut ] / 17.0}, "image/jpeg")
'''
        response = requests.post(service_endpoint, data={'query': query},
                                 verify=False, timeout=20)
        # our query
        c = Datacube(coverage_name='S2_L2A_32631_B08_10m',
                     index='ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 )')
        d = Datacube(coverage_name='S2_L2A_32631_B04_10m',
                     index='ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 )')
        e = Datacube(coverage_name='S2_L2A_32631_B03_10m',
                     index='ansi( "2021-04-09" ), E( 670000:679000 ), N( 4990220:4993220 )')
        f = Datacube.refactor([
            ('red', c / 17.0),
            ('green', d / 17.0),
            ('blue', e / 17.0)
        ]).encode("image/jpeg")
        self.assertEqual(response.content, f.fetch())

    def test_subindex(self):
        service_endpoint = "https://ows.rasdaman.org/rasdaman/ows"
        query = '''
for $c in (S2_L2A_32631_B08_10m)
  return avg($c)
'''
        response = requests.post(service_endpoint, data={'query': query},
                                 verify=False, timeout=20)
        c = Datacube(coverage_name='S2_L2A_32631_B08_10m')
        self.assertEqual(response.content, c.avg().fetch())


if __name__ == '__main__':
    unittest.main()
