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
    "filename": "tmp.error.log",
    "formatter": "standard",
}

FILE_HEADER = {
    "level": "DEBUG",
    "class": "logging.FileHandler",
    "filename": "tmp.info.log",
    "formatter": "standard",
}

ERROR_SET_CONFIG_HEADER = {
    'level': 'ERROR',
    'formatter': 'standard',
    'class': 'appbuilder.SizeAndTimeRotatingFileHandler',
    'file_name': 'tmp.error.log',
    'rotate_frequency': 'MIDDNIGHT',
    'rotate_interval': 1,
    'max_file_size': 5*1024*1024,
    'max_log_files': 20,
    'total_log_size': 100*1024*1024
}

SET_CONFIG_HEADER = {
    'level': 'DEBUG',
    'formatter': 'standard',
    'class': 'appbuilder.SizeAndTimeRotatingFileHandler',
    'file_name': 'tmp.info.log',
    'rotate_frequency': 'MIDDNIGHT',
    'rotate_interval': 1,
    'max_file_size': 5*1024*1024,
    'max_log_files': 20,
    'total_log_size': 100*1024*1024
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
        log_path = os.environ.get("APPBUILDER_LOGPATH", "")
        loglevel = loglevel.strip().lower()
        if loglevel not in ["debug", "info", "warning", "error"]:
            raise ValueError("expected APPBUILDER_LOGLEVEL in [debug, info, warning, error], but got %s" % loglevel)
        loglevel = loglevel.upper()

        if log_path:
            current_pid = str(os.getpid())
            full_log_path = os.path.join(log_path, "log")
            if not os.path.exists(full_log_path):
                os.makedirs(full_log_path)
            info_log_file = os.path.join(log_path, "log", current_pid + ".info.log")
            error_log_file = os.path.join(log_path, "log", current_pid + ".error.log")
            FILE_HEADER["filename"] = info_log_file
            ERROR_FILE_HEADER["filename"] = error_log_file
            FILE_HEADER["level"] = loglevel
            LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
            if loglevel in ("DEBUG", "INFO", "WARNING"):
                LOGGING_CONFIG["handlers"]["error_file"] = ERROR_FILE_HEADER
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
        elif log_file:
            ERROR_FILE_HEADER["filename"] = self._add_error_to_file_name(log_file)
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

    @staticmethod
    def _add_error_to_file_name(filename):
        prefix = "error."
        dir_name, base_name = os.path.split(filename)
        new_base_name = f"{prefix}{base_name}"
        return os.path.join(dir_name, new_base_name)

    def setFilename(self, filename):
        """
        set filename
        """
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            FILE_HEADER["filename"] = filename
            LOGGING_CONFIG["handlers"]["file"] = FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
        if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            ERROR_FILE_HEADER["filename"] = self._add_error_to_file_name(filename)
            LOGGING_CONFIG["handlers"]["error_file"] = ERROR_FILE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
        FILE_HEADER["filename"] = filename
        ERROR_FILE_HEADER["filename"] = self._add_error_to_file_name(filename)
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
                    console_output: bool = True,
                    loglevel: str = "DEBUG",
                    log_path: str = "/tmp",
                    rotate_frequency: str = "MIDNIGHT",
                    rotate_interval: int = 1,
                    max_file_size: Optional[int] = None, # 以B为单位
                    total_log_size: Optional[int] = None, # 以B为单位
                    max_log_files: Optional[int] = None,
                    file_name: Optional[str] = None
                    ):
        LOGGING_CONFIG["handlers"] = {}
        LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"] = []

        # log_level 数据校验
        log_level = loglevel.strip().lower()
        if log_level not in ["debug", "info", "warning", "error"]:
            raise ValueError("expected APPBUILDER_LOGLEVEL in [debug, info, warning, error], but got %s" % log_level)
        log_level = log_level.upper()

        # 设置console输出日志
        if console_output:
            CONSOLE_HEADER['level'] = loglevel
            LOGGING_CONFIG["handlers"]["console"] = CONSOLE_HEADER
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("console")
        else:
            LOGGING_CONFIG["loggers"]["appbuilder"]["propagate"] = False

        # 参数验证
        if not max_file_size or max_file_size <= 0:
            max_file_size = sys.maxsize
        if not total_log_size or total_log_size <= 0:
            total_log_size = sys.maxsize
        if not max_log_files or max_log_files <= 0:
            max_log_files = sys.maxsize
        if rotate_interval < 1:
            rotate_interval = 1
        rotate_frequency = rotate_frequency.strip().lower()
        if rotate_frequency not in ["s", "m", "h", "d", "midnight"]:
            raise ValueError("expected rotate_frequency in [S, M, H, D, MIDNIGHT], but got %s" % rotate_frequency)

        # 设置文件输出日志
        # 设置日志级别
        SET_CONFIG_HEADER['level'] = loglevel

        # 设置文件名称
        if not file_name:
            current_pid = str(os.getpid())
        else:
            current_pid = file_name
        full_log_path = os.path.join(log_path, "log")
        if not os.path.exists(full_log_path):
            os.makedirs(full_log_path)
        info_log_file = os.path.join(log_path, "log", current_pid + ".info.log")
        error_log_file = os.path.join(log_path, "log", current_pid + ".error.log")
        SET_CONFIG_HEADER["file_name"] = info_log_file
        ERROR_SET_CONFIG_HEADER["file_name"] = error_log_file

        # 设置滚动时间
        SET_CONFIG_HEADER['rotate_frequency'] = rotate_frequency
        ERROR_SET_CONFIG_HEADER['rotate_frequency'] = rotate_frequency
        SET_CONFIG_HEADER['rotate_interval'] = rotate_interval
        ERROR_SET_CONFIG_HEADER['rotate_interval'] = rotate_interval

        # 设置最大文件大小

        SET_CONFIG_HEADER['max_file_size'] = max_file_size
        ERROR_SET_CONFIG_HEADER['max_file_size'] = max_file_size

        # 设置总大小限制
        SET_CONFIG_HEADER['total_log_size'] = total_log_size
        ERROR_SET_CONFIG_HEADER['total_log_size'] = total_log_size

        # 设置备份数量
        SET_CONFIG_HEADER['max_log_files'] = max_log_files
        ERROR_SET_CONFIG_HEADER['max_log_files'] = max_log_files

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
