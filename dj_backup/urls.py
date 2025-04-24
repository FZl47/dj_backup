from django.urls import path
from . import views

app_name = 'dj_backup'
urlpatterns = [
    path('logout', views.Logout.as_view(), name='logout'),
    path('login', views.Login.as_view(), name='login'),

    path('', views.Index.as_view(), name='dashboard__index'),

    path('file/list', views.FileList.as_view(), name='file__list'),
    path('file/backup/add', views.FileBackupAdd.as_view(), name='file_backup__add'),

    path('db/list', views.DataBaseList.as_view(), name='db__list'),
    path('db/backup/add', views.DataBaseBackupAdd.as_view(), name='db_backup__add'),

    path('notif/list', views.NotificationList.as_view(), name='notification__list'),

    path('backup/list', views.BackupList.as_view(), name='backup__list'),
    path('backup/<int:backup_id>/detail', views.BackupDetail.as_view(), name='backup__detail'),
    path('backup/<int:backup_id>/delete', views.BackupDelete.as_view(), name='backup__delete'),
    path('backup/<int:backup_id>/update', views.BackupUpdate.as_view(), name='backup__update'),
    path('backup/<int:backup_id>/manage-running-status', views.BackupManageRunningStatus.as_view(),
         name='backup__manage_running_status'),

    path('backup/result/<int:backup_result_id>/download', views.DJBackupResultDownload.as_view(),
         name='backup__result_download'),

]
