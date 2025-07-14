from abc import abstractmethod, ABC


class TriggerLogBase(ABC):
    """
        Trigger classes should inherit from this class.
    """

    @staticmethod
    def call_trigger(level: str, level_n: int, msg: str, exc: Exception, *args: list, **kwargs: dict):
        """
            Call by logging function
        """
        triggers = TriggerLogBase.__subclasses__()
        for trigger in triggers:
            trigger.log(trigger, level, level_n, msg, exc, *args, **kwargs)

    @abstractmethod
    def log(self, level: str, level_n: int, msg: str, exc: Exception, *args: list, **kwargs: dict):
        """
            When a new log is created, this function is called
        """
        raise NotImplementedError
