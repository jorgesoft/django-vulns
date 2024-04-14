from django import forms
from .models import Vulnerabilities, Hosts, Os, Users, Groups

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


class GroupsForm(forms.Form):
    name = forms.CharField(label='Group Name', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(label='Group Type', max_length=45, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


class OsForm(forms.ModelForm):
    FAMILY_CHOICES = [
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
        ('MacOS', 'MacOS'),
    ]

    family = forms.ChoiceField(choices=FAMILY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Os
        fields = ['family', 'version', 'patch']
        widgets = {
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'patch': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssignedGroupsForm(forms.Form):
    group_name = forms.ModelChoiceField(
        queryset=Groups.objects.all(),
        label='Group',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='name',
        required=True
    )
    host_id = forms.ModelChoiceField(
        queryset=Hosts.objects.all(),
        label='Host',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id',
        required=True
    )