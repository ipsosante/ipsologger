
default_fields = (
        '@timestamp',
        '@hostname',
        '@tag',
        'asctime',
        'message',
        'name',
        'created',
        'filename',
        'module',
        'funcName',
        'lineno',
        'msecs',
        'pathname',
        'process',
        'processName',
        'relativeCreated',
        'thread',
        'threadName',
        'levelname')


format_str = ' '.join([
        '%({})s'.format(el)
        for el
        in default_fields
    ])

DATEFORMAT = '%Y-%m-%dT%H:%M:%S,%03d'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(message)s'
                    },
        'json-gunicorn': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'gunicorn',
            '()': 'ipsologger.formatter.JsonFormatter',
                    },
        'json-gunicorn-access': {
            'datefmt': DATEFORMAT,
            'tag': 'gunicorn_access',
            'format': format_str + '%(access)',
            '()': 'ipsologger.formatter.JsonFormatter',
         },
        
        'json-python': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'python',
            '()': 'ipsologger.formatter.JsonFormatter',
                    },
        
        'json-django': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'django',
            '()': 'ipsologger.formatter.JsonFormatter',
        },
    },
    'filters': {
        'default': {
            '()': 'jslog4kube.KubeMetaInject',
                    },
            },
    'handlers': {
        'json-stdout': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-python',
            'filters': ['default'],
                    },
        'json-gunicorn': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-gunicorn',
            'filters': ['default'],
                    },
        'json-gunicorn-access': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-gunicorn-access',
            'filters': ['default'],
                    },
        
        'json-django': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-django',
            'filters': ['default'],
                    },
        
        
        'default': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'filters': ['default'],
                    },
            },
    'loggers': {
        'django': {
            'handlers': ['json-django',],
            'propagate': True,
            'level': 'INFO',
            'filters': ['default'],
            'formatters': ['json'],
                    },
        'gunicorn': {
            'handlers': ['json-gunicorn'],
            'formatters': ['json'],
            'propagate': False,
            'level':'ERROR',
                    },
        'gunicorn.access': {
            'handlers': ['json-gunicorn-access'],
            'formatters': ['json-access'],
            'propagate': False,
            'level':'INFO',
                    },
        'gunicorn.error': {
            'handlers': ['json-gunicorn'],
            'formatters': ['json'],
            'propagate': False,
            'level':'INFO',
                    },
        'requests': {
            'handlers': ['json-stdout',],
            'formatters': ['json'],
            'propagate': True,
            'filters': ['default'],
            'level':'INFO',
                    },
            }
    }
