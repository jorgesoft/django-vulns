from django import forms
from .models import Vulnerabilities, Hosts, Os, Users

class VulnerabilitiesForm(forms.Form):
    # The same fields as the Vulnerabilities table
    cve = forms.CharField(max_length=100)
    software = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255)
    severity = forms.DecimalField(max_digits=5, decimal_places=2)
    cwe = forms.CharField(max_length=100)


class HostForm(forms.ModelForm):
    os_id = forms.ModelChoiceField(
        queryset=Os.objects.all(),
        label="Operating System",
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name="id",  # Ensures the ID is used
    )

    class Meta:
        model = Hosts
        fields = ['name', 'ip', 'os_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom label presentation can be handled here if needed


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'full_name']
