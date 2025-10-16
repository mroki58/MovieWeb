def pick_fields(node, fields):
    return {k: v for k, v in dict(node).items() if k in fields}

from functools import wraps

def with_session(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if "session" in kwargs and kwargs["session"] is not None:
            return func(self, *args, **kwargs)

        with self.driver.session() as session:
            kwargs["session"] = session
            return func(self, *args, **kwargs)
    return wrapper