import logging
import logging.config
import sys

class MaxLevelFilter(logging.Filter):
    def __init__(self, level=logging.WARNING):
        super().__init__()
        self.max_level = level

    def filter(self, record):
        return record.levelno <= self.max_level
    
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'max_level_filter': {
            '()': MaxLevelFilter,
            'level': logging.WARNING
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console_stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': sys.stdout,
            'filters': ['max_level_filter']
        }, 
        'console_stderr': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'standard',
            'stream': sys.stderr,

        },
    }, 
    'root': {
        'level': 'DEBUG',
        'handlers': ['console_stdout', 'console_stderr']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
