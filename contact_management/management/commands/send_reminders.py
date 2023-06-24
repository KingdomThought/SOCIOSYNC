
from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from contact_management.models import Contact, Reminder
from django.utils import timezone
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send reminders to users'

    def handle(self, *args, **options):
        reminders_for_today = Reminder.objects.filter(date_time__date=timezone.now().date(), sent=False).select_related('contact')

        for reminder in reminders_for_today:
            contact = reminder.contact
            reminder_position = reminder.position

            if reminder_position == 0:  # First reminder
                email_content = f"It's time to contact {contact.name}! Remember, you planned to reach out to them regularly."
            elif reminder_position == 1:  # Second reminder
                email_content = f"Just a reminder to contact {contact.name} soon."
            else:  # Third reminder
                email_content = f"Final reminder: don't forget to contact {contact.name} as you planned."

            email = EmailMessage(
                'Contact Reminder',
                email_content,
                'from_email@example.com',
                [contact.user.email]
            )

            for i in range(3):
                try:
                    email.send(fail_silently=False)
                    reminder.sent = True
                    reminder.save()
                    break
                except Exception as e:
                    logger.error(f"Attempt {i+1} failed to send email for contact {contact.id}: {e}")
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