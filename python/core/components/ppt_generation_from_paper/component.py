# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import traceback
import time

from typing import Optional

from .base import PPTGenerationFromPaperArgs, DEFAULT_AUTHOR

from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.utils.logger_util import logger


class PPTGenerationFromPaper(Component):
    """
    论文生成PPT。

    Examples:

    .. code-block:: python

        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = '...'

        ppt_generator = appbuilder.PPTGenerationFromPaper()
        user_input = {
            'file_key': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'
        }
        answer = ppt_generator(appbuilder.Message(user_input))
        print(answer.content)
    """
    uniform_prefix = '/api/v1/component/component'
    ppt_generation_url = '/ppt/text2ppt/apps/ppt-create-thesis'
    get_ppt_generation_status_url = '/ppt/text2ppt/apps/ppt-result'
    get_ppt_download_link_url = '/ppt/text2ppt/apps/ppt-download'

    name = 'ppt_generation_from_paper'
    version: str
    meta = PPTGenerationFromPaperArgs

    manifests = [
        {
            "name": "ppt_generation_from_paper",
            "description": "根据上传的论文生成PPT。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_key": {
                        "type": "string",
                        "description": "用户上传的论文的链接。"
                    }
                },
                "required": [
                    "file_key"
                ]
            }
        }
    ]

    def __init__(
        self, 
        secret_key: Optional[str] = None,
        gateway: str = "",
        lazy_certification: bool = False,
        **kwargs
    ):
        """初始化论文生成PPT组件。
        
        Args:
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        """
        super().__init__(PPTGenerationFromPaperArgs,
                         secret_key=secret_key,
                         gateway=gateway,
                         lazy_certification=lazy_certification)
        self.x_alternative_authorization = None

    def ppt_generation(self,
                       post_data: dict,
                       timeout: float = None):
        """
        创建PPT生成任务
        
        Args:
            post_data (dict): 发送的POST请求体数据
            timeout (float, optional): 请求超时时间，默认为None。
        
        Returns:
            str: 返回的任务ID
        
        Raises:
            Exception: 如果PPT生成请求失败，抛出异常
        
        """
        url = self.http_client.service_url(self.ppt_generation_url, self.uniform_prefix)
        headers = self.http_client.auth_header()
        if self.x_alternative_authorization:
            headers["X-Alternative-Authorization"] = self.x_alternative_authorization
        headers['Content-Type'] = 'application/json'
        response = self.http_client.session.post(url,
                                                 json=post_data,
                                                 headers=headers,
                                                 timeout=timeout)
        self.http_client.check_response_header(response)
        resp_data = response.json()
        if resp_data.get('code', None) != 200 or resp_data.get('msg', None) != 'success':
            error_msg = f'[ppt_generation] PPT generation request error! response: {resp_data}'
            logger.error(error_msg)
            raise Exception(error_msg)
        job_id = resp_data['data']['id']
        return job_id

    def get_ppt_generation_status(self,
                                  job_id: str,
                                  request_times: int = 60,
                                  request_interval: int = 5,
                                  timeout: float = None):
        """
        轮询查看PPT生成状态
        
        Args:
            job_id (str): 任务ID
            request_times (int, optional): 请求次数，默认为60次。
            request_interval (int, optional): 请求间隔时间，默认为5秒。
            timeout (float, optional): 请求超时时间，默认为None，即不设置超时时间。
        
        Returns:
            int: PPT生成状态码。
                - 1: PPT正在生成中
                - 2: PPT生成完成
                - 3: PPT生成失败
        
        Raises:
            Exception: PPT生成失败或请求失败时抛出异常。
        """
        url = self.http_client.service_url(self.get_ppt_generation_status_url, self.uniform_prefix) + f'?id={job_id}'
        headers = self.http_client.auth_header()
        if self.x_alternative_authorization:
            headers["X-Alternative-Authorization"] = self.x_alternative_authorization
        headers['Content-Type'] = 'application/json'

        status = -1
        for _ in range(request_times):
            response = self.http_client.session.get(url,
                                                    headers=headers,
                                                    timeout=timeout)
            try:
                self.http_client.check_response_header(response)
            except:
                error_msg = f'[get_ppt_generation_status] ERROR!\n{traceback.format_exc()}'
                logger.error(error_msg)
                time.sleep(request_interval)
                continue
            self.http_client.check_response_header(response)

            resp_data = response.json()
            if resp_data.get('code', None) != 200 or resp_data.get('msg', None) != 'success':
                error_msg = f'[get_ppt_generation_status] Get PPT generation status error! job_id: {job_id}, ' \
                            f'response: {resp_data}'
                logger.error(error_msg)
                raise Exception(error_msg)
            status = resp_data['data']['status']
            if status == 1:
                # 正在生成
                time.sleep(request_interval)
            elif status == 2:
                # 生成完成
                break
            elif status == 3:
                # 生成失败
                raise Exception(f'[get_ppt_generation_status] PPT generation Fail! job_id: {job_id}')
        
        if status == 1:
            error_msg = f'[get_ppt_generation_status] PPT generation timeout! job_id: {job_id}'
            logger.error(error_msg)
            raise Exception(error_msg)
        elif status == -1:
            error_msg = f'[get_ppt_generation_status] Request fail! job_id: {job_id}'
            logger.error(error_msg)
            raise Exception(error_msg)

        return status

    def get_ppt_download_link(self,
                              job_id: str,
                              timeout: float = None):
        """
        获取PPT下载链接
        
        Args:
            job_id (str): 任务ID
            timeout (float, optional): 请求超时时间，默认为None.
        
        Returns:
            str: PPT下载链接
        
        Raises:
            Exception: PPT生成请求失败
        
        """
        url = self.http_client.service_url(self.get_ppt_download_link_url, self.uniform_prefix) + f'?id={job_id}'
        headers = self.http_client.auth_header()
        if self.x_alternative_authorization:
            headers["X-Alternative-Authorization"] = self.x_alternative_authorization
        headers['Content-Type'] = 'application/json'
        response = self.http_client.session.get(url,
                                                headers=headers,
                                                timeout=timeout)
        self.http_client.check_response_header(response)
        resp_data = response.json()
        if resp_data.get('code', None) != 200 or resp_data.get('msg', None) != 'success':
            error_msg = f'[get_ppt_download_link] PPT generation request error! response: {resp_data}'
            logger.error(error_msg)
            raise Exception(error_msg)
        download_link = resp_data['data']['download_url']
        return download_link
    
    def run(self, message: Message, poll_request_times=60, poll_request_interval=5) -> Message:
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (Message): 输入消息，用于传入请求参数。
            poll_request_times (int): 轮询请求结果次数，默认为60次。
            poll_request_interval (int): 轮询请求的间隔时间（秒），默认为5秒。
        
        Returns:
            Message: 模型运行后的输出消息，包含PPT下载链接。
        
        Raises:
            Exception: 当输入参数中缺少必要的键时，抛出异常。
        
        """
        # 参数检查与设置
        user_input = message.content
        for key in ['file_key']:
            if key not in user_input:
                raise Exception(f'[PPTGenerationFromPaper] Missing key: {key}')
        if user_input.get('pleader', '') is None or not user_input.get('pleader', '').strip():
            user_input['pleader'] = DEFAULT_AUTHOR
        if user_input.get('advisor', '') is None or not user_input.get('advisor', '').strip():
            user_input['advisor'] = DEFAULT_AUTHOR
        user_input = self.meta(**{k: v for k, v in user_input.items() if v is not None})
        user_input = user_input.convert_params_to_dict()
        
        # 创建PPT生成任务
        logger.info('Creating a PPT generation task...')
        job_id = self.ppt_generation(user_input)
        logger.info('Creating a PPT generation task succeeds.')
        
        # 查询PPT生成状态
        logger.info('Generating PPT...')
        status = self.get_ppt_generation_status(job_id,
                                                request_times=poll_request_times,
                                                request_interval=poll_request_interval)
        logger.info('PPT generation task completed.')
        
        # 获取PPT下载链接
        logger.info('Getting PPT download link...')
        ppt_download_link = self.get_ppt_download_link(job_id)
        logger.info('Getting PPT download link succeeds.')

        return Message(ppt_download_link)

    def tool_eval(self, stream: bool = False, **kwargs):
        """
        使用指定的file_key来评估并获取相应的结果。
        
        Args:
            stream (bool, optional): 是否以生成器的方式逐项返回结果，默认为False。
            **kwargs: 关键字参数，用于传递其他参数，目前仅支持file_key。
        
        Returns:
            如果stream为False，则直接返回结果。
            如果stream为True，则逐个返回结果。
        
        Raises:
            ValueError: 如果参数file_key为空，则抛出异常。
        
        """
        file_key = kwargs.get('file_key', '')
        if not file_key:
            raise ValueError('param `file_key` should not be empty.')
        user_input = {
            'file_key': file_key
        }

        message = Message(user_input)
        result = self.run(message,
                          poll_request_times=60,
                          poll_request_interval=5)

        ppt_download_link = result.content

        if stream:
            yield ppt_download_link
        else:
            return ppt_download_link