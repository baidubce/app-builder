# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
日志
"""
import uuid
import os
import logging.config
from threading import current_thread


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s.%(msecs)03d] %(filename)s [line:%(lineno)d] %(levelname)s [%(logid)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',  # Use standard output
        },
    },
    'loggers': {
        'appbuilder': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


class LoggerWithLoggerId(logging.LoggerAdapter):
    """
    logger with logid
    """
    def __init__(self, logger, extra, loglevel):
        """
        init
        """
        LOGGING_CONFIG['handlers']['console']['level'] = loglevel
        LOGGING_CONFIG['loggers']['appbuilder']['level'] = loglevel
        logging.config.dictConfig(LOGGING_CONFIG)
        logging.LoggerAdapter.__init__(self, logger, extra)
        self.logid_dict = {}

    def set_auto_logid(self):
        """
        set auto log_id
        """
        self.logid_dict[current_thread().ident] = str(uuid.uuid4().int & (1 << 64) - 1)

    def set_logid(self, logid):
        """
        set log_id
        """
        self.logid_dict[current_thread().ident] = logid

    def get_logid(self):
        """
        get log_id
        """
        if current_thread().ident in self.logid_dict:
            return self.logid_dict[current_thread().ident]
        else:
            return None

    @property
    def level(self):
        """
        level
        """
        return self.logger.level

    def process(self, msg, kwargs):
        """
        processing
        """
        if current_thread().ident in self.logid_dict:
            # in process thread
            if 'extra' not in kwargs:
                kwargs['extra'] = {'logid': self.logid_dict[current_thread().ident]}
            else:
                kwargs['extra']['logid'] = self.logid_dict[current_thread().ident]
        else:
            # in main thread
            if 'extra' not in kwargs:
                kwargs['extra'] = {'logid': 'main-' + str(uuid.uuid4().int & (1 << 64) - 1)}
            else:
                kwargs['extra']['logid'] = 'main-' + str(uuid.uuid4().int & (1 << 64) - 1)

        return msg, kwargs


def _setup_logging():
    log_level = os.environ.get("APPBUILDER_LOGLEVEL", "INFO")
    log_level = log_level.strip().lower()

    if log_level not in ["debug", "info", "warning", "error"]:
        raise ValueError("expected APPBUILDER_LOGLEVEL in [debug, info, warning, error], but got %s" % log_level)
    return LoggerWithLoggerId(logging.getLogger('appbuilder'), {'logid': ''}, log_level.upper())


logger = _setup_logging()


