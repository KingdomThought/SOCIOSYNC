from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Contact

from django.views import View
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import Contact


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from contact_management.models import Contact, Reminder
from contact_management.forms import ContactForm, ReminderForm
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class AddNewContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Temporarily save contact instance to get id for the Reminder instances
        self.object = form.save(commit=False)

        contact = self.object

        delta = contact.get_frequency_delta()

        if delta is None:
            return super().form_valid(form)  # For other frequencies, no reminders are created.

        reminders = []
        if contact.frequency != 'Daily':
            for i in range(3):
                reminders.append(Reminder(
                    contact=contact,
                    date_time=timezone.now() + (i + 1) * delta / 3,
                    position=i,  # Assign position here
                ))
        else:
            reminders.append(Reminder(
                contact=contact,
                date_time=timezone.now() + delta,
                position=0,  # Assign position here
            ))

        # Set the next reminder for the contact
        contact.next_reminder = min(r.date_time for r in reminders)

        # Now save the contact instance
        self.object.save()

        # Save all the reminders after the contact is saved
        for reminder in reminders:
            reminder.save()

        return HttpResponseRedirect(self.get_success_url())

    success_url = reverse_lazy('dashboard')




class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'edit_contact.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        contact = self.object
        delta = contact.get_frequency_delta()

        if delta is None:
            return response

        # Delete existing reminders
        contact.reminder_set.all().delete()

        reminders = []
        if contact.frequency != 'Daily':
            for i in range(3):
                reminders.append(Reminder(
                    contact=contact,
                    date_time=timezone.now() + (i + 1) * delta / 3,
                    position=i,
                ))
        else:
            reminders.append(Reminder(
                contact=contact,
                date_time=timezone.now() + delta,
                position=0,
            ))

        # Save the new reminders
        for reminder in reminders:
            reminder.save()

        return response

    def get_success_url(self):
        return reverse_lazy('dashboard')



class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contact_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        # Delete related reminders as well
        self.object.reminder_set.all().delete()
        return super().delete(request, *args, **kwargs)

    success_url = reverse_lazy('dashboard')  # Pointing to the dashboard view in the auth_user app


