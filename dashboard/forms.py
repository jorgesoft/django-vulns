from django import forms
from .models import Vulnerabilities

class VulnerabilitiesForm(forms.Form):
    # The same fields as the Vulnerabilities table
    cve = forms.CharField(max_length=100)
    software = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255)
    severity = forms.DecimalField(max_digits=5, decimal_places=2)
    cwe = forms.CharField(max_length=100)