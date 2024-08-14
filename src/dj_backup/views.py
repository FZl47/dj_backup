from itertools import chain

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import redirect, Http404
from django.contrib import messages
from django.contrib.auth import logout as logout_django
from django.http import HttpResponse

from dj_backup.core.utils import get_files_dir, get_file_name
from dj_backup.core.backup.db import DATABASES_AVAILABLE
from dj_backup.core import tasks
from dj_backup import models, forms
from dj_backup import settings


class Login(TemplateView):
    pass


class Logout(View):

    def get(self, request):
        logout_django(request)
        return redirect('')


class Index(TemplateView):
    template_name = 'dj_backup/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['storages'] = models.DJStorage.objects.all()
        context['file_backups'] = models.DJFileBackUp.objects.all()
        context['db_backups'] = models.DJDataBaseBackUp.objects.all()
        return context


class FileList(TemplateView):
    template_name = 'dj_backup/file/list.html'

    def get_context_data(self, **kwargs):
        # TODO: should be restrict dir locations(prevent security bugs and access)
        context = super(FileList, self).get_context_data(**kwargs)
        dir_location = self.request.GET.get('dir')
        if dir_location:
            dir_location = [dir_location]
        else:
            dir_location = settings.get_base_root_dirs()
        files_iter = get_files_dir(*dir_location)
        context.update({
            'files_iter': files_iter,
            'storages': models.DJStorage.objects.all()
        })
        return context


class FileBackupAdd(View):
    form = forms.DJFileBackUpForm
    form_file = forms.DJFileForm

    def get_referrer_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        # TODO: refactor this shit
        data = request.POST.copy()
        file_dirs = data.getlist('file_dirs', [])
        if not file_dirs:
            messages.error(request, _('You should set file to backup'))
            return redirect(self.get_referrer_url())
        # create file objs
        file_objects = []
        for file_dir in file_dirs:
            f = self.form_file({
                'dir': file_dir,
                'name': get_file_name(file_dir)
            })
            if not f.is_valid():
                # TODO: log exception
                messages.error(request, _('Something went wrong in file object creation'))
                return redirect(self.get_referrer_url())
            file_obj = f.save()
            file_objects.append(file_obj.id)
        data.setlist('files', file_objects)
        f_backup = self.form(data)
        if not f_backup.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_referrer_url())
        backup = f_backup.save()
        tasks.ScheduleFileBackupTask(backup)
        messages.success(request, _('Backup file submited successfully'))
        return redirect(self.get_referrer_url())


class DataBaseList(TemplateView):
    template_name = 'dj_backup/db/list.html'

    def get_context_data(self, **kwargs):
        context = super(DataBaseList, self).get_context_data(**kwargs)
        context.update({
            'databases': DATABASES_AVAILABLE,
            'storages': models.DJStorage.objects.all()
        })
        return context


class DataBaseBackupAdd(View):
    form = forms.DJDataBaseBackUpForm

    def get_referrer_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        additional_args = '|'.join(data.getlist('additional_args', []))
        data['additional_args'] = additional_args
        f = self.form(data)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_referrer_url())
        backup = f.save()
        tasks.ScheduleDataBaseBackupTask(backup)
        messages.success(request, _('Backup database submited successfully'))
        return redirect(self.get_referrer_url())


class BackupList(ListView):
    template_name = 'dj_backup/backup/list.html'
    paginate_by = 20

    def search(self, objects):
        search = self.request.GET.get('search')
        if not search:
            return objects
        objects = objects.filter(name__icontains=search)
        return objects

    def get_queryset(self):
        backup_dbs = self.search(models.DJDataBaseBackUp.objects.all())
        backup_files = self.search(models.DJFileBackUp.objects.all())
        qs = list(chain(backup_dbs, backup_files))
        return qs


class BackupDetail(TemplateView):
    template_name = 'dj_backup/backup/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        backup_id = kwargs.get('backup_id')
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        context['backup'] = backup
        backup_storages = backup.get_storages()
        for storage in backup_storages:
            storage.usage_size = backup.get_usage_size_by_storage(storage)
            storage.count_backup = backup.get_count_backup_storage(storage)
        context['backup_storages'] = backup_storages
        context['all_storages'] = models.DJStorage.objects.all()

        return context


class BackupDelete(View):

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        backup.delete()
        messages.success(request, _('Backup deleted successfully'))
        return redirect('dj_backup:backup__list')


class BackupUpdate(View):

    def get_form(self, backup):
        data = self.request.POST
        if backup.backup_type == 'database':
            return forms.DJDataBaseBackUpUpdateForm(data, instance=backup)
        else:
            return forms.DJFileBackUpUpdateForm(data, instance=backup)

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404

        f = self.get_form(backup)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(backup.get_absolute_url())
        backup = f.save()
        # delete old schedule task
        if backup.schedule_task:
            backup.schedule_task.delete()
            # create new task
            tasks.ScheduleFileBackupTask(backup)
        messages.success(request, _('Backup updated successfully'))
        return redirect(backup.get_absolute_url())


class BackupManageRunningStatus(View):

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        data = request.POST
        status = data.get('status')
        if not status:
            messages.error(request, _('Field status is required'))
            return redirect(backup.get_absolute_url())

        if backup.schedule_task:
            # delete schedule task
            backup.schedule_task.delete()

        if status == 'start':
            if backup.backup_type == 'file':
                tasks.ScheduleFileBackupTask(backup)
            else:
                tasks.ScheduleDataBaseBackupTask(backup)
            messages.success(request, _('Backup status changed to running'))
        else:
            messages.success(request, _('Backup status changed to stopped'))
        return redirect(backup.get_absolute_url())


class DJBackupResultDownload(View):

    def get(self, request, backup_result_id):
        try:
            br = models.DJBackUpStorageResult.objects.get(id=backup_result_id)
        except (models.DJBackUpStorageResult.DoesNotExist, models.DJBackUpStorageResult.MultipleObjectsReturned):
            raise Http404
        if not br.has_temp_file:
            raise Http404
        with open(br.temp_location, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={br.backup_name}'
            return response



