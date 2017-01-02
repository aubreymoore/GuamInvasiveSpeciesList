from django.shortcuts import render

from django.template import RequestContext

from taxonomy.models import Taxon, DwcaTaxon
#from taxon_names_resolver import Resolver
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .forms import TaxonForm
#from taxonomy.gbif_name_match import Taxon_resolver

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import requests
import logging
from django.http import HttpResponse
from .dwca_processor import dwca_to_db
#from django.contrib.auth.decorators import user_passes_test
import time

stdlogger = logging.getLogger(__name__)

def myfunction():
    stdlogger.debug("this is a debug message!")

def myotherfunction():
    stdlogger.error("this is an error message!!")


def find_names(modeladmin, request, queryset):
    pass


def eureka(request):

    # Admin actions:
    # https://docs.djangoproject.com/en/1.10/ref/contrib/admin/actions/

    # html = """
    # <html>
    #     <body>Eureka2</body>
    # </html>
    # """
    # url = 'http://gnrd.globalnames.org/name_finder.json?'
    # params = {'url': 'https://aubreymoore.github.io/crop-pest-list/list.html'}
    # r = requests.get(url, params)
    # rj = r.json()
    # token_url = rj['token_url']
    # print(token_url)
    # i = 0
    # while i <= 100:
    #     time.sleep(1)
    #     r = requests.get(token_url)
    #     rj = r.json()
    #     status = rj['status']
    #     print(i, statusj)
    return render(request, "eureka.html")


def empty_dwca_tables(request):
    # If we delete all records from DwcaTaxon, all associated records in the other 3 DwCA
    # tables should disappear because the "on_delete=models.CASCADE" is set.
    DwcaTaxon.objects.all().delete()
    return HttpResponse('All records have been deleted from DwCA database tables.')

def add_dwca_to_db(request):
    if not request.user.is_authenticated:
         return HttpResponse('Sorry, you must be logged in to access this page.')
    dwca_to_db()
    return HttpResponse('Data from the Darwin Core Archive have been stored in the database.')

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

#@user_passes_test(lambda u: u.is_staff)
def resolve_names_in_dwca(request):
    if not request.user.is_authenticated:
         return HttpResponse('Sorry, you must be logged in to access this page.')
    taxa = DwcaTaxon.objects.values_list('scientificName', flat=True)
    for taxon in taxa:
        doit(taxon)
    html = '''
    <html>
        <body>
            Finished resolving scientific names in the Darwin Core Archive.
        </body>
    </html>
    '''
    return HttpResponse(html)





def add_taxon(request):
    stdlogger.debug("Entering add_taxon")

    taxon = request.POST['taxon']
    result_list = doit(taxon)
    return render(request, "results.html")

def add_taxon_form(request):
    return render(request, "taxonform.html")
