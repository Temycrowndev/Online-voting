from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Vote, Candidate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'



class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['candidate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['candidate'].queryset = Candidate.objects.all()
        self.fields['candidate'].widget.attrs.update({'class': 'form-select'})
