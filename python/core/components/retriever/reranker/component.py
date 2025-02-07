# -*- coding: utf-8 -*-

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

""" Reranker 文本精排
"""
from typing import Union, List

from appbuilder.core.message import Message
from appbuilder.core.component import Component, Message
from appbuilder.core._exception import AppBuilderServerException, ModelNotSupportedException
from appbuilder.utils.trace.tracer_wrapper import components_run_trace

from .model import RerankerArgs


class Reranker(Component):
    """ 
    Reranker

    Examples:

    .. code-block:: python

        import os
        import appbuilder
        from appbuilder import Message

        os.environ["APPBUILDER_TOKEN"] = '...'

        reranker = appbuilder.Reranker()
        ranked_1 = reranker("你好", ["他也好", "hello?"])
        print(ranked_1)
    """
    name: str = "reranker"
    version: str = "v1"

    meta = RerankerArgs
    base_urls = {
        'bce-reranker-base' : "/api/v1/component/component/bce_reranker_base"
    }
    accepted_models = list(base_urls.keys())

    def __init__(self, 
                 model="bce-reranker-base",
                 **kwargs
                 ):
        """Reranker"""

        if model not in self.accepted_models:
            raise ModelNotSupportedException(f"Model {model} not supported, only support {self.accepted_models}")

        if model in self.base_urls:
            self.base_url = self.base_urls[model]
        else:
            raise ModelNotSupportedException(f"Model {model} is not yet supported, only support {self.base_urls.keys()}")

        super().__init__(self.meta)

    def _check_response_json(self, data: dict):
        """
        check_response_json
        """

        self.http_client.check_response_json(data)
        if "error_code" in data and "error_msg" in data:
            raise AppBuilderServerException(
                service_err_code=data['error_code'],
                service_err_message=data['error_msg'],
            )

    def _request(self, payload: dict) -> dict:
        """
        request to gateway
        """
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        resp = self.http_client.session.post(
            url=self.http_client.service_url(self.base_url, "/"),
            headers=headers,
            json=payload,
        )
        self.http_client.check_response_header(resp)
        self._check_response_json(resp.json())

        return resp.json()

    def _batch(self, query, texts: List[str]) -> List[dict]:
        """
        batch run implement
        """
        if len(texts) > 50:
            raise ValueError(f'Rerank texts max nums must be lower than 50, but got {len(texts)}')
        for v in texts:
            if not isinstance(v, str):
                raise ValueError(f'Rerank texts must be str, but got {v}')

        params = {
            "inputs": {
                "query": query,
                "texts": texts
            }
        }
        result = self._request(params)
        result = result["result"]
        return result

    @components_run_trace
    def run(self, query: Union[Message[str], str],
            texts: Union[Message[List[str]], List[str]]) -> Message[List[dict]]:
        """
        运行查询，对给定的文本集合进行批量处理，并返回处理后的结果列表。
        
        Args:
            query (Union[Message[str], str]): 查询条件，可以是字符串或Message对象。
            texts (Union[Message[List[str]], List[str]]): 待处理的文本集合，可以是字符串列表或包含字符串列表的Message对象。
        
        Returns:
            Message[List[dict]]: 处理后的结果列表，每个元素是一个字典，包含处理后的文本信息。
        """
        _query = query if isinstance(query, str) else query.content
        _texts = texts if isinstance(texts, List) else texts.content

        return Message(self._batch(_query, _texts))
