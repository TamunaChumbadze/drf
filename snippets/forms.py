from django import forms
from .models import Snippet

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = [
            'title',
            'description',
            'code',
            'language',
            'style',
            'linenos',
            'is_public',
            'tags',
        ]