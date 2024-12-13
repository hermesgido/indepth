from .models import Facility
from django import forms
from django.contrib.auth.models import Group, Permission


class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class AssignPermissionsForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = [
            'district', 'ward', 'hfrcode', 'supporting_facility',
            'responsible_cso', 'responsible_person', 'mobile_no',
            'app_password', 'status',
        ]
        widgets = {
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter district'}),
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ward'}),
            'hfrcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter HFR Code'}),
            'supporting_facility': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supporting facility'}),
            'responsible_cso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter responsible CSO'}),
            'responsible_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter responsible person'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'app_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter app password'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
