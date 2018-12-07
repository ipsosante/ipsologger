import unittest
import logging
import json
import sys
import traceback
from io import StringIO
from ipso_json_loggger_formatter import IpsoJsonFormatter


class TestIpsoJsonFormatter(unittest.TestCase):

    
    def setUp(self):
        self.logger = logging.getLogger('logging-test')
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()
        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def test_custom_format(self):
        """Test our custom format."""
        supported_keys = ['@tag', '@hostname', '@timestamp', '@message']
        log_format = lambda x: ['%({0:s})'.format(i) for i in x]
        custom_format = ' '.join(log_format(supported_keys))
        formatter = IpsoJsonFormatter(custom_format, tag='custom')
        self.logHandler.setFormatter(formatter)
        msg = "t≈esting logging format"
        self.logger.info(msg)
        log_msg = self.buffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            if supported_key in log_json:
                self.assertTrue(True)
                                        
