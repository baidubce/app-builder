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


# -*- coding: utf-8 -*-
"""
文本翻译-通用版组件
"""
import json

from appbuilder.core.message import Message
from appbuilder.core.component import Component
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.translate.model import *


class Translation(Component):
    """
    文本翻译组件,可支持中、英、日、韩等200+语言互译，100+语种自动检测。
    支持语种列表可参照 https://ai.baidu.com/ai-doc/MT/4kqryjku9#%E8%AF%AD%E7%A7%8D%E5%88%97%E8%A1%A8


    Examples:

            .. code-block:: python

                import appbuilder

                # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
                os.environ["APPBUILDER_TOKEN"] = '...'

                translate = appbuilder.Translation()
                resp = translate(appbuilder.Message("你好\n中国"), to_lang="en")
                # 输出 {'from_lang':'zh', 'to_lang':'en', 'trans_result':[{'src':'你好','dst':'hello'},{'src':'中国','dst':'China'}]}
                print(resp.content)
    """

    name = "translate"
    version = "v1"

    def run(self, message: Message, from_lang: str = "auto", to_lang: str = "en",
            timeout: float = None, retry: int = 0) -> Message:
        """
        根据提供的文本以及语种参数执行文本翻译

        Args:
            message (Message): 翻译文本。
            from_lang (str): 翻译的源语言。默认为 "auto"。
            to_lang (str): 翻译的目标语言。默认为 "en"。
            timeout (float, optional): 翻译请求的超时时间。
            retry (int, optional): 重试次数。

        Returns:
            Message: 返回的文本翻译结果。
            例如，Message(content={'from_lang': 'zh', 'to_lang': 'en', 'trans_result': [{'src': '你好', 'dst': 'hello'}]})
        """
        req = TranslateRequest()
        req.q = message.content
        req.from_lang = from_lang
        req.to_lang = to_lang
        result = self._translate(req, timeout=timeout, retry=retry)
        result_dict = proto.Message.to_dict(result)

        out = TranslateOutMsg(**result_dict["result"])
        return Message(content=out.dict())

    def _translate(self, request: TranslateRequest, timeout: float = None,
                   retry: int = 0) -> TranslateResponse:
        """
        根据提供的 TranslateRequest 执行文本翻译。

        Args:
            request (TranslateRequest): 翻译请求参数。
            timeout (float, optional): 请求超时时间。
            retry (int, optional): 重试次数。

        Returns:
            TranslateResponse: 文本翻译结果的响应体。
        """
        if not request.to_lang or not request.q:
            raise ValueError("params `to_lang` and `q` must be set")
        if not request.from_lang:
            request.from_lang = "auto"
        request_data = TranslateRequest.to_json(request)
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/json;charset=utf-8'

        url = self.http_client.service_url("/v1/bce/aip/mt/texttrans/v1")

        response = self.http_client.session.post(url, headers=headers, data=request_data, timeout=timeout)

        self.http_client.check_response_header(response)
        data = response.json()
        request_id = self.http_client.response_request_id(response)
        self.http_client.check_response_json(data)
        if "error_code" in data and "error_msg" in data:
            raise AppBuilderServerException(request_id=request_id, service_err_code=data["error_code"], service_err_message=data["error_msg"])

        json_str = json.dumps(data)
        return TranslateResponse(TranslateResponse.from_json(json_str))
