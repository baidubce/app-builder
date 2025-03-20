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

from .base import PPTGenerationFromInstructionArgs, DEFAULT_AUTHOR

from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.utils.logger_util import logger


class PPTGenerationFromInstruction(Component):
    """
    指令生成PPT，可通过传入对PPT的描述或者自定义参数进行生成。

    Examples:

        .. code-block:: python

            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = '...'

            ppt_generator = appbuilder.PPTGenerationFromInstruction()
            input_data = {
                'text': '生成一个介绍北京的PPT。',
                'custom_data': {},
                'complex': 3,
                'user_name': '百度千帆AppBuilder'
            }
            answer = ppt_generator(appbuilder.Message(input_data))
            print(answer.content)
    """
    uniform_prefix = '/api/v1/component/component'
    ppt_generation_url = '/ppt/text2ppt/apps/ppt-create'
    get_ppt_generation_status_url = '/ppt/text2ppt/apps/ppt-result'
    get_ppt_download_link_url = '/ppt/text2ppt/apps/ppt-download'

    name = 'ppt_generation_from_instruction'
    version: str
    meta = PPTGenerationFromInstructionArgs

    manifests = [
        {
            "name": "ppt_generation_from_instruction",
            "description": "根据输入指令生成PPT。",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "用户请求生成PPT的指令。",
                        "example": "生成一个介绍北京的PPT。"
                    }
                },
                "required": [
                    "text"
                ]
            }
        }
    ]

    def __init__(
        self, 
        secret_key: Optional[str] = None,
        gateway: str = '',
        lazy_certification: bool = False,
        **kwargs
    ):
        """初始化PPT生成组件。
        
        Args:
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        """
        super().__init__(PPTGenerationFromInstructionArgs,
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
            post_data (dict): 请求数据
            timeout (float, optional): 请求超时时间，默认为None.
        
        Returns:
            str: 任务ID
        
        Raises:
            Exception: PPT生成请求失败
        
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
            job_id (str): PPT生成任务的唯一标识符
            request_times (int, optional): 轮询请求的次数，默认为60次。
            request_interval (int, optional): 每次轮询请求之间的间隔时间（秒），默认为5秒。
            timeout (float, optional): 请求的超时时间（秒）。如果未设置，则使用http_client的默认超时时间。
        
        Returns:
            int: PPT生成状态码。
                - 1：正在生成
                - 2：生成完成
                - 3：生成失败
        
        Raises:
            Exception: PPT生成过程中出现异常时抛出。
        
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
            job_id (str): 作业ID
            timeout (float, optional): 请求超时时间，默认为None。
        
        Returns:
            str: PPT下载链接
        
        Raises:
            Exception: 当PPT生成请求失败时抛出异常
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
            poll_request_times (int, optional): 轮询请求结果次数，默认为60。
            poll_request_interval (int, optional): 轮询请求的间隔时间（秒），默认为5。
        
        Returns:
            Message: 模型运行后的输出消息，包含PPT下载链接。
        
        """
        # 参数检查与设置
        user_input = message.content
        for key in ['text', 'custom_data']:
            if key not in user_input:
                raise Exception(f'[PPTGeneration] Missing key: {key}')
        if user_input['custom_data']:
            author = user_input['custom_data'].get('author', '')
            if author is None or not author.strip():
                user_input['custom_data']['author'] = DEFAULT_AUTHOR
        if user_input.get('user_name', '') is None or not user_input.get('user_name', '').strip():
            user_input['user_name'] = DEFAULT_AUTHOR
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
        评估给定的文本内容。
        
        Args:
            stream (bool, optional): 是否以生成器形式返回结果，默认为False。如果为True，则逐个生成下载链接；如果为False，则直接返回下载链接。
            **kwargs: 关键字参数，可以传递其他参数，但当前只使用 'text' 参数。
        
        Returns:
            如果 stream 为 False，则返回一个包含下载链接的字符串；如果 stream 为 True，则逐个生成下载链接。
        
        Raises:
            ValueError: 如果 'text' 参数为空，则抛出此异常。
        
        """
        text = kwargs.get('text', '')
        if not text:
            raise ValueError('param `text` should not be empty.')
        user_input = {
            'text': text,
            'custom_data': {}
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