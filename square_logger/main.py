import functools
import glob
import logging
import os
import re
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        filename,
        pint_log_backup_count,
        when="MIDNIGHT",
        interval=1,
    ):
        super().__init__(filename, when, interval, pint_log_backup_count)


class SquareLogger:
    def __init__(
        self,
        pstr_log_file_name: str,
        pint_log_level: int = 20,
        pstr_log_path: str = "logs",
        pint_log_backup_count: int = 3,
    ):
        """
        Initializes the logger with the specified parameters.

            :param pstr_log_file_name: str
                Name of the log file.
            :param pint_log_level: int, optional, default: 20
                Logging level, with possible values:
                | Log Level | Value |
                | --------- | ----- |
                | CRITICAL  | 50    |
                | ERROR     | 40    |
                | WARNING   | 30    |
                | INFO      | 20    |
                | DEBUG     | 10    |
                | NOTSET    | 0     |
            :param pstr_log_path: str, optional, default: "logs"
                Path to the directory where log files will be stored. This can be an absolute or relative path.
            :param pint_log_backup_count: int, optional, default: 3
                Number of backup log files to keep during rotation. If set to zero, rollover never occurs.

            Example:
                logger = Logger("my_log.log", pint_log_level=10, pint_log_path="/var/logs", pint_log_backup_count=5)

        """
        try:
            self.gstr_log_file_name = pstr_log_file_name
            self.gint_log_level = pint_log_level
            self.gstr_log_path = pstr_log_path
            self.gint_log_backup_count = pint_log_backup_count

            self.logger = self.main()
        except Exception:
            raise

    def cleanup_old_logs(self):
        log_pattern = f"{self.gstr_log_path}{os.sep}{self.gstr_log_file_name}.*.log"
        log_files = glob.glob(log_pattern)

        def extract_date(log_file):
            match = re.search(r"(\d{2}-[A-Za-z]+-\d{4})", log_file)
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, "%d-%B-%Y")
            else:
                return datetime.min

        log_files_with_date = [{"file": x, "date": extract_date(x)} for x in log_files]

        for log_file in log_files_with_date:
            if log_file["date"] < datetime.now() - timedelta(
                days=self.gint_log_backup_count
            ):
                os.remove(log_file["file"])

    def main(self):
        try:
            if not os.path.exists(self.gstr_log_path):
                os.makedirs(self.gstr_log_path)
            logger = logging.getLogger("square_logger")
            logger.setLevel(self.gint_log_level)
            handler = CustomTimedRotatingFileHandler(
                filename=f"{self.gstr_log_path}{os.sep}{self.gstr_log_file_name}.log",
                pint_log_backup_count=self.gint_log_backup_count,
            )
            handler.suffix = "%d-%B-%Y"
            handler.namer = lambda name: name.replace(".log", "") + ".log"
            handler.extMatch = re.compile(r"\d{2}-[A-Za-z]+-\d{4}$")
            handler.setLevel(self.gint_log_level)
            formatter = logging.Formatter(
                "=== === ===\n%(asctime)s\n%(levelname)s\n%(message)s\n=== === ===\n\n",
                datefmt="%d-%B-%Y %I:%M:%S %p %A",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            self.cleanup_old_logs()
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
