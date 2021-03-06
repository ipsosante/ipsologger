"""Define a custom logconfig for gunicorn and django."""
import os

# Define our default fields.
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

# Format fields.
format_str = ' '.join([
        '%({})s'.format(el)
        for el
        in default_fields
    ])

# Date format.
DATEFORMAT = '%Y-%m-%dT%H:%M:%S,%03d'

# Define logger.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(message)s'},
        'json-gunicorn': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'gunicorn',
            '()': 'ipsologger.formatter.JsonFormatter', },
        'json-gunicorn-access': {
            'datefmt': DATEFORMAT,
            'tag': 'gunicorn_access',
            'format': format_str + '%(access)',
            '()': 'ipsologger.formatter.JsonFormatter', },
        'json-python': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'python',
            '()': 'ipsologger.formatter.JsonFormatter', },
        'json-django': {
            'format': format_str,
            'datefmt': DATEFORMAT,
            'tag': 'django',
            '()': 'ipsologger.formatter.JsonFormatter', },
    },
    'filters': {
        'default': {
            '()': 'jslog4kube.KubeMetaInject', },
    },
    'handlers': {
        'json-stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-python',
            'filters': ['default']},
        'json-gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-gunicorn',
            'filters': ['default']},
        'json-gunicorn-access': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-gunicorn-access',
            'filters': ['default']},
        'json-django': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'json-django',
            'filters': ['default']},
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'filters': ['default']},
     },
    'loggers': {
        'django': {
            'handlers': ['json-django', ],
            'propagate': True,
            'level': 'INFO',
            'filters': ['default'],
            'formatters': ['json']},
        'gunicorn': {
            'handlers': ['json-gunicorn'],
            'formatters': ['json'],
            'propagate': False,
            'level': 'ERROR'},
        'gunicorn.access': {
            'handlers': ['json-gunicorn-access'],
            'formatters': ['json-access'],
            'propagate': False,
            'level': 'INFO'},
        'gunicorn.error': {
            'handlers': ['json-gunicorn'],
            'formatters': ['json'],
            'propagate': False,
            'level': 'INFO'},
        'requests': {
            'handlers': ['json-stdout', ],
            'formatters': ['json'],
            'propagate': True,
            'filters': ['default'],
            'level': 'INFO'}
    }
}

if os.environ.get('GUNICORN_LOGGER_USE_SOCKET_HANDLER', False):
    socket_host = os.environ.get('GUNICORN_LOGGER_SOCKET_HOST', '127.0.0.1')
    socket_port = int(os.environ.get('GUNICORN_LOGGER_SOCKET_PORT', 9000))
    LOGGING['handlers'].update({
        'json-gunicorn-socket': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SocketHandler',
            'host': socket_host,
            'port': socket_port,
            'formatter': 'json-gunicorn',
            'filters': ['default']},
        'json-gunicorn-access-socket': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SocketHandler',
            'host': socket_host,
            'port': socket_port,
            'formatter': 'json-gunicorn-access',
            'filters': ['default']},
        'json-django-socket': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SocketHandler',
            'host': socket_host,
            'port': socket_port,
            'formatter': 'json-django',
            'filters': ['default']},
             })
    LOGGING['loggers']['gunicorn']['handlers'].append('json-gunicorn-socket')
    LOGGING['loggers']['gunicorn.access']['handlers'].append('json-gunicorn-access-socket')
    LOGGING['loggers']['gunicorn.error']['handlers'].append('json-gunicorn-socket')
    LOGGING['loggers']['django']['handlers'].append('json-django-socket')
