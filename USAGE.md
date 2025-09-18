# usage guide

## setup

```python
from square_logger import SquareLogger

# create a logger instance
logger = SquareLogger(
    log_file_name="app",  # log filename prefix
    log_level=10,  # DEBUG level
    log_path="logs",  # directory for logs
    log_backup_count=5,  # keep 5 days of logs
    enable_redaction=True  # redact sensitive keys
).logger

logger.info("application started")
logger.debug("debugging details")
logger.error("something went wrong")
```

### logs will be written to:

```text
logs/app.log
logs/app.31-August-2025.log
logs/app.30-August-2025.log
```

## using auto_logger decorator

the auto_logger decorator automatically logs function calls, arguments, return values, and exceptions.
it also redacts sensitive keys if configured.

```python
from square_logger import SquareLogger

square_logger = SquareLogger("demo", log_level=10)


@square_logger.auto_logger(redacted_keys={"password", "token"})
def process_user(username: str, password: str, token: str):
    return {"username": username, "status": "ok", "password": password, "token": token}


process_user("alice", "supersecret", "abcd1234")
```

### logs show:

```text
Calling process_user with args: {'username': 'alice', 'password': '**REDACTED**', 'token': '**REDACTED**'}
process_user returned: {'username': 'alice', 'status': 'ok', 'password': '**REDACTED**', 'token': '**REDACTED**'}
```

## async functions

```python
import asyncio

from square_logger import SquareLogger

square_logger = SquareLogger("demo", log_level=10)


@square_logger.auto_logger(redacted_keys={"secret"})
async def fetch_data(user_id: int, secret: str):
    return {"user_id": user_id, "secret": secret, "data": [1, 2, 3]}


asyncio.run(fetch_data(42, "hidden"))
```