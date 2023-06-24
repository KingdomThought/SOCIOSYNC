from django.conf import settings
import logging

logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
from contact_management.models import Reminder
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send reminders to users'

    def handle(self, *args, **options):
        unsent_reminders = Reminder.objects.filter(sent=False).order_by('date_time')

        for reminder in unsent_reminders:
            contact = reminder.contact

            if timezone.now() >= reminder.date_time:
                if reminder.position == 0:  # First reminder
                    email_content = f"It's time to contact {contact.name}! Remember, you planned to reach out to them regularly."
                else:  # Mid-cycle reminder
                    email_content = f"Just a reminder to contact {contact.name} soon."

                email = EmailMessage(
                    'Contact Reminder',
                    email_content,
                    'from_email@example.com',
                    [contact.user.email],
                )

                for i in range(3):
                    try:
                        email.send(fail_silently=False)
                        reminder.sent = True
                        reminder.save()

                        # Check if this is the last reminder of the cycle
                        if reminder.position == 1:
                            # If yes, create new reminders for the next cycle
                            contact.create_new_reminders()
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

            else:
                # Stop the loop as further reminders are not due yet because they are ordered by 'date_time'
                break
