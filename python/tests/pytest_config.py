
# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import os
from appbuilder.utils.logger_util import get_logger
log = get_logger(__name__)

class LoadConfig(object):
    """
    config
    """
    def __init__(self):
        """
        初始化函数，读取配置文件并设置实例属性。
        """
        self.token = os.environ.get("APPBUILDER_TOKEN", "")
        self.console_url = os.environ.get("GATEWAY_URL", "https://appbuilder.baidu.com")
        self.cookie =  os.environ.get("COOKIE", "")
        self.csrftoken = os.environ.get('CSRFTOKEN', "")

        log.info("token: %s" % self.token)
        log.info("console_url: %s" % self.console_url)
        log.info("cookie: %s" % self.cookie)
        log.info("csrftoken: %s" % self.csrftoken)




