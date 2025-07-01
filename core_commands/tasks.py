from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, retry_delay=60, max_retries=3)
def send_test_email_task(self, recipient_email, subject=None, message=None):
    """
    Celery task to send a test email.
    
    Args:
        recipient_email (str): Email address to send the test email to
        subject (str, optional): Email subject. Defaults to a test subject.
        message (str, optional): Email message. Defaults to a test message.
    
    Returns:
        dict: Status information about the email sending attempt
    """
    try:
        # Default subject and message if not provided
        if not subject:
            subject = f"Test Email from {settings.DEFAULT_FROM_EMAIL}"
        
        if not message:
            message = f"""
                        This is a test email sent from your Django application using Celery.

                        Task ID: {self.request.id}
                        Sent at: {self.request.eta or 'immediately'}
                        From: {settings.DEFAULT_FROM_EMAIL}
                        To: {recipient_email}

                        If you received this email, your email configuration is working correctly!

                        Best regards,
                        Your Django Application
                        """

        # Send the email
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        if result:
            logger.info(f"Test email sent successfully to {recipient_email}")
            return {
                'status': 'success',
                'message': f'Test email sent successfully to {recipient_email}',
                'task_id': self.request.id,
                'recipient': recipient_email
            }
        else:
            logger.error(f"Failed to send test email to {recipient_email}")
            return {
                'status': 'error',
                'message': f'Failed to send test email to {recipient_email}',
                'task_id': self.request.id,
                'recipient': recipient_email
            }
            
    except Exception as exc:
        logger.error(f"Error sending test email to {recipient_email}: {str(exc)}")
        
        # Retry the task if it's a temporary failure
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            return {
                'status': 'failed',
                'message': f'Failed to send test email after maximum retries: {str(exc)}',
                'task_id': self.request.id,
                'recipient': recipient_email
            }


@shared_task
def send_bulk_test_emails_task(recipient_emails, subject=None, message=None):
    """
    Celery task to send test emails to multiple recipients.
    
    Args:
        recipient_emails (list): List of email addresses
        subject (str, optional): Email subject
        message (str, optional): Email message
    
    Returns:
        dict: Summary of bulk email sending results
    """
    results = []
    
    for email in recipient_emails:
        # Queue individual email tasks
        task_result = send_test_email_task.delay(email, subject, message)
        results.append({
            'email': email,
            'task_id': task_result.id,
            'status': 'queued'
        })
    
    return {
        'status': 'bulk_queued',
        'message': f'Queued {len(recipient_emails)} test emails',
        'total_emails': len(recipient_emails),
        'results': results
    }
