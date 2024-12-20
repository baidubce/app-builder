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
import sys
import logging.config
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from threading import current_thread


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s.%(msecs)03d] %(filename)s [line:%(lineno)d] %(levelname)s [%(logid)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",  # Use standard output
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "tmp.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "appbuilder": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


TIME_HANDLERS_FILE = {
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'formatter': 'standard',
    'level': 'DEBUG',
    'filename': 'tmp.log',
    'when': 'midnight',  # 可选项: 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight'
    'interval': 1,       # 每1天滚动一次
    'backupCount': 5,    # 保留5个备份
    'encoding': 'utf-8',
}


class LoggerWithLoggerId(logging.LoggerAdapter):
    """
    logger with logid
    """
    def __init__(self, logger, extra, loglevel):
        """
        init
        """
        log_file = os.environ.get("APPBUILDER_LOGFILE", "")
        if log_file:
            LOGGING_CONFIG["handlers"]["file"]["filename"] = log_file
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
            LOGGING_CONFIG["handlers"]["file"]["level"] = loglevel
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

    def setLogConfig(
            self, 
            rolling=True, 
            console_show=True, 
            update_interval:int=1, 
            update_time='', 
            backup_count=0, 
            log_file=''
            ):
        # 配置控制台输出
        if not console_show:
            if "console" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("console")
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")

        # 确定日志文件名称
        if log_file:
            filename = log_file
        elif os.environ.get("APPBUILDER_LOGFILE"):
            filename = os.environ["APPBUILDER_LOGFILE"]
        else:
            filename = LOGGING_CONFIG["handlers"]["file"]["filename"]

        # 确定备份数量
        if backup_count <= 0 or not isinstance(backup_count, int):
            backup_count = sys.maxsize # 默认为无穷大

        # 确定滚动时间
        if update_interval < 1:
            update_interval = 1
        if update_time:
            update_time = update_time.lower()
            if update_time not in ['s', 'm', 'h', 'd', 'midnight'] and not (update_time.startswith('w') and update_time[1:].isdigit() and 0 <= int(update_time[1:]) <= 6):
                raise ValueError("expected APPBUILDER_LOG_UPDATE_TIME in [s, m, h, d, w0-w6, midnight], but got %s" % update_time)
            else:
                update_time = update_time.upper()

        # 创建处理器
        if rolling:
            if update_time:
                TIME_HANDLERS_FILE['filename'] = filename
                TIME_HANDLERS_FILE['when'] = update_time
                TIME_HANDLERS_FILE['interval'] = update_interval
                TIME_HANDLERS_FILE['backupCount'] = backup_count
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("file")
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append('timed_file')
                LOGGING_CONFIG["handlers"]["timed_file"] = TIME_HANDLERS_FILE
                LOGGING_CONFIG["handlers"]["timed_file"]["level"] = LOGGING_CONFIG['loggers']['appbuilder']['level']
        else:
            LOGGING_CONFIG["handlers"]["file"]["filename"] = filename

        logging.config.dictConfig(LOGGING_CONFIG)


    def setFilename(self, filename):
        """
        set filename
        """
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
        LOGGING_CONFIG["handlers"]["file"]["filename"] = filename
        logging.config.dictConfig(LOGGING_CONFIG)

    def setLoglevel(self, level):
        """
        set log level
        """
        log_level = level.strip().lower()

        if log_level not in ["debug", "info", "warning", "error"]:
            raise ValueError("expected APPBUILDER_LOGLEVEL in [debug, info, warning, error], but got %s" % log_level)
        log_level = log_level.upper()
        LOGGING_CONFIG['handlers']['console']['level'] = log_level
        LOGGING_CONFIG['loggers']['appbuilder']['level'] = log_level
        LOGGING_CONFIG["handlers"]["file"]["level"] = log_level
        logging.config.dictConfig(LOGGING_CONFIG)

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


def get_logger(name, level=logging.INFO):
    """
    Get logger from logging with given name, level and format without
    setting logging basicConfig.

    Args:
        name (str): The logger name.
        level (logging.LEVEL): The base level of the logger
        fmt (str): Format of logger output

    Returns:
        logging.Logger: logging logger with given settings

    Examples:
        .. code-block:: python

            logger = log_helper.get_logger(__name__, logging.INFO,
                            fmt='%(asctime)s-%(levelname)s: %(message)s')
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt='%(asctime)s: %(filename)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # stop propagate for propagating may print
    # log multiple times
    logger.propagate = False
    return logger


logger = _setup_logging()
