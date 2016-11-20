from django.shortcuts import render

from django.template import RequestContext

from taxonomy.models import Taxon
#from taxon_names_resolver import Resolver
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .forms import TaxonForm

from .ncbi import Taxon_resolver

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned


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

def add_taxon(request):
    taxon = request.POST['taxon']
    result = Taxon_resolver(taxon)
    result_list = []
    if result.name_resolved:
        result_list.append('Name resolved.')
        result_list.append('')
        # result_string = result_string.join(result.taxon_list) + '\n'
        # result_string = result_string.join(result.rank_list) + '\n'

        try:
            node = Taxon.objects.get(name='root')
        except Taxon.DoesNotExist:
            node = Taxon.objects.create(name='root')

        for rank, taxon in zip(result.rank_list, result.taxon_list):
            if rank != '':
                try:
                    node = Taxon.objects.create(name=taxon, rank=rank, parent=node)
                    result_list.append(taxon + ' added to local database.')
                except IntegrityError:
                    node = Taxon.objects.get(name=taxon)
                    result_list.append(taxon + ' not added to local database; already there.')
                    pass
    else:
        result_list.append('Taxon name not resolved.')
        result_list.append('Here is what was returned:')
        result_list.append('')
        result_list.append(result.ncbi_json) # let the user see what was returned
    return render(request, "results.html", {'result_list': result_list})

def add_taxon_form(request):
    return render(request, "taxonform.html")
