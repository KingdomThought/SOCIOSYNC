from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth import get_user_model


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


class Reminder(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    position = models.IntegerField(null=False)

    def __str__(self):
        return f"Reminder for {self.contact.name} on {self.date_time}"
