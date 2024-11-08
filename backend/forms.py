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
