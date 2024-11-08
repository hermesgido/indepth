# myapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import AssignPermissionsForm, RoleForm


def roles(request):
    roles = Group.objects.all()
    return render(request, 'roles.html', {'roles': roles})


def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role added successfully.')
            return redirect('roles')
    return redirect('roles')


def edit_role(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('roles')
    return redirect('roles')


def delete_role(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    role.delete()
    messages.success(request, 'Role deleted successfully.')
    return redirect('roles')


def assign_permissions(request, role_id):
    role = get_object_or_404(Group, id=role_id)
    if request.method == 'POST':
        form = AssignPermissionsForm(request.POST)
        if form.is_valid():
            # Assign new permissions
            role.permissions.set(form.cleaned_data['permissions'])
            messages.success(request, 'Permissions updated successfully.')
            return redirect('roles')
    else:
        form = AssignPermissionsForm(
            initial={'permissions': role.permissions.all()})
    return render(request, 'assign_permissions.html', {'form': form, 'role': role})
