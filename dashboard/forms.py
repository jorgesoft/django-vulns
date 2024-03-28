from django import forms
from .models import Vulnerabilities

class VulnerabilitiesForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilities
        fields = ['cve', 'software', 'description', 'severity', 'cwe']
