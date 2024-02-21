from django.shortcuts import render
from django.views.generic import TemplateView, View
from .core.file.utils import get_files_dir
from .core.storage import FileBackup
from .core.task import ScheduleFileBackupTask


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

    def post(self, request):
        data = request.POST
        locations = data.getlist('location', [])
        file_backups = []
        for location in locations:
            file_backups.append(FileBackup(location))
        # ScheduleFileBackupTask(file_backups, 10, 'seconds')
        ScheduleFileBackupTask([FileBackup('F:\\Project\\dj_backup\\src\\test\\1.txt.txt')], 5, 'seconds')

