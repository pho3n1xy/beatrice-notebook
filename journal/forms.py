from django import forms
from .models import Notebook, JournalEntry, NonNegotiable, WhatWentWrongItem
from django.forms import inlineformset_factory

# THIS IS THE NEW FORM FOR CREATING AND EDITING NOTEBOOKS
class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['name', 'description']

class JournalEntryForm(forms.ModelForm):
    # This queryset ensures the dropdown only shows notebooks belonging to the current user.
    # We will pass the user in from the view.
    notebook = forms.ModelChoiceField(queryset=Notebook.objects.none())

    class Meta:
        model = JournalEntry
        # Add 'notebook' to the list of fields to display
        fields = ['notebook', 'waking_life_entry', 'dream_entry', 'entry_date', 'rating', 'cup_spilled']
        widgets = {
            'entry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # We pop the user from the kwargs so we can use it to filter the notebook queryset.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['notebook'].queryset = Notebook.objects.filter(user=user)

# --- Formsets remain the same ---

NonNegotiableFormSet = inlineformset_factory(
    JournalEntry,
    NonNegotiable,
    fields=('name', 'notes', 'completed'),
    extra=0,
    can_delete=True
)

WhatWentWrongFormSet = inlineformset_factory(
    JournalEntry,
    WhatWentWrongItem,
    fields=('description',),
    extra=1,
    can_delete=True
)
