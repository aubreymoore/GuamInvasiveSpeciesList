from django.shortcuts import render

from django.template import RequestContext

from taxonomy.models import Taxon
from taxon_names_resolver import Resolver
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .forms import TaxonForm

def show_taxa(request):
    return render(request, "taxa.html", {'nodes':Taxon.objects.all()})

def add_taxonx(taxon):
    try:
        Taxon.objects.get(name=taxon)
        return(taxon+' is already in local database.')
    except Taxon.DoesNotExist:
        try:
            resolver = Resolver(terms=[taxon])
            resolver.main()
        except:
            return(taxon+' not found by Global Names Resolver.')

    taxon_list = resolver.retrieve('classification_path')[0]
    rank_list = resolver.retrieve('classification_path_ranks')[0]

    for i in range(len(taxon_list)):
        try:
            node = Taxon.objects.get(name=taxon_list[i])[0]
        except Taxon.DoesNotExist:
            if i==0:
                Taxon.objects.create(name=taxon_list[i], rank=rank_list[i], parent=None)
            else:
                Taxon.objects.create(name=taxon_list[i], rank=rank_list[i], parent=node)
    return(taxon_list, rank_list)

def add_taxon2(request):
    taxon = request.POST['taxon']

    try:
        resolver = Resolver(terms=[taxon])
        resolver.main()
    except:
        return(taxon+' not found by Global Names Resolver.')

    print(resolver.__dict__)

    taxon_list = resolver.retrieve('classification_path')[0]
    print(taxon_list)
    rank_list = resolver.retrieve('classification_path_ranks')[0]
    print(rank_list)

    try:
        node = Taxon.objects.get(name='root')
    except Taxon.DoesNotExist:
        node = Taxon.objects.create(name='root')

    for i in range(len(taxon_list)):
        if rank_list[i] != '':
            try:
                node = Taxon.objects.create(name=taxon_list[i], rank=rank_list[i], parent=node)
                print(taxon_list[i]+' added to local database.')
            except IntegrityError:
                node = Taxon.objects.get(name=taxon_list[i])
                print(taxon_list[i]+' not added to local database; already there.')
                pass
    return(render(request, "taxonform.html"))

def add_taxon(request):
    return(render(request, "taxonform.html"))
