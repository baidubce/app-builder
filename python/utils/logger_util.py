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
import json
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
        }
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
    'level': 'INFO',
    'filename': "",
    'when': 'midnight',  # 可选项: 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight'
    'interval': 1,       # 每1天滚动一次
    'backupCount': 5,    # 保留5个备份
    'encoding': 'utf-8',
}

TIME_HANDLERS_FILE_ERROR = {
    'class': 'logging.handlers.TimedRotatingFileHandler',
    'formatter': 'standard',
    'level': 'ERROR',
    'filename': "",
    'when': 'midnight',  # 可选项: 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight'
    'interval': 1,       # 每1天滚动一次
    'backupCount': 5,    # 保留5个备份
    'encoding': 'utf-8',
}

SIMPLE_HANDLERS_FILE = {
    "level": "INFO",
    "class": "logging.FileHandler",
    "filename": "",
    "formatter": "standard",
}

SIMPLE_HANDLERS_FILE_ERROR = {
    "level": "ERROR",
    "class": "logging.FileHandler",
    "filename": "",
    "formatter": "standard",
}

def _update_error_file_name(filename:str):
    """
    更新文件名，使其以 "error." 开头。
    
    Args:
        filename (str): 原始文件名。
    
    Returns:
        str: 更新后的文件名。
    
    Raises:
        无
    
    """
    filenames = filename.split('/')
    filenames[-1] = f"error.{filenames[-1]}"
    return '/'.join(filenames)

class LoggerWithLoggerId(logging.LoggerAdapter):
    """
    logger with logid
    """
    def __init__(self, logger, extra, loglevel):
        """
        初始化LoggerAdapter实例。
        
        Args:
            logger (logging.Logger): 日志记录器实例。
            extra (dict): 用于日志记录的额外上下文信息。
            loglevel (str): 日志级别，如'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'。
        
        Returns:
            None
        
        """
        log_file = os.environ.get("APPBUILDER_LOGFILE", "")
        if log_file:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handler"] = ["console"] # 默认使用console

            SIMPLE_HANDLERS_FILE["level"] = loglevel
            TIME_HANDLERS_FILE['level'] = loglevel
            SIMPLE_HANDLERS_FILE["filename"] = log_file
            SIMPLE_HANDLERS_FILE_ERROR["filename"] = _update_error_file_name(log_file)
            LOGGING_CONFIG["handlers"]["file"] = SIMPLE_HANDLERS_FILE 
            LOGGING_CONFIG["handlers"]["error_file"] = SIMPLE_HANDLERS_FILE_ERROR
            if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
            if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
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
            rolling:bool=True, 
            update_interval:int=1, 
            update_time:str='midnight', 
            backup_count:int=0, 
            filename:str=''
            ):
        """
        设置日志配置。
        
        Args:
            rolling (bool): 是否开启日志滚动。默认为True。
            update_interval (int): 日志滚动更新的时间间隔。默认为1。
            update_time (str): 日志滚动更新的时间单位。默认为'midnight'。
            backup_count (int): 日志备份数量。默认为0。
            filename (str): 日志文件名。默认为空字符串。
        
        Returns:
            None
        
        Raises:
            ValueError: 如果update_time参数的值不在预期的范围内。
        
        """
        # 配置控制台输出
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
        if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")

        # 确定备份数量
        if backup_count <= 0 or not isinstance(backup_count, int):
            backup_count = sys.maxsize # 默认为无穷大

        # 确定滚动时间
        if update_interval < 1:
            update_interval = 1
        if update_time:
            update_time = update_time.lower()
            if update_time not in ['s', 'm', 'h', 'd', 'midnight'] and not (update_time.startswith('w') and update_time[1:].isdigit() and 0 <= int(update_time[1:]) <= 6):
                raise ValueError("expected update_time in [S, M, H, D, midnight, WX], where X is between 0~6, but got %s")
            else:
                update_time = update_time.upper()

        # 设置filename
        if not filename:

            filename = (SIMPLE_HANDLERS_FILE.get("filename") or
                        TIME_HANDLERS_FILE.get("filename") or 
                        "tmp.log")
            

        # 创建处理器
        if rolling:
            if update_time:
                TIME_HANDLERS_FILE['when'] = update_time
                TIME_HANDLERS_FILE_ERROR['when'] = update_time
                TIME_HANDLERS_FILE['interval'] = update_interval
                TIME_HANDLERS_FILE_ERROR['interval'] = update_interval
                TIME_HANDLERS_FILE['backupCount'] = backup_count
                TIME_HANDLERS_FILE_ERROR['backupCount'] = backup_count
                TIME_HANDLERS_FILE['filename'] = filename
                TIME_HANDLERS_FILE_ERROR['filename'] = _update_error_file_name(filename)
                if 'file' in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                    LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("file")
                if 'error_file' in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                    LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("error_file")
                if not "timed_file" in LOGGING_CONFIG["handlers"]:
                    LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append('timed_file')
                if not "error_timed_file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                    LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append('error_timed_file')
                LOGGING_CONFIG["handlers"]["timed_file"] = TIME_HANDLERS_FILE
                LOGGING_CONFIG["handlers"]["error_timed_file"] = TIME_HANDLERS_FILE_ERROR
                LOGGING_CONFIG["handlers"]["timed_file"]["level"] = LOGGING_CONFIG['loggers']['appbuilder']['level']
        else:
            SIMPLE_HANDLERS_FILE["filename"] = filename
            SIMPLE_HANDLERS_FILE_ERROR["filename"] = _update_error_file_name(filename)
            LOGGING_CONFIG["handlers"]["file"] = SIMPLE_HANDLERS_FILE
            LOGGING_CONFIG["handlers"]["error_file"] = SIMPLE_HANDLERS_FILE_ERROR
            if "timed_file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("timed_file")
            if "error_timed_file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("error_timed_file")
            if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
            if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
                LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
            LOGGING_CONFIG["handlers"]["file"]["level"] = LOGGING_CONFIG['loggers']['appbuilder']['level']

        logging.config.dictConfig(LOGGING_CONFIG)

    def setFilename(self, filename):
        """
        设置日志文件和错误日志文件的文件名，并取消日志文件的滚动功能。
        
        Args:
            filename (str): 要设置的日志文件和错误日志文件的文件名。
        
        Returns:
            None
        
        说明:
            1. 如果LOGGING_CONFIG配置中存在"timed_file"和"error_timed_file"处理器，则从"appbuilder"日志记录器的处理器列表中移除它们。
            2. 如果"file"和"error_file"处理器不在"appbuilder"日志记录器的处理器列表中，则将它们添加到列表中。
            3. 更新SIMPLE_HANDLERS_FILE和SIMPLE_HANDLERS_FILE_ERROR配置中的"filename"为传入的文件名。
            4. 使用_update_error_file_name函数更新错误日志文件的名称。
            5. 更新LOGGING_CONFIG配置中的"handlers"下的"file"和"error_file"处理器配置。
            6. 调用logging.config.dictConfig函数重新配置日志系统。
        """
        if "timed_file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("timed_file")
        if "error_timed_file" in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].remove("error_timed_file")
        if "file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("file")
        if "error_file" not in LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"]:
            LOGGING_CONFIG["loggers"]["appbuilder"]["handlers"].append("error_file")
        SIMPLE_HANDLERS_FILE["filename"] = filename
        SIMPLE_HANDLERS_FILE_ERROR["filename"] = _update_error_file_name(filename)
        LOGGING_CONFIG["handlers"]["file"] = SIMPLE_HANDLERS_FILE
        LOGGING_CONFIG["handlers"]["error_file"] = SIMPLE_HANDLERS_FILE_ERROR
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
        SIMPLE_HANDLERS_FILE["level"] = log_level
        TIME_HANDLERS_FILE['level'] = log_level
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
