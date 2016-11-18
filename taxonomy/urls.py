from django.conf.urls import url

from . import views

app_name = 'taxonomy'
urlpatterns = [
    url(r'^show/$', views.show_taxa, name='show_taxa'),
    url(r'^add/$', views.add_taxon_form, name='add_taxon_form'),
    url(r'^addtaxon/$', views.add_taxon, name='addtaxon'),
]
