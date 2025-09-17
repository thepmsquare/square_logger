import functools
import inspect
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Literal

from pydantic import BaseModel


class Redactor:
    @staticmethod
    def redact(data, redacted_keys=None):
        if redacted_keys is None:
            redacted_keys = set()
        else:
            redacted_keys = set(redacted_keys)

        if isinstance(data, dict):
            return {
                k: (
                    "**REDACTED**"
                    if k in redacted_keys
                    else Redactor.redact(v, redacted_keys)
                )
                for k, v in data.items()
            }
        elif isinstance(data, (list, tuple, set)):
            return type(data)(Redactor.redact(v, redacted_keys) for v in data)
        elif isinstance(data, BaseModel):
            return Redactor.redact(data.model_dump(), redacted_keys)

        return data


class SquareTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, log_backup_count, when="MIDNIGHT", interval=1):
        super().__init__(filename, when, interval, log_backup_count)


class LoggerFactory:
    @staticmethod
    def build_logger(
        log_file_name: str,
        log_path: str,
        log_level: int,
        log_backup_count: int,
        logger_name: str,
        formatter_choice: Literal["human_readable", "json"],
    ):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        handler = SquareTimedRotatingFileHandler(
            filename=f"{log_path}{os.sep}{log_file_name}.log",
            log_backup_count=log_backup_count,
        )
        handler.setLevel(log_level)
        if formatter_choice == "human_readable":

            formatter = logging.Formatter(
                "=== === ===\n%(asctime)s\n%(levelname)s\n%(message)s\n=== === ===\n\n",
                datefmt="%d-%B-%Y %I:%M:%S %p %A",
            )
        else:

            class JsonFormatter(logging.Formatter):
                def format(self, record):
                    log_record = {
                        "timestamp": self.formatTime(
                            record, datefmt="%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "level": record.levelname.lower(),
                        "message": record.getMessage(),
                    }
                    return json.dumps(log_record)

            formatter = JsonFormatter()

        handler.setFormatter(formatter)

        # prevent duplicate handlers on re-instantiation
        if not logger.handlers:
            logger.addHandler(handler)

        return logger


class AutoLoggerDecorator:
    def __init__(self, logger, enable_redaction=True):
        self.logger = logger
        self.enable_redaction = enable_redaction

    def log_function_calls(self, redacted_keys=None):
        if redacted_keys is None:
            redacted_keys = set()
        else:
            redacted_keys = set(redacted_keys)

        def decorator(func):
            is_coroutine = inspect.iscoroutinefunction(func)

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    sig = inspect.signature(func)
                    bound = sig.bind(*args, **kwargs)
                    bound.apply_defaults()
                    all_kwargs = bound.arguments
                    redacted = (
                        Redactor.redact(all_kwargs, redacted_keys)
                        if self.enable_redaction
                        else all_kwargs
                    )
                    self.logger.debug(f"Calling {func.__name__} with args: {redacted}.")
                    result = await func(*args, **kwargs)
                    self.logger.debug(
                        f"{func.__name__} returned: {Redactor.redact(result, redacted_keys) if self.enable_redaction else result}"
                    )
                    return result
                except Exception as e:
                    self.logger.error(
                        f"An exception occurred in {func.__name__}: {e}", exc_info=True
                    )
                    raise

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    sig = inspect.signature(func)
                    bound = sig.bind(*args, **kwargs)
                    bound.apply_defaults()
                    all_kwargs = bound.arguments
                    redacted = (
                        Redactor.redact(all_kwargs, redacted_keys)
                        if self.enable_redaction
                        else all_kwargs
                    )
                    self.logger.debug(f"Calling {func.__name__} with args: {redacted}.")
                    result = func(*args, **kwargs)
                    self.logger.debug(
                        f"{func.__name__} returned: {Redactor.redact(result, redacted_keys) if self.enable_redaction else result}"
                    )
                    return result
                except Exception as e:
                    self.logger.error(
                        f"An exception occurred in {func.__name__}: {e}", exc_info=True
                    )
                    raise

            return async_wrapper if is_coroutine else sync_wrapper

        return decorator


class SquareLogger:
    def __init__(
        self,
        log_file_name: str,
        log_level: int = 20,
        log_path: str = "logs",
        log_backup_count: int = 3,
        logger_name: str = __name__,
        formatter_choice: Literal["human_readable", "json"] = "json",
        enable_redaction: bool = True,
    ):
        """
        Opinionated logger setup.
        """
        self.logger = LoggerFactory.build_logger(
            log_file_name=log_file_name,
            log_path=log_path,
            log_level=log_level,
            log_backup_count=log_backup_count,
            logger_name=logger_name,
            formatter_choice=formatter_choice,
        )
        self.decorator = AutoLoggerDecorator(self.logger, enable_redaction)

    def log_function_calls(self, redacted_keys=None):
        return self.decorator.log_function_calls(redacted_keys)


class SquareCustomLogger:
    def __init__(
        self,
        logger: logging.Logger,
        enable_redaction: bool = True,
    ):

        self.logger = logger
        self.decorator = AutoLoggerDecorator(self.logger, enable_redaction)

    def log_function_calls(self, redacted_keys=None):
        return self.decorator.log_function_calls(redacted_keys)
