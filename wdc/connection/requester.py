# need library for images, we use Pillow
# for Jupyter Notebook, keep from IPython.display import Image
import requests

class ClientRequest:
    '''Class for server connection and certain methods'''

    # base url that we need to use
    service_endpoint = "https://ows.rasdaman.org/rasdaman/ows"
    
    # connection to server, use default value (if unspecified)
    def __init__(self, base_wcs_url = service_endpoint + "?service=WCS&version=2.0.1"):
        self.base_wcs_url = base_wcs_url
    


    def get_capabilities(self):
        '''
        Returns XML description of service capabilities and overview of covarages
        
        Args:
            self: Self@ClientRequest
        Returns:
            response
        '''
        request_url = self.base_wcs_url + "&request=GetCapabilities"
        response = requests.get(request_url, verify=False)
        return response
    


    def describe_coverage(self, cov_id):
        '''Returns XML-encoded description of a specific coverage
    
        Args:
            self: Self@ClientRequest
            cov_id (str): coverage id (e.g. "S2_L2A_32631_TCI_60m")
        Returns:
            response
        '''
        request_url = self.base_wcs_url + "&request=DescribeCoverage"
        request_url += f"&coverageId={cov_id}"
        response = requests.get(request_url, verify=False)
        return response



    def get_subset_coverage(self, cov_id, subsets, encode_format=None):
        '''
        Method that returns an encoded subset coverage with already defined subsets 

        Args:
            self: Self@ClientRequest
            cov_id (str): coverage id (e.g. "S2_L2A_32631_TCI_60m")
            subsets (list): list of descriptive subsets of the coverage
        Returns:
            response
        '''
        request_url = self.base_wcs_url + "&REQUEST=GetCoverage"
        request_url += f"&COVERAGEID={cov_id}"
        for subset in subsets:
            request_url += f"&SUBSET={subset}"
        if not encode_format is None:
            request_url += f"&FORMAT={encode_format}"
        # storing data we get in response
        response = requests.get(request_url, verify=False)
        return response
    


    def evaluate_query(self, query):
        '''Method to send WCPS query for evaluation'''
        response = requests.post(self.service_endpoint, data = {'query': query}, verify=False)
        return response.content


