import logging
from logging.config import dictConfig
import os
import sys
from jslog4kube.gunicorn.dictconfig_logger import GunicornLogger as BaseLogger
from .formatter import JsonFormatter
from .settings import LOGGING


class GunicornLogger(BaseLogger):
    '''
    overrides gunicorn's Logger class to provide dictionary configuration
    capabilities
    '''
    
    def setup(self, cfg):
        super().setup(cfg)
        dictConfig(LOGGING)
        
        
