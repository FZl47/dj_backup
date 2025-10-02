# dj_backup

![DJ Backup Logo](https://raw.githubusercontent.com/FZl47/dj_backup/main/dj_backup/static/dj_backup/assets/images/logo.png)

## What is this ?
#### DJ Backup is a Django app that provides the capability to back up your files and databases.

[![PyPI version](https://img.shields.io/pypi/v/djbackup.svg)](https://pypi.org/project/djbackup/) [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![Django](https://img.shields.io/badge/django-3.2%2B-green)](https://www.djangoproject.com/) [![Documentation](https://img.shields.io/badge/docs-readthedocs-blue)](https://djbackup.readthedocs.io/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/FZl47/dj_backup/blob/main/LICENSE) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage](https://img.shields.io/badge/coverage-90%25-green)](https://github.com/FZl47/dj_backup) [![PyPI Downloads](https://static.pepy.tech/personalized-badge/djbackup?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/djbackup)



## Overview

`DJ Backup` is a powerful and flexible Django application designed to automate and manage backups for your project files and databases. With support for multiple storage providers and databases, it’s an essential tool for developers and system administrators looking to ensure data safety.


### Links
- [PyPI Package](https://pypi.org/project/djbackup/)
- [GitHub Repository](https://github.com/FZl47/dj_backup)
- [Documentation](https://djbackup.readthedocs.io/)
- [Issue Tracker](https://github.com/FZl47/dj_backup/issues)


## Key Features

- **Multiple Database Support**: Backup MySQL, PostgreSQL, and SQLite databases effortlessly.
- **Flexible Storage Options**: Store backups locally or on remote services like SFTP, FTP, Dropbox, or Telegram Bot.
- **Web Dashboard**: Intuitive interface to manage and monitor backup tasks.
- **Highly Configurable**: Customize backup directories, storage locations, and logging levels.
- **Lightweight & Modular**: Install only the dependencies you need for your setup.
- **Open Source**: Licensed under MIT, with a welcoming community for contributions.

## Supported Databases
- MySQL
- PostgreSQL
- SQLite

## Supported Storage Providers
- Local
- SFTP Server
- FTP Server
- Dropbox
- Telegram Bot

## Installation

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher


### How to use?(Step-by-Step Guide)

1. **Install DJ Backup**
   ```bash
   pip install djbackup
   ```
   To include all optional features (databases and storages):
   ```bash
   pip install djbackup[all]
   ```

2. **Add `dj_backup` to `INSTALLED_APPS`**
   ```python
   # settings.py
   
   INSTALLED_APPS = [
       # Other apps
       'dj_backup',
   ]
   ```

3. **Configure Static Files**
   ```python
   # settings.py
   
   from dj_backup.core.utils.static import load_static

   STATICFILES_DIRS = [
       # Other static directories
       load_static(),
   ]
   ```

4. **Add DJ Backup URLs**
   ```python
   # urls.py
   
   from django.urls import include, path

   urlpatterns = [
       # Other URLs
       path('dj-backup/', include('dj_backup.urls', namespace='dj_backup')),
   ]
   ```

5. **Set Up Basic Configuration**
   ```python
   # settings.py
   
   DJ_BACKUP_CONFIG = {
       'STORAGES': {
           'LOCAL': {
               'OUT': BASE_DIR / 'backup/result'
           },
       }
   }
   ```

6. **Run Migrate and Collect Static Files**
   ```bash
   # cmd
   python manage.py migrate
   python manage.py collectstatic
   ```

7. **Execute Backup**
   ```bash
   # cmd
   python manage.py run-backup
   ```

8. **Start the Django Server**
   ```bash
   # cmd
   python manage.py runserver
   ```
   **Note**: For production, use a WSGI/ASGI server like Gunicorn or uWSGI instead of `runserver`.



### Access the Dashboard
Navigate to:
```
http://127.0.0.1:8000/dj-backup/
```
Or your custom domain:
```
http://your-domain:port/dj-backup/
```

## Advanced Configuration

A complete example of `DJ_BACKUP_CONFIG`:

```python
# settings.py

DJ_BACKUP_CONFIG = {
    'MAX_WORKERS': 5,  # Maximum concurrent backup tasks
    'NOTIFICATION_OBJECT_LOG_LEVEL': 'WARNING',  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'POSTGRESQL_DUMP_PATH': None,  # Path to PostgreSQL dump executable (if needed)
    'MYSQL_DUMP_PATH': None,  # Path to MySQL dump executable (if needed)
    # External databases(Optional)
    'EXTERNAL_DATABASES': {
        'default2': {
            'ENGINE': 'postgresql',
            'NAME': 'test_db',
            'USER': 'postgres',
            'PASSWORD': 'your_password',
            'HOST': '127.0.0.1',
        },
        'default3': {
            'ENGINE': 'mysql',
            'NAME': 'test_db',
            'USER': 'root',
            'PASSWORD': 'your_password',
            'HOST': '127.0.0.1',
        },
    },
    'BASE_ROOT_DIRS': [BASE_DIR],  # Directories to include in backups
    'BACKUP_TEMP_DIR': BASE_DIR / 'backup/temp',  # Temporary backup storage
    'BACKUP_SYS_DIR': BASE_DIR / 'backup/sys',  # System backup storage
    'STORAGES': {
        'LOCAL': {
            'OUT': BASE_DIR / 'backup/result'
        },
        'TELEGRAM_BOT': {
            'BOT_TOKEN': 'your_bot_token',
            'CHAT_ID': 'your_chat_id'
        },
        'SFTP_SERVER': {
            'HOST': 'sftp.example.com',
            'USERNAME': 'your_username',
            'PASSWORD': 'your_password',
            'OUT': 'backups'
        },
        'FTP_SERVER': {
            'HOST': 'ftp.example.com',
            'USERNAME': 'your_username',
            'PASSWORD': 'your_password',
            'OUT': 'backups'
        },
        'DROPBOX': {
            'APP_KEY': 'your_app_key',
            'OUT': '/dj_backup/'
        }
    }
}
```


## Additional Dependencies

Install specific dependencies for your needs:

### Storage Providers
| Provider      | Install Command                     |
|---------------|-------------------------------------|
| Telegram Bot  | `pip install djbackup[telegram]`   |
| SFTP Server   | `pip install djbackup[sftpserver]` |
| FTP Server    | `pip install djbackup[ftpserver]`  |
| Dropbox       | `pip install djbackup[dropbox]`    |

### Databases
| Database     | Install Command                     |
|--------------|-------------------------------------|
| MySQL        | `pip install djbackup[mysql]`      |
| PostgreSQL   | `pip install djbackup[postgresql]` |



## Notes
- Remove unused storage configurations to prevent connection errors.
- Specify `POSTGRESQL_DUMP_PATH` or `MYSQL_DUMP_PATH` if the default dump executables are not found.
- Regularly update dependencies and check the [documentation](https://djbackup.readthedocs.io/) for new features.
- For secure backups, consider encrypting sensitive data before uploading to remote storage.


## Contributing
We welcome contributions! Please read our [Contributing Guidelines](https://github.com/FZl47/dj_backup/blob/main/CONTRIBUTING.md) for details on how to submit pull requests, report bugs, or suggest features.

## License
DJ Backup is licensed under the [MIT License](https://github.com/FZl47/dj_backup/blob/main/LICENSE.txt).

## Contact
For bugs, feature requests, or questions, please open an issue on [GitHub Issues](https://github.com/FZl47/dj_backup/issues).

---

⭐ **Star this project on [GitHub](https://github.com/FZl47/dj_backup) to support its development!** ⭐
