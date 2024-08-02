from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib import messages

from dj_backup.core.utils import get_files_dir, get_file_name
from dj_backup.core.backup.file import FileBackup
from dj_backup.core.tasks import ScheduleFileBackupTask
from dj_backup.core import storages
from dj_backup import models, forms


class Index(TemplateView):
    template_name = 'dj_backup/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context


class FileList(TemplateView):
    template_name = 'dj_backup/file/list.html'

    def get_context_data(self, **kwargs):
        # TODO: should be restrict dir locations(prevent security bugs and access)
        context = super(FileList, self).get_context_data(**kwargs)
        dir_location = self.request.GET.get('dir')
        files = get_files_dir(dir_location)
        context.update({
            'files': files
        })
        return context


class FileBackupAdd(View):
    form = forms.DJFileBackUpForm

    def get_referrer_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST
        f_backup = self.form(data)
        if not f_backup.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_referrer_url())
        backup = f_backup.save()
        file_dirs = data.getlist('file_dirs', [])
        if not file_dirs:
            messages.error(request, _('You should set file to backup'))
            return redirect(self.get_referrer_url())
        # create file objs
        for file_dir in file_dirs:
            f = forms.DJFileForm({
                'backup': backup,
                'dir': file_dir,
                'name': get_file_name(file_dir)
            })
            if not f.is_valid():
                # TODO: log exception | refactor
                messages.error(request, _('Something went wrong in file object creation'))
                backup.delete()
                return redirect(self.get_referrer_url())
            f.save()
        fb = FileBackup(backup)
        file_path = fb.save_temp()
        # ScheduleFileBackupTask(backup)
        for storage in storages.STORAGES_AVAILABLE:
            storage(file_path).save()
        fb.delete_temp()
        messages.success(request, _('Backup file submited successfully'))
        return redirect(self.get_referrer_url())


class Test(View):

    def get(self, request):
        from .core.backup.db import base
        base.MysqlDB().dump()
