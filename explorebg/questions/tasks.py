from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(user_email, code):
    send_mail(
        'Your Explore Bulgaria Quiz Code',
        f"Hi there!\n\nThank you for participating in the Explore Bulgaria Quiz. Your unique code is: {code}\n\nBest of luck, and we hope you enjoy the quiz experience!\n\nCheers,\nThe Explore Bulgaria Quiz Team",
        "explorebg.quiz@gmail.com",
        [user_email],
        fail_silently=False
    )
