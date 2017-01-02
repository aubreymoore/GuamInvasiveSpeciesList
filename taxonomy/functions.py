import requests
import time
from taxonomy.models import NameFinderResult

def find_names(doc_url):
    '''
    DOCS GO Here
    '''
    url = 'http://gnrd.globalnames.org/name_finder.json?'
    #params = {'url': 'https://aubreymoore.github.io/crop-pest-list/list.html'}
    params = {'url': doc_url, 'data_source_ids': '11'}
    r = requests.get(url, params)
    mydict = r.json()
    token_url = mydict['token_url']
    print('token_url: {}'.format(token_url))

    # Poll the token url once a second for 100 s to see if results have been returned.
    i = 0
    while i <= 100:
        i += 1
        time.sleep(1)
        r = requests.get(token_url)
        mydict = r.json()
        status = mydict.get('status','')
        queue_size = mydict.get('queue_size','')
        print('{} status: {} queue_size: {}'.format(i, status, queue_size))
        if status != 303:
            break
    return(mydict)

#doc_url = 'https://aubreymoore.github.io/crop-pest-list/list.html'
#extracted_taxa = find_names(doc_url)

def json_to_name_finder_results(pub, name_finder_json):
    '''
    DOCS GO Here
    '''
    d = name_finder_json
    for name in d['resolved_names']:
        x = NameFinderResult()
        x.pub = pub
        x.is_known_name = name['is_known_name']
        x.supplied_name_string = name['supplied_name_string']

        print('supplied_name_string: {}   is_known_name: {}'.format(
              name['supplied_name_string'],
              name['is_known_name']))
        results = name['results']
        if len(results) == 1:
            r = results[0]
            x.classification_path_ranks = r.get('classification_path_ranks','')
            x.classification_path = r.get('classification_path','')
            x.current_name_string = r.get('current_name_string','')
            x.imported_at = r.get('imported_at','')
            x.canonical_form = r.get('canonical_form','')
            x.data_source_id = r.get('data_source_id','')
            x.match_value = r.get('match_value','')
            x.data_source_title = r.get('data_source_title','')
            x.gni_uuid = r.get('gni_uuid','')
            x.edit_distance = r.get('edit_distance','')
            x.match_type = r.get('match_type','')
            x.name_string = r.get('name_string','')
            x.current_taxon_id = r.get('current_taxon_id','')
            x.taxon_id = r.get('taxon_id','')
            x.prescore = r.get('prescore','')
            x.classification_path_ids = r.get('classification_path_ids','')
            x.score = r.get('score','')
        x.save()
