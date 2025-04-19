# dj_backup

## What is this ?

    DJ Backup is a Django app that provides the capability to back up your files and databases.

##### supported databases

- mysql
- postgres
- sqlite

## How to use ?

1. First you need to install dj_backup

```sh
    pip install djbackup
```

#### 2. After that, add the `dj_backup` and `django_q` apps to your Django project's installed apps.

```pycon
    INSTALLED_APPS = [
    ...
    ...
    # apps
    'dj_backup',
    'django_q'
]
```

3. add static files dir path to django

```python
STATICFILES_DIRS = (
    ...
    os.path.join(BASE_DIR, 'dj_backup/static/'),
)

```

4. add locale file to django(`optional`)

```python
LOCALE_PATHS = (
    ...
    BASE_DIR/ 'dj_backup/locale',
)
```

5. dj_backup urls to django urls

```python
urlpatterns = [
    ...
    path('dj-backup/', include('dj_backup.urls', namespace='dj_backup')),
    ...
]
```

### 6. set dj_backup config to django settings

```python
    DJ_BACKUP_CONFIG = {
    # optional (if dj_backup cant find `pg_dump` file then you must fill this
    'POSTGRESQL_DUMP_PATH': None,
    # optional (if dj_backup cant find `mysqldump` file then you must fill this
    'MYSQL_DUMP_PATH': None,
    # if you want backup external databases you can set this config
    # By default local databases are accessible and can be backed up
    'EXTERNAL_DATABASES': {
        # 'external_db': {
        #     'ENGINE': 'mysql',
        #     'NAME': 'test',
        #     'USER': 'test',
        #     'PASSWORD': 'test',
        #     'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        #     'PORT': 3306  # optional
        # },
        ...
        ...
    },
    'BASE_ROOT_DIRS': [
        # the main path for the files that need to be backed up
        BASE_DIR,
        ...
    ],
    'BACKUP_TEMP_DIR': BASE_DIR / 'backup/temp',
    'STORAGES': {
        'LOCAL': {
            'OUT': BASE_DIR / 'backup/result'  # the path local storage
        },
        'SFTP_SERVER': {
            'HOST': 'xxx.xxx.xxx.xxx',
            'USERNAME': 'xxx.xxx.xxx.xxx',
            'PASSWORD': 'xxx.xxx.xxx.xxx',
            'OUT': '/backups'
        },
        'FTP_SERVER': {
            'HOST': "xxx.xxx.xxx.xxx",
            'USERNAME': "xxx.xxx.xxx.xxx",
            'PASSWORD': "xxx.xxx.xxx.xxx",
            'OUT': '/backups'
        },
        'DROPBOX': {
            'ACCESS_TOKEN': 'xxx.xxx.xxx.xxx',
            'OUT': '/backups'
        }
    }
}

```

### 7. migrate & collect static files

```python
    python
manage.py
migrate
```

```python
    python
manage.py
collectstatic
```

### 8. run backup!

```python
    python
manage.py
run - backup
```

### 9. Dashboard

#### now you can access to `dj_backup` dashboard

```djangourlpath
    127.0.0.1:8000/dj-backup/
```

OR

```djangourlpath
    xxx.xxx:xxxx/dj-backup/  
```

## NOTE:

    If you dont need any of the storages, you must remove that configuration
    because you get an error if it cant be connected

### TODO:

[ ] complete code TODO

[x] fix access direction in list files(prevent access to out of base dirs)

[x] add update/delete backup object

[x] add storages in dashboard

[x] add user required mixin views

[x] add ftp server storage

[x] add sftp server storage

[x] add drop box storage

#### Update TODO:

[x] add external databases

[x] add postgresql db backup

[ ] add google cloud and aws S3 storages

[ ] add notification(email)

[/] add storages free space

[ ] add schedule task for clear temp files

[ ] add object logs

[x] use local file instead temp files if not available to download

[x] * change structure load and initial storages

[x] add time taken to generate and store backup

[ ] * use pure schedule library or apscheduler or etc. instead django_q(has problems)

[ ] add password for backups

[x] add telegram storage
