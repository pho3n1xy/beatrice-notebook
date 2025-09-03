from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import JournalEntry, Notebook
# Import all three form classes
from .forms import JournalEntryForm, NonNegotiableFormSet, WhatWentWrongFormSet, NotebookForm
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone

# This mixin will handle the spill counter for all views
class SpillCounterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_spill = JournalEntry.objects.filter(
            user=self.request.user,
            cup_spilled=True
        ).order_by('-entry_date').first()

        if last_spill:
            days_since_spill = (timezone.now().date() - last_spill.entry_date).days
        else:
            first_entry = JournalEntry.objects.filter(user=self.request.user).order_by('entry_date').first()
            if first_entry:
                days_since_spill = (timezone.now().date() - first_entry.entry_date).days
            else:
                days_since_spill = 0

        context['days_since_last_spill'] = days_since_spill
        return context

# --- Notebook Views ---
class NotebookListView(LoginRequiredMixin, SpillCounterMixin, ListView):
    model = Notebook
    template_name = 'journal/notebook_list.html'
    context_object_name = 'notebooks'

    def get_queryset(self):
        return Notebook.objects.filter(user=self.request.user)

class NotebookDetailView(LoginRequiredMixin, SpillCounterMixin, DetailView):
    model = Notebook
    template_name = 'journal/notebook_detail.html'
    context_object_name = 'notebook'

    def get_queryset(self):
        return Notebook.objects.filter(user=self.request.user)

# ADD THESE NEW VIEWS FOR CREATING AND EDITING NOTEBOOKS
class NotebookCreateView(LoginRequiredMixin, SpillCounterMixin, CreateView):
    model = Notebook
    form_class = NotebookForm
    template_name = 'journal/notebook_form.html'
    success_url = reverse_lazy('journal:notebook_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NotebookUpdateView(LoginRequiredMixin, SpillCounterMixin, UpdateView):
    model = Notebook
    form_class = NotebookForm
    template_name = 'journal/notebook_form.html'
    success_url = reverse_lazy('journal:notebook_list')

    def get_queryset(self):
        return Notebook.objects.filter(user=self.request.user)



# --- Journal Entry Views ---
class JournalEntryDetailView(LoginRequiredMixin, SpillCounterMixin, DetailView):
    model = JournalEntry
    template_name = 'journal/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

class JournalEntryCreateView(LoginRequiredMixin, SpillCounterMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry_form.html'
    success_url = reverse_lazy('journal:notebook_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['non_negotiables'] = NonNegotiableFormSet(self.request.POST)
            # Add the new formset
            data['what_went_wrong_items'] = WhatWentWrongFormSet(self.request.POST)
        else:
            data['non_negotiables'] = NonNegotiableFormSet()
            # Add the new formset
            data['what_went_wrong_items'] = WhatWentWrongFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        non_negotiables = context['non_negotiables']
        what_went_wrong_items = context['what_went_wrong_items']
        form.instance.user = self.request.user
        self.object = form.save()

        if non_negotiables.is_valid():
            non_negotiables.instance = self.object
            non_negotiables.save()

        # Save the new formset
        if what_went_wrong_items.is_valid():
            what_went_wrong_items.instance = self.object
            what_went_wrong_items.save()

        return super().form_valid(form)


class JournalEntryUpdateView(LoginRequiredMixin, SpillCounterMixin, UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = 'journal/entry_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('journal:entry_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['non_negotiables'] = NonNegotiableFormSet(self.request.POST, instance=self.object)
            # Add the new formset
            data['what_went_wrong_items'] = WhatWentWrongFormSet(self.request.POST, instance=self.object)
        else:
            data['non_negotiables'] = NonNegotiableFormSet(instance=self.object)
            # Add the new formset
            data['what_went_wrong_items'] = WhatWentWrongFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        non_negotiables = context['non_negotiables']
        what_went_wrong_items = context['what_went_wrong_items']

        if non_negotiables.is_valid():
            non_negotiables.save()

        # Save the new formset
        if what_went_wrong_items.is_valid():
            what_went_wrong_items.save()

        return super().form_valid(form)

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)
