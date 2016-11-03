from django.conf.urls import url

from . import views

app_name = 'taxonomy'
urlpatterns = [
    url(r'^show/$', views.show_taxa, name='show_taxa'),
]
