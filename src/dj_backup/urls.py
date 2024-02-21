from django.urls import path
from . import views

app_name = 'dj_backup'
urlpatterns = [
    path('dashboard', views.Index.as_view(), name='dashboard__index'),
    path('dashboard/file/list', views.FileList.as_view(), name='file__list'),
    path('dashboard/file/backup/add', views.FileBackupAdd.as_view(), name='file_backup__add'),
]
