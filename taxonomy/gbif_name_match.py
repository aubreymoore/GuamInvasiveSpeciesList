import json
import urllib.request

class Taxon_resolver:
    '''
    Uses the GBIF Species API to resolve a taxonomic name.

    Example usage:

        x = Taxon_resolver('Apis mellifera')
        if x.name_resolved:
            <do stuff with the returned data>
        else:
            print('Taxon name not resolved.')
            print('Here is what was returned:\n')
            print(x.gbif_json) # let the user see what was returned

    Properties:

        gbif_json:        raw data from the NCBI taxonomy in json format
        name_resolved:    a boolean indicating whther of no the target name was found
        taxon_list:       list of dicts for taxonomic tree, from kingdom to target taxon
                          Example: [{'kingdom': 'Plantae'}, {'phylum': 'Tracheophyta'}]
    '''

    def __init__(self, taxon_name_str):
        taxon_name_str = taxon_name_str.replace(' ', '+')
        root_url = 'http://api.gbif.org/v1/species/match?verbose=false'
        url = '{}&name={}'.format(root_url, taxon_name_str)
        print(url)

        try:
            r = urllib.request.urlopen(url).read()
            self.gbif_json = json.loads(r.decode('utf-8'))
        except urllib.error.URLError as e:
            print('Taxon_resolver error: ', e.reason)
            return

        self.name_resolved = (self.gbif_json['matchType'] == 'EXACT')
        if self.name_resolved:
            self.taxon_list = []
            for rank in ['kingdom', 'phylum', 'class', 'family', 'genus', 'species']:
                if rank in self.gbif_json:
                    self.taxon_list.append({rank: self.gbif_json[rank]})
