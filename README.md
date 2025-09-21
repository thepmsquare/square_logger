# square_logger

> 📌 versioning: see [CHANGELOG.md](./CHANGELOG.md).

## about

python logger for my personal use.

## goals

- standardized opinionated logging setup
- improved readability
- auto logging decorators
- redaction support in auto logging
- simple configuration

## installation

```shell
pip install square_logger
```

## usage

see [USAGE.md](./USAGE.md) or [example.py](./example.py).
> note:
> - SquareLogger provides a full opinionated setup with file rotation, formatters, redaction, and auto_logger decorator.
> - SquareCustomLogger wraps any existing logging.Logger and adds the auto_logger decorator plus optional redaction
    without changing your original logger.

## env

- python>=3.12.0

> feedback is appreciated. thank you!