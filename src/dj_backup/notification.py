from dj_backup.core.task import Task
from dj_backup.core.triggers import TriggerLogBase
from dj_backup import settings

from .models.notification import DJBackupLog, DJBackupLogLevel


class TriggerLogNotification(TriggerLogBase):
    is_email_configured = settings.is_email_configured

    @staticmethod
    def handler_send_mail(log_obj, level_n):
        log_level_emails = DJBackupLogLevel.objects.filter(level_n__lte=level_n, is_active=True)
        for log_level_email in log_level_emails:
            log_level_email.send_mail(log_obj)

    def log(self, level, level_n, msg, exc, *args, **kwargs):
        log = DJBackupLog.objects.create(
            level=level,
            msg=msg,
            exc=exc,
        )
        if not self.is_email_configured:
            return
        t = Task(self.handler_send_mail, f_args=(log, level_n))
        t.run()
