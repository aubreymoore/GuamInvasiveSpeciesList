import json
import urllib.request

class Taxon_resolver:
    '''
    Uses the Global Names Resolver API to resolve a taxonomic name.
    Search is limited to the NCBI taxonomy (data_source_ids=4).

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

    def __init__(self, taxon_name_str):
        root_url = 'http://resolver.globalnames.org/name_resolvers.json'
        taxon_name_str = taxon_name_str.replace(' ', '+')
        url = '{}?names={};data_source_ids=4;with_vernaculars=True;best_match_only=True'.format(root_url, taxon_name_str)
        try:
            response = urllib.request.urlopen(url).read()
            self.ncbi_json = json.loads(response.decode('utf-8'))
            self.name_resolved = self.ncbi_json['data'][0]['is_known_name']
            if self.name_resolved:
                self.taxon_list = self.ncbi_json['data'][0]['results'][0]['classification_path'].split("|")
                self.rank_list = self.ncbi_json['data'][0]['results'][0]['classification_path_ranks'].split("|")
                self.common_name_list = []
                vernaculars = self.ncbi_json['data'][0]['results'][0]['vernaculars']
                for vernacular in vernaculars:
                    self.common_name_list.append(vernacular['name'])
        except urllib.error.URLError as e:
            print(e.reason)          
