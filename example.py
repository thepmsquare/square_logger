import asyncio
import logging

from square_logger import SquareLogger, SquareCustomLogger

# -----------------------
# using SquareLogger
# -----------------------
square_logger = SquareLogger(
    log_file_name="demo",
    log_level=10,  # DEBUG level
    log_path="logs",
    log_backup_count=3,  # keep logs for 3 days
    enable_redaction=True,
)
logger = square_logger.logger

# simple log statements
logger.info("application started")
logger.debug("debugging details")
logger.error("an error message example")


# sync function example
@square_logger.auto_logger(redacted_keys={"password"})
def login(username: str, password: str):
    return {"username": username, "password": password, "status": "ok"}


# async function example
@square_logger.auto_logger(redacted_keys={"secret"})
async def fetch_data(user_id: int, secret: str):
    return {"user_id": user_id, "secret": secret, "data": [1, 2, 3]}


# -----------------------
# using SquareCustomLogger
# -----------------------
base_logger = logging.getLogger("external_logger")
custom_logger = SquareCustomLogger(base_logger, enable_redaction=True)


@custom_logger.auto_logger(redacted_keys={"token"})
def some_func(token: str):
    return {"token": token, "status": "ok"}


if __name__ == "__main__":
    # run sync functions
    login("alice", "supersecret")
    some_func("hidden_token")

    # run async function
    asyncio.run(fetch_data(42, "hidden_secret"))
