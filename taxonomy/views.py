from django.shortcuts import render

from django.template import RequestContext

from taxonomy.models import Taxon
#from taxon_names_resolver import Resolver
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .forms import TaxonForm
#from taxonomy.gbif_name_match import Taxon_resolver

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import requests


def show_taxa(request):
    nodes = None
    error_msg = None
    taxon = 'root'
    if request.GET.get('taxon'):
        taxon = request.GET.get('taxon')
        try:
            node = Taxon.objects.get(name__istartswith=taxon)
        except MultipleObjectsReturned:
            error_msg = 'A search for "{}" returned multiple taxa.'.format(taxon)
            return render(request, "taxa.html", {'taxon':taxon, 'error_msg':error_msg,'nodes':nodes})
        except ObjectDoesNotExist:
            error_msg = 'A search for "{}" did not find any matches.'.format(taxon)
            return render(request, "taxa.html", {'taxon':taxon, 'error_msg':error_msg,'nodes':nodes})

        nodes = node.get_descendants(include_self=True)
    return render(request, "taxa.html", {'taxon':taxon, 'error_msg':error_msg, 'nodes':nodes})

def match_name(name):
    '''
    Matches scientific names using the GBIF Species API.
    Returns GBIF JSON.
    '''
    url = 'http://api.gbif.org/v1/species/match'
    params = {'name': name, 'verbose': 'true'}
    r = requests.get(url, params=params)
    return(r.json())

def check_db_for_taxon(taxon):
    '''
    Check to see if taxon is already in the db
    '''
    try:
        node = Taxon.objects.get(name=taxon)
    except Taxon.DoesNotExist:
        node = None
    return(node)

def add_taxon(request):
    result_list = []
    taxon = request.POST['taxon']

    # If taxon is already in db; return early.
    if check_db_for_taxon(taxon):
        result_list.append('{} already in db.'.format(taxon))
        return render(request, "results.html", {'result_list': result_list})

    # Attempt to match taxon using the GBIF Species API
    res = match_name(taxon)

    # Extract some key items for the user
    if 'note' in res:
        result_list.append('note: {}'.format(res['note']))
    if 'matchType' in res:
        result_list.append('matchType: {}'.format(res['matchType']))
    if 'status' in res:
        result_list.append('status: {}'.format(res['status']))

    name_resolved = (
        'matchType' in res and
        res['matchType'] == 'EXACT' and
        'status' in res and
        res['status'] == 'ACCEPTED'
        )

    if name_resolved:
        result_list.append('Name resolved.')
        result_list.append('')

        # Build hierarchy
        taxon_list = []
        for rank in ['kingdom', 'phylum', 'class', 'family', 'genus', 'species']:
            if rank in res:
                taxon_list.append({rank: res[rank]})
        print(taxon_list)

        try:
            node = Taxon.objects.get(name='root')
        except Taxon.DoesNotExist:
            node = Taxon.objects.create(name='root')

        for  taxon in taxon_list:
            for rank, name in taxon.items():
                try:
                    node = Taxon.objects.create(name=name, rank=rank, parent=node)
                    result_list.append('{} {} added to local database.'.format(rank, name))
                except IntegrityError:
                    node = Taxon.objects.get(name=taxon)
                    result_list.append('{} {} not added to local database; already there.'.format(rank, name))
                    pass
    else:
        result_list.append('Taxon name not resolved.')
        result_list.append('Here is what was returned:')
        result_list.append('')
        result_list.append(res) # let the user see what was returned
    return render(request, "results.html", {'result_list': result_list})

def add_taxon_form(request):
    return render(request, "taxonform.html")
