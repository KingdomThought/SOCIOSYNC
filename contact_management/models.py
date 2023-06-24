from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Contact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Business', 'Business'),
        ('Friend', 'Friend'),
        ('Worker', 'Worker'),
    ]

    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Bi-weekly', 'Bi-weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Bi-annual', 'Bi-annual'),
        ('Annual', 'Annual'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relationship = models.CharField(choices=RELATIONSHIP_CHOICES, max_length=10)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, max_length=10)
    next_reminder = models.DateTimeField()

    def __str__(self):
        return f"{self.name} ({self.relationship})"

    def get_frequency_delta(self):
        if self.frequency == 'Daily':
            return relativedelta(days=1)
        elif self.frequency == 'Weekly':
            return relativedelta(weeks=1)
        elif self.frequency == 'Bi-weekly':
            return relativedelta(weeks=2)
        elif self.frequency == 'Monthly':
            return relativedelta(months=1)
        elif self.frequency == 'Quarterly':
            return relativedelta(months=3)
        elif self.frequency == 'Bi-annual':
            return relativedelta(months=6)
        elif self.frequency == 'Annual':
            return relativedelta(years=1)
        else:
            return None

    def create_new_reminders(self):
        # Get frequency delta
        delta = self.get_frequency_delta()

        if delta is None:
            return

        now = timezone.now()

        reminders = []
        reminders.append(Reminder(
            contact=self,
            date_time=now,  # Set first reminder at the moment of creation
            position=0,
        ))

        # Calculate the exact midpoint
        if self.frequency in ['Daily', 'Weekly', 'Bi-weekly']:
            mid_cycle = now + delta / 2
        else:
            # For other frequencies, we calculate the exact midpoint
            end_cycle = now + delta
            mid_cycle = now + (end_cycle - now) / 2

        reminders.append(Reminder(
            contact=self,
            date_time=mid_cycle,  # Set second reminder at the calculated mid point of the cycle
            position=1,
        ))

        self.next_reminder = min(r.date_time for r in reminders)

        # Save the reminder objects
        for reminder in reminders:
            reminder.save()


class Reminder(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    position = models.IntegerField(null=False)

    def __str__(self):
        return f"Reminder for {self.contact.name} on {self.date_time}"

    def send(self):
        # Check if the reminder is already sent
        if self.sent:
            print(f'Reminder {self.id} has already been sent. Skipping.')
            return

        # Check if it's time to send the reminder
        if timezone.now() >= self.date_time:
            print(f'Sending reminder {self.position} for {self.contact.name}')  # Debug print

            # Here goes your logic for sending the reminder.
            # This could be sending an email, a text message, etc.

            # Mark the reminder as sent
            self.sent = True
            self.save()
        else:
            print(f"It's not time yet to send reminder {self.position} for {self.contact.name}. Skipping.")


def send_reminders():
    # Get all unsent reminders
    unsent_reminders = Reminder.objects.filter(sent=False).order_by('date_time')
    for reminder in unsent_reminders:
        # Check if it's time to send the reminder
        if timezone.now() >= reminder.date_time:
            reminder.send()
        else:
            # Stop the loop as further reminders are not due yet because they are ordered by 'date_time'
            break
