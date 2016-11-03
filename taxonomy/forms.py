from django import forms

class TaxonForm(forms.Form):
    taxon = forms.CharField(label='Taxon', max_length=100)
