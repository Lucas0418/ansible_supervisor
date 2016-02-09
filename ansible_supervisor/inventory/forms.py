from django.forms import ModelForm
from .models import Host, HostVar


class HostForm(ModelForm):
    class Meta:
        model = Host
        fields = ['ansible_alias']


class HostVarForm(ModelForm):
    class Meta:
        model = HostVar
        fields = ['host', 'var_value', 'var_name']
