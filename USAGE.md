# usage guide

## setup

### using SquareLogger

```python
from square_logger import SquareLogger

# create a logger instance
logger_instance = SquareLogger(
    log_file_name="app",  # log filename prefix
    log_level=10,  # DEBUG level
    log_path="logs",  # directory for logs
    log_backup_count=3,  # number of rotated logs to keep
    logger_name="my_app_logger",  # optional, defaults to __name__
    formatter_choice="json",  # "human_readable" or "json"
    enable_redaction=True  # redact sensitive keys automatically
)

logger = logger_instance.logger

logger.info("application started")
logger.debug("debugging details")
logger.error("something went wrong")
```

#### logs will be written to:

```text
logs/app.log
logs/app.log.2025-09-21_00-00-34
logs/app.log.2025-09-22_00-00-16
```

> note: the filenames depend on the TimedRotatingFileHandler. rotation is midnight by default.

### using SquareCustomLogger

```python
from square_logger import SquareCustomLogger
import logging

# assume you already have a logger
base_logger = logging.getLogger("external_logger")

# wrap it with auto_logger and redaction
square_logger = SquareCustomLogger(base_logger, enable_redaction=True)


@square_logger.auto_logger(redacted_keys={"token"})
def some_func(token: str):
    return token


some_func("secret_token")
```

> retains all features of your existing logger while adding auto_logger and optional redaction.

## auto_logger decorator (sync functions)

the auto_logger decorator automatically logs function calls, arguments, return values, and exceptions.
it also redacts sensitive keys if configured.

```python
from square_logger import SquareLogger

square_logger = SquareLogger(log_file_name="demo", log_level=10)


@square_logger.auto_logger(redacted_keys={"password", "token"})
def process_user(username: str, password: str, token: str):
    return {"username": username, "status": "ok", "password": password, "token": token}


process_user("alice", "supersecret", "abcd1234")
```

## auto_logger decorator (async functions)

```python
import asyncio

from square_logger import SquareLogger

square_logger = SquareLogger(log_file_name="demo", log_level=10)


@square_logger.auto_logger(redacted_keys={"secret"})
async def fetch_data(user_id: int, secret: str):
    return {"user_id": user_id, "secret": secret, "data": [1, 2, 3]}


asyncio.run(fetch_data(42, "hidden"))
```

## logs show (json formatter example):

```text
{"timestamp": "2025-09-21T13:00:00Z", "level": "debug", "message": "Calling process_user with args: {'username': 'alice', 'password': '**REDACTED**', 'token': '**REDACTED**'}"}
{"timestamp": "2025-09-21T13:00:00Z", "level": "debug", "message": "process_user returned: {'username': 'alice', 'status': 'ok', 'password': '**REDACTED**', 'token': '**REDACTED**'}"}
```