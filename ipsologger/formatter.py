import datetime
import socket
import json
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):

    def __init__(self, *args, **kwargs):
        self.tag = kwargs.pop("tag", "python")
        super().__init__(*args, **kwargs)
        self.hostname = socket.gethostname()
        

    def add_fields(self, log_record, record, message_dict):
        """Add @tag, @timestamp, @hostname fields."""
        super().add_fields(log_record, record, message_dict)
        datetime_now_utc = datetime.datetime.now(datetime.timezone.utc)
        log_record['@timestamp'] = datetime_now_utc.isoformat()
        log_record['@hostname'] = self.hostname
        log_record['@tag'] = self.tag
        
