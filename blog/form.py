from django import forms
from .models import Commnt

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commnt
        fields = ('content',)