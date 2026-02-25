from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(username):
    # In a real app this would send an actual email
    # For now we'll just simulate it with a delay
    import time
    time.sleep(3)  # simulate slow email sending
    logger.info(f'Welcome email sent to {username}')
    return f'Email sent to {username}'