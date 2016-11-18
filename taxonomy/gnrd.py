import json
import urllib.request

class Discover_names:
    '''
    Uses the Global Names Recognition and Discovery API to find taxonomic Names
    in documents.

    Example usage:

        x = Taxon_resolver('Apis mellifera')
        if x.name_resolved:
            <do stuff with the returned data>
        else:
            print('Taxon name not resolved.')
            print('Here is what was returned:\n')
            print(x.ncbi_json) # let the user see what was returned

    Properties:

        ncbi_json:        raw data from the NCBI taxonomy in json format
        name_resolved:    a boolean indicating whther of no the target name was found
        taxon_list:       names for taxonomic tree, from root to target name
        rank_list:        taxonomic ranks a=for taxon_list
        common_name_list: list of common names for the target name
    '''

    def __init__(self, document_url):
        root_url = 'http://gnrd.globalnames.org/name_finder.json'
        url = '{}?url={}'.format(root_url, document_url)
        try:
            self.response1 = urllib.request.urlopen(url).read()
            self.json1 = json.loads(self.response1.decode('utf-8'))
            print(self.response1)
        except urllib.error.URLError as e:
            print(e.reason)

        try:
            url = self.json1['token_url']
            self.response2 = urllib.request.urlopen(url).read()
            self.json2 = json.loads(self.response2.decode('utf-8'))
            print(self.response2)
        except urllib.error.URLError as e:
            print(e.reason)
