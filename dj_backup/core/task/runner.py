import time
import sys

from typing import Optional

from dj_backup.core.utils import log_event
from .schedule import BackgroundScheduler

scheduler: Optional[BackgroundScheduler] = None


def run() -> None:
    """
        Starts the background scheduler and keeps it running in a loop.

        Handles shutdown on KeyboardInterrupt or SystemExit.
        Logs key events for monitoring.
    """
    global scheduler
    try:
        scheduler = BackgroundScheduler()
        log_event('Task handler is running!')
        scheduler.start()

        # Keep the process alive
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        # Handle shutdown
        msg = 'Task handler is shutting down..'
        log_event(msg)
        sys.stdout.write(msg + '\n')

        if scheduler:
            scheduler.shutdown()

        msg = 'Task handler has shut down!'
        log_event(msg)
        sys.stdout.write(msg + '\n')
