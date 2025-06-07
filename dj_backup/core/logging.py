import sys
import traceback
import logging

from dj_backup.core.triggers import TriggerLogBase
from dj_backup import settings

logger = logging.getLogger('dj_backup')


def log_event(msg, level='info', exc_info=False, **kwargs):
    LOG_LEVELS_NUM = settings.get_log_level_num()

    level = level.upper()
    level_n = LOG_LEVELS_NUM[level]
    logger.log(level_n, msg=msg, exc_info=exc_info, **kwargs)
    exc = ''
    if exc_info:
        # call triggers
        exception_type, exception_value, trace = sys.exc_info()
        tr = traceback.extract_tb(trace, 1)
        if tr:
            tr = tr[0]
        try:
            exc = f"""
                type: `{exception_type}`\n
                value: `{exception_value}`\n
                file: `{tr.filename}`\n
                line: `{tr.lineno}`\n
                exc_line: `{tr.line}`
            """
        except Exception:
            pass
    TriggerLogBase.call_trigger(level, level_n, msg, exc, [], **kwargs)
