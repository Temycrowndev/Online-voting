from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from django.core.exceptions import ValidationError

from .models import Candidate, Vote, Position

# Custom form to enforce group selection
class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if not groups:
            raise ValidationError("You must assign the user to at least one group (e.g., Voters or Candidates).")
        return groups

# Custom admin with the form
class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

# Unregister and re-register User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Position)
