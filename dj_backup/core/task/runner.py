import time
import sys

from dj_backup.core.utils import log_event

from .schedule import BackgroundScheduler

scheduler = None


def run():
    global scheduler
    try:
        scheduler = BackgroundScheduler()
        log_event('Task handler is running!')
        scheduler.start()

        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        msg = 'Task handler is shutting down..'
        log_event(msg)
        sys.stdout.write(msg + '\n')
        if scheduler:
            scheduler.shutdown()
        msg = 'Task handler has shut down!'
        log_event(msg)
        sys.stdout.write(msg)
