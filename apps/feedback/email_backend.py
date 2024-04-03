from django.core.mail.backends.smtp import *
from .models import LoggingEmail
from django.core.mail.message import sanitize_address
from django.conf import settings
import smtplib


class LoggingEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        for email in email_messages:
            email_record = LoggingEmail.objects.create(
                to="; ".join(email.recipients()),
                subject=email.subject
            )
            try:
                # Открываем подключение к сервису
                super().open()
                errors = self._send(email)
                # Не забыть закрыть соединение
                super().close()
                email_record.ok = True
                email_record.result = str(errors)
            except Exception as error:
                email_record.set_error_body(error)
                email_record.ok = False
            finally:
                email_record.save()

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
        message = email_message.message()
        try:
            errors_dict = self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
            return errors_dict
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            return False
