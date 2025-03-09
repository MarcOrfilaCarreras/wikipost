import logging
import re

from .utils.encrypt import Encryption


class LoggingFilter(logging.Filter):
    def filter(self, record):
        log_format = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \w+ - \[.*\] .+'

        return bool(re.match(log_format, record.msg))


logging.basicConfig(filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,)

logging.getLogger('werkzeug').disabled = True
logging.getLogger('instagrapi').disabled = True
logging.getLogger('instagrapi').addFilter(LoggingFilter())
logging.getLogger('apscheduler').disabled = True
logging.getLogger('apscheduler.scheduler').addFilter(LoggingFilter())
logging.getLogger('apscheduler.executors.default').propagate = False


scheduler = None
encryption = Encryption()
