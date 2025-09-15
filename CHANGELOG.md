# changelog

## v3.0.0 (in progress)

- **breaking change**: input parameters are no longer in hungarian-style prefixes.
- **breaking change**: rename auto_logger to log_function_calls.
- add SquareCustomLogger class.
- SquareLogger
    - new optional parameter logger_name.

## v2.0.1

- docs
    - add GNU license.
    - update setup.py classifiers, author name.
    - move changelog to different file.
    - add pyproject.toml file.

## v2.0.0

- remove async_auto_logger to merge with auto_logger.
- new dependencies pytest and pydantic.
- new optional input parameter pbool_enable_redaction.
- add redacted_keys parameter in auto_logger.
- add common fixture log_folder.
- add tests for auto_logger.

## v1.0.7

- add cleanup_old_logs.

## v1.0.6

- remove config and move variable as init parameters for SquareLogger class.
- import SquareLogger in __init__.py

## v1.0.5

- change config default to relative path.

## v1.0.4

- Added a new configuration option backupCount to specify the number of backup log files to retain during rotation in
  the logger.

## v1.0.3

- config is being read using lapa_commons.

## v1.0.2

- create log path folder if they don't exist.
- change config default to relative path.

## v1.0.1

- bug fix in auto_logger and implement async_auto_logger.

## v1.0.0

- initial implementation.