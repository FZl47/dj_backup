# dj_backup

## What is this ?

    DJ Backup is a Django app that provides the capability to back up your files and databases.

### Available at:
- #### <a href="https://pypi.org/project/djbackup/">pypi</a>
- #### <a href="https://github.com/FZl47/dj_backup">github</a>


##### supported databases

- mysql
- postgres
- sqlite

##### supported storages

- local
- sftp server
- ftp server
- dropbox
- telegram bot

## How to use ?

####  1. First you need to install dj_backup

```sh
    pip install djbackup
```
OR
- #### for using all features
```sh
    pip install djbackup[all]
```

#### 2. After that, add the `dj_backup` app to your Django project's installed apps.

```pycon
    INSTALLED_APPS = [
    ...
    ...
    # apps
    'dj_backup',
]
```

#### 3. add static files dir path to django

```python
from dj_backup.core.utils.static import load_static

STATICFILES_DIRS = [
    ...
    load_static()
]

```

#### 4. add dj_backup urls to project urls

```python
urlpatterns = [
    ...
    path('dj-backup/', include('dj_backup.urls', namespace='dj_backup')),
    ...
]
```

#### 5. set dj_backup <span style="text-decoration: underline;">basic config</span> to django settings

```python

DJ_BACKUP_CONFIG = {
    'STORAGES': {
        'LOCAL': {
            'OUT': BASE_DIR / 'backup/result'
        },
    }
}

```

#### 6. migrate & collect static files

```python
    python manage.py migrate
```

```python
    python manage.py collectstatic
```

#### 7. run backup!

- command is for managing settings and executing backup tasks

```python
    python manage.py run-backup
```

### 8. run django

```python
    python manage.py runserver
```

- OR use wsgi/asgi handler like: (uwsgi, gunicorn, waitress or etc)

### Dashboard

#### now you can access to `dj_backup` dashboard

```djangourlpath
    127.0.0.1:8000/dj-backup/
```

OR

```djangourlpath
    xxx.xxx:xxxx/dj-backup/  
```

### Full Config

```python
# DJ_BACKUP_CONFIG = {
    # 'MAX_WORKERS': 5, #(optional)
    # 'NOTIFICATION_OBJECT_LOG_LEVEL': 'WARNING', #(optional)  # options => ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    # 'POSTGRESQL_DUMP_PATH': None,  # optional(If the postgresql dump file is not found, you can set it)
    # 'MYSQL_DUMP_PATH': None,  # optional(If the mysql dump file is not found, you can set it)
    # 'EXTERNAL_DATABASES': {
    # 'default2': {
    #     'ENGINE': 'postgresql',
    #     'NAME': 'test',
    #     'USER': 'postgres',
    #     'PASSWORD': 'xxx',
    #     'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
    # },
    # 'default3': {
    #     'ENGINE': 'mysql',
    #     'NAME': 'test',
    #     'USER': 'root',
    #     'PASSWORD': 'xxx',
    #     'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
    # },
    # },
    # 'BASE_ROOT_DIRS': [
        # BASE_DIR,
    # ],
    # 'BACKUP_TEMP_DIR': BASE_DIR / 'backup/temp', #(optional)
    # 'BACKUP_SYS_DIR': BASE_DIR / 'backup/sys', #(optional)
    # 'STORAGES': {
    #     'LOCAL': {
    #         'OUT': BASE_DIR / 'backup/result'
    #     },
        # 'TELEGRAM_BOT': {
        #     'BOT_TOKEN': 'xxx-xxx',
        #     'CHAT_ID': 'xxx-xxx'
        # }
        # 'SFTP_SERVER': {
        #     'HOST': 'xxx',
        #     'USERNAME': 'xxx',
        #     'PASSWORD': 'xxx',
        #     'OUT': 'xxx'
        # },
        # 'FTP_SERVER': {
        #     'HOST': "xxx",
        #     'USERNAME': "xxx",
        #     'PASSWORD': "xxx",
        #     'OUT': 'backups'
        # },
        # 'DROPBOX': {
        #     'APP_KEY': 'xxx-xxx',
        #     'OUT': '/dj_backup/'
        # }
    # }
# }
```

- ### <span style="text-decoration: underline;line-height:50px;">To use storage providers or perform database backups, you need to install the appropriate packages according to your needs using the commands below</span>

### - storages:

| storage      | install command                        |
|--------------|----------------------------------------| 
| TELEGRAM_BOT | ```pip install djbackup[telegram]```   |
| SFTP_SERVER  | ```pip install djbackup[sftpserver]``` |
| FTP_SERVER   | ```pip install djbackup[ftpserver]```  |
| DROPBOX      | ```pip install djbackup[dropbox]```    |


### - databases:

| database   | install command                        |
|------------|----------------------------------------| 
| mysql      | ```pip install djbackup[mysql]```      |
| postgresql | ```pip install djbackup[postgresql]``` |


## NOTE:

    If you dont need any of the storages, you must remove that configuration
    because you get an error if it cant be connected

