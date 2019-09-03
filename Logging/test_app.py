import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def activate_log(path_to_logs, mode_debug=False):
    import logging
    import logging.config

    logger_on = "application"
    if mode_debug is True:
        logger_on = "debugging"

    log_app = 'app.log'
    log_debug = 'debug.log'
    if os.path.isdir(path_to_logs):
        log_app = os.path.join(path_to_logs, log_app)
        log_debug = os.path.join(path_to_logs, log_debug)

    dictLogConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": "WARNING",
            "handlers": [
                "console",
                "logFileRotation"
            ]
        },
        "loggers": {
            "application": {
                "handlers": ["logFileRotation"],
                "level": "INFO",
                "propagate": False
            },
            "debugging": {
                "handlers": [
                    "debug",
                    "logFileDebug"
                ],
                "level": "DEBUG",
                "propagate": False
            }
        },
        "handlers": {
            "debug": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "brief"
            },
            "logFileDebug": {
                "class": "logging.FileHandler",
                "formatter": "verbose",
                "filename": log_debug
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "brief"
            },
            "logFileRotation": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "verbose",
                "backupCount": 3,
                "maxBytes": 102400,
                "filename": log_app
            }
        },
        "formatters": {
            "verbose": {
                "format": "%(asctime)s - %(name)s - %(levelname)-12s %(message)s",
                "datefmt": '%Y-%m-%d %H:%M:%S'
            },
            "brief": {
                "format": "%(levelname)-10s %(message)s"
            }
        }
    }

    logging.config.dictConfig(dictLogConfig)
    logger = logging.getLogger(logger_on)
    logger.info('*** The logger is activated. ***')

    return logger


if __name__ == '__main__':
    logger = activate_log(BASEDIR)

    for x in range(50):
        logger.debug('This is a debug message')
        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a critical message')
