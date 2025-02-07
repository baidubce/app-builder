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
ernie bot embedding
"""

from typing import Union, List

from appbuilder.core.message import Message
from appbuilder.core.components.embeddings.base import EmbeddingBaseComponent
from appbuilder.core._exception import AppBuilderServerException, ModelNotSupportedException
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import EmbeddingArgs

class Embedding(EmbeddingBaseComponent):
    """
    Embedding

    Embedding-V1是基于百度文心大模型技术的文本表示模型，将文本转化为用数值表示的向量形式，用于文本检索、信息推荐、知识挖掘等场景。

    Attributes:
        model: str = "Embedding-V1"

    Examples:

        .. code-block:: python

            import appbuilder
            from appbuilder import Message

            os.environ["APPBUILDER_TOKEN"] = '...'

            embedding = appbuilder.Embedding()

            embedding_single = embedding(Message("hello world!"))

            embedding_batch = embedding.batch(Message(["hello", "world"]))
    """

    name: str = "embedding"
    version: str = "v1"

    meta = EmbeddingArgs
    accepted_models = ["Embedding-V1"]

    base_urls = {
        'Embedding-V1' : "/v1/bce/wenxinworkshop/ai_custom/v1/embeddings/embedding-v1"
    }

    def __init__(self, 
                 model="Embedding-V1",
                 **kwargs
                 ):
        """Embedding"""

        if model not in self.accepted_models:
            raise ModelNotSupportedException(f"Model {model} not supported, only support {self.accepted_models}")

        if model in self.base_urls:
            self.base_url = self.base_urls[model]
        else:
            raise ModelNotSupportedException(f"Model {model} is not yet supported, only support {self.base_urls.keys()}")

        super().__init__(self.meta)

    def _check_response_json(self, data: dict):
        """
        check_response_json for embedding
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
            url=self.http_client.service_url(self.base_url),
            headers=headers,
            json=payload,
        )
        self.http_client.check_response_header(resp)
        self._check_response_json(resp.json())

        return resp.json()

    def _batchify(self, texts: List[str], batch_size: int = 16) -> List[List[str]]:
        """
        batchify input text list
        """
        if batch_size > 16:
            raise ValueError(f"The max Embedding batch_size is 16, but got {batch_size}")

        return [
            texts[i : i + batch_size] for i in range(0, len(texts), batch_size)
        ]

    def _batch(self, texts: List[str]) -> Message[List[List[float]]]:
        """
        batch run implement
        """
        batches = self._batchify(texts)
        results = []
        for batch in batches:
            result = self._request({"input": batch})
            results.extend(result['data'])
        results = Message([result['embedding'] for result in results])

        return results

    @components_run_trace
    def run(self, text: Union[Message[str], str]) -> Message[List[float]]:
        """
        处理给定的文本或消息对象，并返回包含处理结果的消息对象。
        
        Args:
            text (Union[Message[str], str]): 待处理的文本或消息对象。
        
        Returns:
            Message[List[float]]: 处理后的结果，封装在消息对象中。结果是一个浮点数列表。
        """
        _text = text if isinstance(text, str) else text.content

        return Message(self._batch([_text]).content[0])

    def batch(self, texts: Union[Message[List[str]], List[str]]) -> Message[List[List[float]]]:
        """
        批量处理文本数据。
        
        Args:
            texts (Union[Message[List[str]], List[str]]):
                待处理的文本数据，可以是 Message 类型，包含多个文本列表，也可以是普通列表类型，包含多个文本。
        
        Returns:
            Message[List[List[float]]]:
                处理后的结果，为 Message 类型，包含一个二维浮点数列表，每个子列表对应输入文本列表中一个文本的处理结果。
        
        """
        _texts = texts if isinstance(texts, list) else texts.content

        return self._batch(_texts)
