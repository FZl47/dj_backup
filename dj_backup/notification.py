from django_q.tasks import async_task

from dj_backup.core.triggers import TriggerLogBase
from dj_backup import settings

from .models.notification import DJBackupLog, DJBackupLogLevel


class TriggerLogNotification(TriggerLogBase):

    def log(self, level, level_n, msg, exc, *args, **kwargs):
        log = DJBackupLog.objects.create(
            level=level,
            msg=msg,
            exc=exc,
        )
        if not settings.is_email_configured:
            return
        log_level_emails = DJBackupLogLevel.objects.filter(level_n__lte=level_n, is_active=True)
        for log_email in log_level_emails:
            async_task(log_email.send_mail, log=log)
