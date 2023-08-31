from celery import shared_task
import logging

logger = logging.getLogger(__name__)
from django.core.mail import send_mail, EmailMessage
from .models import Contact, Reminder
from django.utils import timezone
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_reminders_task():
    reminders_for_today = Reminder.objects.filter(date_time__date=timezone.now().date(), sent=False).select_related('contact')

    for reminder in reminders_for_today:
        contact = reminder.contact
        reminder_position = reminder.position

        if reminder_position == 0:  # First reminder
            email_content = f"It's time to contact {contact.name}! Remember, you planned to reach out to them regularly."
        elif reminder_position == 1:  # Second reminder
            email_content = f"Just a reminder to contact {contact.name} soon."

        email = EmailMessage(
            'Contact Reminder',
            email_content,
            'dinnallenterprise@yahoo.com',
            [contact.user.email]
        )

        print(contact.user.email)

        for i in range(3):
            try:
                email.send(fail_silently=False)
                reminder.sent = True
                reminder.save()
                break
            except Exception as e:
                logger.error(f"Attempt {i + 1} failed to send email for contact {contact.id}: {e}")
                if i == 2:
                    try:
                        send_mail(
                            'Failed to Send Reminder Email',
                            f"Failed to send email for contact {contact.id} after 3 attempts: {e}",
                            'error@example.com',
                            [settings.ADMIN_EMAIL],
                            fail_silently=True,
                        )
                    except:
                        logger.error(f"Failed to send error email to admin for contact {contact.id}: {e}")

def reset_reminders(contact):
    delta = contact.get_frequency_delta()
    now = timezone.now()
    reminders = []

    reminders.append(Reminder(
        contact=contact,
        date_time=now + delta,  # Set first reminder at the end of current cycle
        position=0,
    ))

    # Calculate the exact midpoint
    if contact.frequency in ['Daily', 'Weekly', 'Bi-weekly']:
        mid_cycle = now + delta + delta / 2
    else:
        # For other frequencies, we calculate the exact midpoint
        end_cycle = now + delta * 2
        mid_cycle = now + delta + (end_cycle - now - delta) / 2

    reminders.append(Reminder(
        contact=contact,
        date_time=mid_cycle,  # Set second reminder at the calculated mid point of the cycle
        position=1,
    ))

    # Save the new reminders
    for reminder in reminders:
        reminder.save()
