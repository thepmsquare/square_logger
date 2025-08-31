import asyncio

from square_logger import SquareLogger

# initialize logger
square_logger = SquareLogger(
    pstr_log_file_name="demo",
    pint_log_level=10,  # DEBUG level
    pstr_log_path="logs",
    pint_log_backup_count=3,  # keep logs for 3 days
    pbool_enable_redaction=True,
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


if __name__ == "__main__":
    # run sync function
    login("alice", "supersecret")

    # run async function
    asyncio.run(fetch_data(42, "hidden_secret"))
