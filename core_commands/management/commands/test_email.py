from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from core_commands.tasks import send_test_email_task, send_bulk_test_emails_task


class Command(BaseCommand):
    help = 'Send test emails using Celery tasks to verify email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            'recipient',
            nargs='?',
            type=str,
            help='Email address to send test email to'
        )
        
        parser.add_argument(
            '--bulk',
            nargs='+',
            type=str,
            help='Send test emails to multiple recipients (space-separated email addresses)'
        )
        
        parser.add_argument(
            '--subject',
            type=str,
            default=None,
            help='Custom subject for the test email'
        )
        
        parser.add_argument(
            '--message',
            type=str,
            default=None,
            help='Custom message for the test email'
        )
        
        parser.add_argument(
            '--sync',
            action='store_true',
            help='Send email synchronously without using Celery'
        )
        
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for Celery task to complete and show result'
        )

    def handle(self, *args, **options):
        # Validate email configuration
        self._validate_email_config()
        
        recipient = options.get('recipient')
        bulk_recipients = options.get('bulk')
        subject = options.get('subject')
        message = options.get('message')
        sync = options.get('sync', False)
        wait = options.get('wait', False)
        
        # Determine recipients
        if bulk_recipients:
            recipients = bulk_recipients
            self.stdout.write(f"Preparing to send test emails to {len(recipients)} recipients...")
        elif recipient:
            recipients = [recipient]
        else:
            raise CommandError("Please provide either a recipient email or use --bulk with multiple emails")
        
        # Validate email addresses
        for email in recipients:
            if not self._is_valid_email(email):
                raise CommandError(f"Invalid email address: {email}")
        
        if sync:
            # Send emails synchronously
            self._send_sync_emails(recipients, subject, message)
        else:
            # Send emails using Celery
            self._send_async_emails(recipients, subject, message, wait)

    def _validate_email_config(self):
        """Validate that email settings are properly configured"""
        if not settings.EMAIL_HOST_USER:
            raise CommandError("EMAIL_HOST_USER is not configured in settings")
        
        if not settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(
                self.style.WARNING("EMAIL_HOST_PASSWORD is not configured - emails may fail")
            )
        
        self.stdout.write(
            self.style.SUCCESS("Email configuration validated:")
        )
        self.stdout.write(f"  - Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"  - Port: {settings.EMAIL_PORT}")
        self.stdout.write(f"  - From: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"  - TLS: {settings.EMAIL_USE_TLS}")

    def _is_valid_email(self, email):
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _send_sync_emails(self, recipients, subject, message):
        """Send emails synchronously without Celery"""
        self.stdout.write("Sending emails synchronously...")
        
        for recipient in recipients:
            try:
                # Use default subject and message if not provided
                email_subject = subject or f"Test Email from {settings.DEFAULT_FROM_EMAIL}"
                email_message = message or f"""
This is a test email sent synchronously from your Django application.

Sent to: {recipient}
From: {settings.DEFAULT_FROM_EMAIL}

If you received this email, your email configuration is working correctly!

Best regards,
Your Django Application
"""
                
                result = send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                
                if result:
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Email sent successfully to {recipient}")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f"✗ Failed to send email to {recipient}")
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error sending email to {recipient}: {str(e)}")
                )

    def _send_async_emails(self, recipients, subject, message, wait):
        """Send emails using Celery tasks"""
        self.stdout.write("Sending emails using Celery tasks...")
        
        if len(recipients) == 1:
            # Single email
            recipient = recipients[0]
            try:
                task_result = send_test_email_task.delay(recipient, subject, message)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Email task queued for {recipient}")
                )
                self.stdout.write(f"  Task ID: {task_result.id}")
                
                if wait:
                    self.stdout.write("Waiting for task to complete...")
                    result = task_result.get(timeout=30)  # Wait up to 30 seconds
                    
                    if result['status'] == 'success':
                        self.stdout.write(
                            self.style.SUCCESS(f"✓ {result['message']}")
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(f"✗ {result['message']}")
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error queuing email task: {str(e)}")
                )
        else:
            # Bulk emails
            try:
                task_result = send_bulk_test_emails_task.delay(recipients, subject, message)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Bulk email task queued for {len(recipients)} recipients")
                )
                self.stdout.write(f"  Task ID: {task_result.id}")
                
                if wait:
                    self.stdout.write("Waiting for bulk task to complete...")
                    result = task_result.get(timeout=60)  # Wait up to 60 seconds
                    
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ {result['message']}")
                    )
                    
                    # Show individual task results
                    for task_info in result['results']:
                        self.stdout.write(f"  - {task_info['email']}: {task_info['status']} (Task: {task_info['task_id']})")
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Error queuing bulk email task: {str(e)}")
                )

        if not wait:
            self.stdout.write(
                self.style.WARNING(
                    "\nNote: Tasks are running in the background. "
                    "Use --wait to see results or check Celery logs for task status."
                )
            )
            self.stdout.write("You can also check task status in Django admin or Celery monitoring tools.")