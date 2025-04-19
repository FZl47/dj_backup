import sys
import traceback

from logging import log as base_log

from .triggers import TriggerLogBase

LOG_LEVELS_NAME = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
}


def log_event(msg, level='info', exc_info=False, **kwargs):
    level = level.upper()
    level_n = LOG_LEVELS_NAME[level]
    base_log(level_n, msg=msg, exc_info=exc_info, **kwargs)

    # call triggers
    exception_type, exception_value, trace = sys.exc_info()
    tr = traceback.extract_tb(trace, 1)[0]
    exc = f"""
        type: `{exception_type}`\n
        value: `{exception_value}`\n
        file: `{tr.filename}`\n
        line: `{tr.lineno}`\n
        exc_line: `{tr.line}`
    """
    TriggerLogBase.call_trigger(level, level_n, msg, exc, [], **kwargs)
