import threading

from typing import Callable, Optional, Tuple, Dict, Any


class Task:
    """
    A class to run a function in a separate thread.

    Attributes:
        func (Callable): The function to run.
        f_args (Tuple): Positional arguments for the function.
        f_kwargs (Dict): Keyword arguments for the function.
    """

    def __init__(
            self,
            func: Callable,
            f_args: Optional[Tuple[Any]] = None,
            f_kwargs: Optional[Dict[str, Any]] = None) -> None:
        """
            Create a new Task with a function and its arguments.

            Args:
                func (Callable): The function to run.
                f_args (Optional[Tuple[Any, ...]]): Arguments passed by position.
                f_kwargs (Optional[Dict[str, Any]]): Arguments passed by name (keywords).
        """
        self.func = func
        self.f_args = f_args or ()
        self.f_kwargs = f_kwargs or {}

    def run(self) -> None:
        """
            Start running the function in a new thread.
        """
        t = threading.Thread(target=self.func, *self.f_args, **self.f_kwargs)
        t.start()
