import os
import logging

log_paths = {}
loggers = ['events']

for logger in loggers:
    path = os.path.join(os.getcwd(), 'logs', f'{logger}.log')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    log_paths[logger] = path


LOG_CONFIG = {
    'version': 1,
    'formatters': { 
        'default': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': { 
        'default': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'event_log': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': log_paths['events'],
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': { 
        'edspy.client': {
            'handlers': ['default', 'event_log'],
            'level': 'DEBUG',
        }
    }
}