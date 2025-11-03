import logging

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .models import CustomUser

logger = logging.getLogger(__name__)


def send_password_reset_email(email, user_id):
    logger.info(f"Отправка email для сброса пароля для {email}, user_id={user_id}")
    try:
        user = CustomUser.objects.get(pk=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{settings.SITE_URL}{reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

        subject = "Сброс пароля - Ride-Share"
        message = f"""
        Здравствуйте {user.first_name or user.email},

        Для сброса пароля перейдите по ссылке:
        {reset_url}

        С уважением,
        Ride-Share
        """
        html_message = f"""
        <h1>Сброс пароля</h1>
        <p>Здравствуйте {user.first_name or user.email},</p>
        <p>Для сброса пароля нажмите на ссылку:</p>
        <p><a href="{reset_url}">Сбросить пароль</a></p>
        <p>С уважением,<br>Ride-Share</p>
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        logger.info(f"Email отправлен на {email}")

    except Exception as e:
        logger.error(f"Ошибка отправки email на {email}: {str(e)}")
        raise
