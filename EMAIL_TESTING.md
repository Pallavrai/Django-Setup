# Email Testing Command

This Django management command allows you to test your email configuration using Celery tasks.

## Prerequisites

1. **Email Configuration**: Ensure your email settings are properly configured in `django.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

2. **Celery Setup**: Make sure Redis is running and Celery is configured:
   ```
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```

3. **Start Celery Worker**: In a separate terminal, run:
   ```bash
   celery -A config worker --loglevel=info
   ```

## Usage Examples

### 1. Send a single test email (asynchronous with Celery)
```bash
python manage.py test_email recipient@example.com
```

### 2. Send a single test email and wait for completion
```bash
python manage.py test_email recipient@example.com --wait
```

### 3. Send test emails to multiple recipients
```bash
python manage.py test_email --bulk email1@example.com email2@example.com email3@example.com
```

### 4. Send test email with custom subject and message
```bash
python manage.py test_email recipient@example.com --subject "Custom Test Subject" --message "This is a custom test message."
```

### 5. Send email synchronously (without Celery)
```bash
python manage.py test_email recipient@example.com --sync
```

### 6. Bulk emails with custom content and wait for completion
```bash
python manage.py test_email --bulk email1@example.com email2@example.com --subject "Bulk Test" --message "Testing bulk emails" --wait
```

## Command Options

- `recipient`: Single email address to send test email to
- `--bulk`: Send test emails to multiple recipients (space-separated)
- `--subject`: Custom subject for the test email
- `--message`: Custom message for the test email
- `--sync`: Send email synchronously without using Celery
- `--wait`: Wait for Celery task to complete and show result

## Features

1. **Email Validation**: Validates email addresses before sending
2. **Configuration Check**: Verifies email settings are properly configured
3. **Async and Sync Options**: Choose between Celery tasks or synchronous sending
4. **Bulk Email Support**: Send to multiple recipients at once
5. **Custom Content**: Override default subject and message
6. **Task Monitoring**: Option to wait for task completion and see results
7. **Error Handling**: Comprehensive error handling with retry logic
8. **Logging**: Detailed logging for debugging

## Celery Tasks

The command uses two main Celery tasks:

1. **`send_test_email_task`**: Sends a single test email with retry logic
2. **`send_bulk_test_emails_task`**: Queues multiple individual email tasks

## Monitoring

- Use `--wait` flag to see immediate results
- Check Celery logs for detailed task execution information
- Monitor task status through Celery monitoring tools like Flower
- View task results in Django admin (if configured)

## Troubleshooting

1. **Email not sending**: Check email configuration and credentials
2. **Celery tasks not executing**: Ensure Redis is running and Celery worker is started
3. **Permission errors**: Verify email account allows app passwords (for Gmail)
4. **Timeout errors**: Increase timeout values or check network connectivity

## Development

The email testing functionality is split into:
- `/core_commands/tasks.py`: Celery task definitions
- `/core_commands/management/commands/test_email.py`: Django management command
- Email configuration in `config/settings.py`
