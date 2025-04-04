# square_logger

## about

python logger for my personal use.

## env

python >= 3.9.6

## changelog

### v1.0.7

- add cleanup_old_logs.

### v1.0.6

- remove config and move variable as init parameters for SquareLogger class.
- import SquareLogger in __init__.py

### v1.0.5

- change config default to relative path.

### v1.0.4

- Added a new configuration option backupCount to specify the number of backup log files to retain during rotation in
  the logger.

### v1.0.3

- config is being read using lapa_commons.

### v1.0.2

- create log path folder if they don't exist.
- change config default to relative path.

### v1.0.1

- bug fix in auto_logger and implement async_auto_logger.

### v1.0.0

- initial implementation.
