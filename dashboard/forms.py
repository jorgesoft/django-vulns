from django import forms
from .models import Vulnerabilities, Hosts, Os, Users, Groups, AccessRoles, ActiveUsers

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


class AccessRolesForm(forms.ModelForm):
    ACCESS_LEVEL_CHOICES = (
        ('High', 'High'),
        ('Normal', 'Normal'),
        ('Low', 'Low'),
    )

    access_level = forms.ChoiceField(
        choices=ACCESS_LEVEL_CHOICES,
        label="Access Level",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    
    class Meta:
        model = AccessRoles  # Assuming your model is named AccessRoles
        fields = ['name', 'access_level', 'description']
    
    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)
        super(AccessRolesForm, self).__init__(*args, **kwargs)
        if self.is_update:
            self.fields['name'].disabled = True
            self.fields['name'].required = False

class ActiveUsersForm(forms.ModelForm):
    hosts = forms.ModelChoiceField(
        queryset=Hosts.objects.all(),
        label="Hosts",
        to_field_name='id',  # Ensures the ID is used
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ActiveUsers
        fields = ['hosts', 'users', 'access_roles']
        widgets = {
            'hosts': forms.Select(attrs={'class': 'form-control'}),
            'users': forms.Select(attrs={'class': 'form-control'}),
            'access_roles': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ActiveUsersForm, self).__init__(*args, **kwargs)
        self.fields['hosts'].queryset = Hosts.objects.all()
        self.fields['users'].queryset = Users.objects.all()
        self.fields['access_roles'].queryset = AccessRoles.objects.all()

class ResultsForm(forms.Form):
    hosts = forms.ModelChoiceField(queryset=Hosts.objects.all(), label="Host", to_field_name="id",
                             widget=forms.Select(attrs={'class': 'form-control'}))
    vulnerabilities = forms.ModelChoiceField(queryset=Vulnerabilities.objects.all(), label="Vulnerability", to_field_name="cve",
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    proof = forms.CharField(max_length=45, required=False, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.CharField(max_length=45, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_found = forms.DateField(required=False,
                                  widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    last_update = forms.DateField(required=False,
                                  widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))