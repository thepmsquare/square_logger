import asyncio
import functools
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from square_logger.configuration import cint_log_level, cstr_log_path


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
            self,
            filename,
            when="MIDNIGHT",
            interval=1,
    ):
        super().__init__(
            filename,
            when,
            interval,
        )

    def rotation_filename(self, default_name):
        base, ext = os.path.splitext(default_name)
        base1, base2 = os.path.splitext(base)
        return f"{base1}{ext}{base2}"


class SquareLogger:
    def __init__(self, pstr_log_file_name):
        try:
            self.gstr_log_file_name = pstr_log_file_name
            self.logger = self.main()
        except Exception:
            raise

    def main(self):
        try:
            logger = logging.getLogger("square_logger")
            logger.setLevel(cint_log_level)
            handler = CustomTimedRotatingFileHandler(
                f"{cstr_log_path}{os.sep}{self.gstr_log_file_name}.log",
            )
            handler.suffix = "%d-%B-%Y"
            handler.setLevel(cint_log_level)
            formatter = logging.Formatter(
                "=== === ===\n%(asctime)s\n%(levelname)s\n%(message)s\n=== === ===\n\n",
                datefmt="%d-%B-%Y %I:%M:%S %p %A",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            return logger
        except Exception:
            raise

    def auto_logger(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.logger.debug(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)
                self.logger.debug(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                self.logger.error(f"An exception occurred in {func.__name__}: {e}")
                raise

        return wrapper

    def async_auto_logger(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                self.logger.debug(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = await func(*args, **kwargs)
                self.logger.debug(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                self.logger.error(f"An exception occurred in {func.__name__}: {e}")
                raise

        return wrapper
