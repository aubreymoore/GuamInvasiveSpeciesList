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
import logging

stdlogger = logging.getLogger(__name__)

def myfunction():
    stdlogger.debug("this is a debug message!")

def myotherfunction():
    stdlogger.error("this is an error message!!")




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

def doit(taxon):
    stdlogger.debug("Entering doit with taxon = '{}'".format(taxon))

    # If taxon is already in db; return early.
    if check_db_for_taxon(taxon):
        stdlogger.debug('{} already in db.'.format(taxon))
        return([])

    # Attempt to match taxon using the GBIF Species API
    res = match_name(taxon)

    # Extract some key items for the user
    if 'note' in res:
        stdlogger.debug('note: {}'.format(res['note']))
    if 'matchType' in res:
        stdlogger.debug('matchType: {}'.format(res['matchType']))
    if 'status' in res:
        stdlogger.debug('status: {}'.format(res['status']))

    name_resolved = (
        'matchType' in res and
        res['matchType'] == 'EXACT' and
        'status' in res and
        res['status'] == 'ACCEPTED'
        )

    if name_resolved:
        stdlogger.debug('Name resolved.')
        stdlogger.debug('')

        # Build hierarchy
        taxon_list = []
        for rank in ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']:
            if rank in res:
                taxon_list.append({rank: res[rank]})
        stdlogger.debug(taxon_list)

        try:
            node = Taxon.objects.get(name='root')
        except Taxon.DoesNotExist:
            node = Taxon.objects.create(name='root')

        for  taxon in taxon_list:
            for rank, name in taxon.items():
                try:
                    node = Taxon.objects.create(name=name, rank=rank, parent=node)
                    stdlogger.debug('{} {} added to local database.'.format(rank, name))
                except IntegrityError:
                    node = Taxon.objects.get(name=name)
                    stdlogger.debug('{} {} not added to local database; already there.'.format(rank, name))
                    pass
    else:
        stdlogger.info('Taxon name "{}" not resolved.'.format(taxon))
        stdlogger.info('Here is what was returned:')
        stdlogger.info('')
        stdlogger.info(res) # let the user see what was returned
    return([])


def add_taxon(request):
    stdlogger.debug("Entering add_taxon")

    taxon = request.POST['taxon']
    result_list = doit(taxon)
    return render(request, "results.html")

def add_taxon_form(request):
    return render(request, "taxonform.html")
