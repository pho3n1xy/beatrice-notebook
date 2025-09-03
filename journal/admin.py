from django.contrib import admin
from .models import Notebook, JournalEntry, NonNegotiable, WhatWentWrongItem

# This makes the new Notebook model appear in the admin panel
@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'description')

# --- Existing Admin Configuration ---
class WhatWentWrongItemInline(admin.TabularInline):
    model = WhatWentWrongItem
    extra = 1

class NonNegotiableInline(admin.TabularInline):
    model = NonNegotiable
    extra = 1

# --- Updated JournalEntry Admin ---
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    # We've added 'notebook' to the display and filters
    list_display = ('__str__', 'notebook', 'user', 'entry_date', 'rating')
    list_filter = ('user', 'notebook', 'entry_date')
    inlines = [NonNegotiableInline, WhatWentWrongItemInline]
