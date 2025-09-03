from django.urls import path
from .views import (
    NotebookListView,
    NotebookDetailView,
    NotebookCreateView,
    NotebookUpdateView,
    JournalEntryDetailView,
    JournalEntryCreateView,
    JournalEntryUpdateView
)

app_name = 'journal'

urlpatterns = [
    # Main page is now the list of notebooks
    path('', NotebookListView.as_view(), name='notebook_list'),

    # URLs for Notebooks
    path('notebook/<int:pk>/', NotebookDetailView.as_view(), name='notebook_detail'),
    path('notebook/new/', NotebookCreateView.as_view(), name='notebook_create'),
    path('notebook/<int:pk>/edit/', NotebookUpdateView.as_view(), name='notebook_edit'),

    # URLs for Journal Entries
    path('entry/<int:pk>/', JournalEntryDetailView.as_view(), name='entry_detail'),
    path('entry/new/', JournalEntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/edit/', JournalEntryUpdateView.as_view(), name='entry_edit'),
]
