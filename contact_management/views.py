from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from contact_management.models import Contact, Reminder
from contact_management.forms import ContactForm, ReminderForm
from django.utils import timezone
from dateutil.relativedelta import relativedelta


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from dateutil.relativedelta import relativedelta
from datetime import timedelta

class AddNewContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)

        contact = self.object
        delta = contact.get_frequency_delta()

        if delta is None:
            return super().form_valid(form)

        now = timezone.now()

        reminders = []
        reminders.append(Reminder(
            contact=contact,
            date_time=now,  # Set first reminder at the moment of creation
            position=0,
        ))

        # Calculate the exact midpoint
        if contact.frequency in ['Daily', 'Weekly', 'Bi-weekly']:
            mid_cycle = now + delta / 2
        else:
            # For other frequencies, we calculate the exact midpoint
            end_cycle = now + delta
            mid_cycle = now + (end_cycle - now) / 2

        reminders.append(Reminder(
            contact=contact,
            date_time=mid_cycle,  # Set second reminder at the calculated mid point of the cycle
            position=1,
        ))

        contact.next_reminder = min(r.date_time for r in reminders)

        self.object.save()

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

        now = timezone.now()

        reminders = []
        reminders.append(Reminder(
            contact=contact,
            date_time=now,  # Set first reminder at the moment of update
            position=0,
        ))

        # Calculate the exact midpoint
        if contact.frequency in ['Daily', 'Weekly', 'Bi-weekly']:
            mid_cycle = now + delta / 2
        else:
            # For other frequencies, we calculate the exact midpoint
            end_cycle = now + delta
            mid_cycle = now + (end_cycle - now) / 2

        reminders.append(Reminder(
            contact=contact,
            date_time=mid_cycle,  # Set second reminder at the calculated mid point of the cycle
            position=1,
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