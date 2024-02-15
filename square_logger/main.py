import functools
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import re

from square_logger.configuration import cint_log_level, cstr_log_path, cint_log_backup_count


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
            cint_log_backup_count
        )


class SquareLogger:
    def __init__(self, pstr_log_file_name):
        try:
            self.gstr_log_file_name = pstr_log_file_name
            self.logger = self.main()
        except Exception:
            raise

    def main(self):
        try:
            if not os.path.exists(cstr_log_path):
                os.makedirs(cstr_log_path)
            logger = logging.getLogger("square_logger")
            logger.setLevel(cint_log_level)
            handler = CustomTimedRotatingFileHandler(
                f"{cstr_log_path}{os.sep}{self.gstr_log_file_name}.log",
            )
            handler.suffix = "%d-%B-%Y"
            handler.namer = lambda name: name.replace(".log", "") + ".log"
            handler.extMatch = re.compile(r"\d{2}-\w+-\d{4}$")
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
                self.logger.debug(
                    f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}"
                )
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
                self.logger.debug(
                    f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}"
                )
                result = await func(*args, **kwargs)
                self.logger.debug(f"{func.__name__} returned: {result}")
                return result
            except Exception as e:
                self.logger.error(f"An exception occurred in {func.__name__}: {e}")
                raise

        return wrapper
