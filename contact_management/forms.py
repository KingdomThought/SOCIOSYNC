from django import forms
from .models import Contact, Reminder

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'relationship', 'frequency']

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['contact', 'date_time', 'sent']