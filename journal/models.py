from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import pylunar # Import the moon phase library
from datetime import datetime
from django.urls import reverse

#NOTEBOOK MODEL
class Notebook(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # We will create this URL later
        return reverse('journal:notebook_detail', args=[self.pk])


class JournalEntry(models.Model):
    # THIS IS THE NEW LINK TO THE NOTEBOOK
    notebook = models.ForeignKey(Notebook, related_name='entries', on_delete=models.CASCADE, null=True)

    # This links the entry to a specific user for privacy
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The two main text bodies as you requested
    waking_life_entry = models.TextField(verbose_name="Notes from Today")
    dream_entry = models.TextField(verbose_name="Notes from Dream", blank=True)

    entry_date = models.DateField(default=timezone.now)

    # Additional reflection fields
    rating = models.IntegerField(
        verbose_name="Rating for the day (1-10)",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )


     # New field for the Cup of Hermes
    cup_spilled = models.BooleanField(
        default=False,
        verbose_name="Did you spill the Cup of Hermes today?",
        help_text="In the end you will be a witness against yourself..."
    )

    # Automated fields
    moon_phase = models.CharField(max_length=50, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-entry_date'] # Show newest entries first

    def __str__(self):
        # Use the date if the title is empty
        return f'Entry for {self.entry_date}'

    # THIS IS THE NEW METHOD TO FIX THE LINKS
    def get_absolute_url(self):
        return reverse('journal:entry_detail', args=[self.pk])

    def save(self, *args, **kwargs):
        # This code runs every time an entry is saved.
        if not self.pk: # Only run this when the object is first created.
            # Coordinates for Fort Worth, Texas
            mi = pylunar.MoonInfo((32, 45, 23), (-97, 19, 57))
            date_to_use = self.entry_date if self.entry_date else timezone.now().date()
            date_obj = datetime.combine(date_to_use, datetime.min.time())
            mi.update(date_obj)

            # Save the moon phase name (e.g., "Waxing Crescent")
            self.moon_phase = mi.phase_name()

        super().save(*args, **kwargs) # Call the original save method

class NonNegotiable(models.Model):
    # This creates the many-to-one link. Many non-negotiables belong to one journal entry.
    journal_entry = models.ForeignKey(JournalEntry, related_name='non_negotiables', on_delete=models.CASCADE)

    name = models.CharField(max_length=100, help_text="")
    notes = models.TextField(blank=True, help_text="")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WhatWentWrongItem(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, related_name='what_went_wrong_items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, verbose_name="Item")

    class Meta:
        verbose_name_plural = "What Went Wrong Items"

    def __str__(self):
        return self.description
