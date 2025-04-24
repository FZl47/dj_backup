from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class DJBackupLog(models.Model):
    level = models.CharField(max_length=10)
    msg = models.TextField(null=True, blank=True)
    exc = models.TextField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.level} - {self.exc[:10]}'

    @property
    def subject(self):
        return _('DJBackup Log')

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')


class DJBackupLogLevel(models.Model):
    level_n = models.IntegerField(default=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email} / {self.level_n}'

    def send_mail(self, log: DJBackupLog):
        context = {
            'msg': log.msg,
            'exc': log.exc,
            'level': log.level,
        }
        html_content = render_to_string('dj_backup/notification/log-mail.html', context)
        send_mail(log.subject, log.msg, settings.EMAIL_HOST_USER, [self.email], html_message=html_content)
