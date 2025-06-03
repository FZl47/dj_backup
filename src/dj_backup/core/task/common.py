import threading


class Task:

    def __init__(self, func, f_args=None, f_kwargs=None):
        self.func = func
        self.f_args = f_args or ()
        self.f_kwargs = f_kwargs or {}

    def run(self):
        t = threading.Thread(target=self.func, args=self.f_args, kwargs=self.f_kwargs)
        t.start()
