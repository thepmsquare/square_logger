def test_auto_logger_redaction(caplog, log_folder):
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
    )

    @global_object_square_logger.auto_logger(redacted_keys=["secret"])
    def do_something(value, secret=None):
        return {"value": value, "secret": secret}

    result = do_something("visible", secret="12345")
    log_output = "\n".join(caplog.messages)

    assert result["secret"] == "12345"
    assert "visible" in log_output
    assert "12345" not in log_output
    assert "**REDACTED**" in log_output


def test_auto_logger_redaction_variation2(caplog, log_folder):
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
    )

    @global_object_square_logger.auto_logger(redacted_keys=["secret"])
    def do_something(value, secret=None):
        return {"value": value, "secret": secret}

    result = do_something("visible", "12345")
    log_output = "\n".join(caplog.messages)

    assert result["secret"] == "12345"
    assert "visible" in log_output
    assert "12345" not in log_output
    assert "**REDACTED**" in log_output


def test_auto_logger_with_disabled_redaction(caplog, log_folder):
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
        enable_redaction=False,
    )

    @global_object_square_logger.auto_logger(redacted_keys=["secret"])
    def do_something(value, secret=None):
        return {"value": value, "secret": secret}

    result = do_something("visible", secret="12345")
    log_output = "\n".join(caplog.messages)

    assert result["secret"] == "12345"
    assert "visible" in log_output
    assert "12345" in log_output


def test_auto_logger_without_redaction(caplog, log_folder):
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
    )

    @global_object_square_logger.auto_logger()
    def do_something(value, secret=None):
        return {"value": value, "secret": secret}

    result = do_something("visible", secret="12345")
    log_output = "\n".join(caplog.messages)

    assert result["secret"] == "12345"
    assert "visible" in log_output
    assert "12345" in log_output


def test_auto_logger_without_redaction_variation2(caplog, log_folder):
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
        enable_redaction=False,
    )

    @global_object_square_logger.auto_logger()
    def do_something(value, secret=None):
        return {"value": value, "secret": secret}

    result = do_something("visible", secret="12345")
    log_output = "\n".join(caplog.messages)

    assert result["secret"] == "12345"
    assert "visible" in log_output
    assert "12345" in log_output


def test_auto_logger_with_pydantic_input(caplog, log_folder):
    from square_logger import SquareLogger
    from pydantic import BaseModel

    class InputModel(BaseModel):
        value: str
        secret: str

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing",
        log_level=10,
        log_path=log_folder,
    )

    @global_object_square_logger.auto_logger(redacted_keys=["secret"])
    def do_something(input_model: InputModel):
        return input_model

    result = do_something(InputModel(value="visible", secret="12345"))
    log_output = "\n".join(caplog.messages)

    assert result.secret == "12345"
    assert "visible" in log_output
    assert "12345" not in log_output
    assert "**REDACTED**" in log_output


def test_square_logger_with_custom_name():
    from square_logger import SquareLogger

    global_object_square_logger = SquareLogger(
        log_file_name="log_testing", log_level=10, logger_name="my_custom_logger"
    )

    # Assert the logger name is what we passed in
    assert global_object_square_logger.logger.name == "my_custom_logger"


def test_square_logger_with_default_name():
    from square_logger import SquareLogger

    # Create a dummy class or function to check the default __name__
    class TestClass:
        def __init__(self):
            self.logger = SquareLogger(log_file_name="default_log", log_level=10)

    test_instance = TestClass()
    # The default name should be the name of the module where the SquareLogger instance is created, which in this case is __main__
    assert test_instance.logger.logger.name == "square_logger.main"


def test_square_custom_logger_initialization():
    import logging
    from square_logger import SquareCustomLogger

    # Create a custom logger instance
    custom_logger = logging.getLogger("custom_test_logger")
    custom_logger.setLevel(logging.INFO)

    # Initialize SquareCustomLogger with the custom logger
    scl = SquareCustomLogger(logger=custom_logger)

    # Assert that the logger instance is the one we passed in
    assert scl.logger is custom_logger
    # Assert that the decorator also holds a reference to the same logger
    assert scl.decorator.logger is custom_logger
    # Assert that redaction is enabled by default
    assert scl.decorator.enable_redaction is True


def test_square_custom_logger_disabled_redaction():
    import logging
    from square_logger import SquareCustomLogger

    custom_logger = logging.getLogger("redaction_disabled_logger")
    custom_logger.setLevel(logging.INFO)

    # Initialize SquareCustomLogger with redaction disabled
    scl = SquareCustomLogger(logger=custom_logger, enable_redaction=False)

    # Assert that the redaction flag is set to False
    assert scl.decorator.enable_redaction is False


def test_square_custom_logger_auto_logger(caplog):
    import logging
    from square_logger import SquareCustomLogger

    custom_logger = logging.getLogger("auto_logger_test")
    # Set level to DEBUG to capture the decorator's logs
    custom_logger.setLevel(logging.DEBUG)

    # Add a handler to the logger to capture the logs.
    # This is similar to what LoggerFactory does, but we'll do it manually for the test.
    handler = logging.StreamHandler()
    custom_logger.addHandler(handler)

    scl = SquareCustomLogger(logger=custom_logger)

    @scl.auto_logger()
    def greet(name):
        return f"Hello, {name}"

    with caplog.at_level(logging.DEBUG, logger="auto_logger_test"):
        result = greet("World")

    assert result == "Hello, World"
    assert "Calling greet with args" in caplog.text
    assert "returned: Hello, World" in caplog.text


def test_square_logger_creates_log_file(tmp_path):
    from square_logger import SquareLogger
    import os

    log_file_name = "test_log_creation"
    log_path = tmp_path / "logs"

    # Instantiate SquareLogger, which will create the file
    SquareLogger(log_file_name=log_file_name, log_path=str(log_path))

    # Construct the expected file path
    expected_log_file = os.path.join(str(log_path), f"{log_file_name}.log")

    # Assert that the log file now exists
    assert os.path.exists(expected_log_file)
