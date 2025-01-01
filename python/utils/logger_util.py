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
import os
import sys
import uuid
import logging
import logging.handlers
import logging.config
from threading import current_thread
from typing import Optional
    
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s.%(msecs)03d] %(filename)s [line:%(lineno)d] %(levelname)s [%(logid)s] %(message)s",
        },
    },
    "handlers": {},
    "loggers": {
        "appbuilder": {
            "handlers": [],
            "level": "INFO",
            "propagate": True,
        },
    },
}

CONSOLE_HEADER = {
    "level": "INFO",
    "class": "logging.StreamHandler",
    "formatter": "standard",
    "stream": "ext://sys.stdout",  # Use standard output
}

ERROR_FILE_HEADER = {
    "level": "ERROR",
    "class": "logging.FileHandler",
    "filename": "error.tmp.log",
    "formatter": "standard",
}

FILE_HEADER = {
    "level": "DEBUG",
    "class": "logging.FileHandler",
    "filename": "tmp.log",
    "formatter": "standard",
}

ERROR_SET_CONFIG_HEADER = {
    'level': 'ERROR',
    'formatter': 'standard',
    'class': 'appbuilder.SizeAndTimeRotatingFileHandler',
    'filename': 'error.tmp.log',
    'when': 'MIDDNIGHT',
    'interval': 1,
    'max_bytes': 5*1024*1024,
    'backup_count': 20,
    'total_size_limit': 100*1024*1024
}

SET_CONFIG_HEADER = {
    'level': 'DEBUG',
    'formatter': 'standard',
    'class': 'appbuilder.SizeAndTimeRotatingFileHandler',
    'filename': 'tmp.log',
    'when': 'MIDNIGHT',
    'interval': 1,
    'max_bytes': 5*1024*1024,
    'backup_count': 20,
    'total_size_limit': 100*1024*1024
}

class LoggerWithLoggerId(logging.LoggerAdapter):
    """
    logger with logid
    """
    def __init__(self, logger, extra, loglevel):
        """
        init
        """
        LOGGING_CONFIG["handlers"] = {}
        LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"] = []
        log_file = os.environ.get("APPBUILDER_LOGFILE", "")
        if log_file:
            ERROR_FILE_HEADER["filename"] = f"error.{log_file}"
            FILE_HEADER["filename"] = log_file
            FILE_HEADER["level"] = loglevel
            LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
            if loglevel in ("DEBUG", "INFO", "WARNING"):
                LOGGING_CONFIG["handlers"]["error_file"] = ERROR_FILE_HEADER
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
        CONSOLE_HEADER["level"] = loglevel
        LOGGING_CONFIG["handlers"]["console"] = CONSOLE_HEADER
        LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("console")
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

    def setFilename(self, filename):
        """
        set filename
        """
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            FILE_HEADER["filename"] = filename
            LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
        if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            ERROR_FILE_HEADER["filename"] = f"error.{filename}"
            LOGGING_CONFIG["handlers"]["error_file"] = ERROR_FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
        FILE_HEADER["filename"] = filename
        ERROR_FILE_HEADER["filename"] = f"error.{filename}"
        LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
        LOGGING_CONFIG["handlers"]["error_file"] = ERROR_FILE_HEADER
        logging.config.dictConfig(LOGGING_CONFIG)

    def setLoglevel(self, level):
        """
        set log level
        """
        log_level = level.strip().lower()
        if log_level not in ["debug", "info", "warning", "error"]:
            raise ValueError("expected APPBUILDER_LOGLEVEL in [debug, info, warning, error], but got %s" % log_level)
        log_level = log_level.upper()
        if "file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            FILE_HEADER["level"] = log_level
            LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
        if "console" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"] or not LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            CONSOLE_HEADER["level"] = log_level
            LOGGING_CONFIG["handlers"]["console"] = CONSOLE_HEADER
        LOGGING_CONFIG['loggers']['appbuilder']['level'] = log_level
        logging.config.dictConfig(LOGGING_CONFIG)

    def setLogConfig(self,
                    console_show: bool = True,
                    loglevel: str = "DEBUG",
                    file_name: str = "tmp.log",
                    when: str = "MIDNIGHT",
                    interval: int = 1,
                    max_bytes: Optional[int] = None, # 以B为单位
                    total_size_limit: Optional[int] = None, # 以B为单位
                    backup_count: Optional[int] = None
                    ):
        LOGGING_CONFIG["handlers"] = {}
        LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"] = []
        

        # 设置console输出日志
        if console_show:
            CONSOLE_HEADER['level'] = loglevel
            LOGGING_CONFIG["handlers"]["console"] = CONSOLE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("console")
        
        # 参数验证
        if not max_bytes or max_bytes <= 0:
            max_bytes = sys.maxsize
        if not total_size_limit or total_size_limit <= 0:
            total_size_limit = sys.maxsize
        if not backup_count or backup_count <= 0:
            backup_count = sys.maxsize
        if interval < 1:
            interval = 1
        when = when.strip().lower()
        if when not in ["s", "m", "h", "d", "midnight"]:
            raise ValueError("expected when in [S, M, H, D, MIDNIGHT], but got %s" % when)

        # 设置文件输出日志
        # 设置日志级别
        SET_CONFIG_HEADER['level'] = loglevel

        # 设置文件名称
        SET_CONFIG_HEADER['filename'] = file_name
        ERROR_SET_CONFIG_HEADER['filename'] = f"error.{file_name}"

        # 设置滚动时间
        SET_CONFIG_HEADER['when'] = when
        ERROR_SET_CONFIG_HEADER['when'] = when
        SET_CONFIG_HEADER['interval'] = interval
        ERROR_SET_CONFIG_HEADER['interval'] = interval

        # 设置最大文件大小
        
        SET_CONFIG_HEADER['max_bytes'] = max_bytes
        ERROR_SET_CONFIG_HEADER['max_bytes'] = max_bytes

        # 设置总大小限制
        SET_CONFIG_HEADER['total_size_limit'] = total_size_limit
        ERROR_SET_CONFIG_HEADER['total_size_limit'] = total_size_limit

        # 设置备份数量
        SET_CONFIG_HEADER['backup_count'] = backup_count
        ERROR_SET_CONFIG_HEADER['backup_count'] = backup_count

        LOGGING_CONFIG["handlers"]["file"] = SET_CONFIG_HEADER
        LOGGING_CONFIG["handlers"]["error_file"] = ERROR_SET_CONFIG_HEADER
        LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].extend(["file", "error_file"])
        LOGGING_CONFIG['loggers']['appbuilder']['level'] = loglevel
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
