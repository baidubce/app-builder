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
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.llms.base import CompletionResponse, LLMMessage


class ConsoleLLMMessage(LLMMessage):
    conversation_id: str = ""

    def __str__(self):
        return f"Message(name={self.name}, content={self.content}, mtype={self.mtype}, extra={self.extra}, conversation_id={self.conversation_id})"


class ConsoleCompletionResponse(CompletionResponse):
    """
    console端大模型返回结果解析
    """
    error_no = 0
    error_msg = ""
    result = None
    log_id = ""
    extra = None
    conversation_id = ""

    def __init__(self, response, stream: bool = False):
        """初始化客户端状态。"""
        super().__init__(response, stream)
        self.error_no = 0
        self.error_msg = ""
        self.log_id = response.headers.get("X-Appbuilder-Request-Id", None)
        self.extra = {}
        
        if not stream:
        
            data = response.json()

            if "code" in data and data.get("code") != 0:
                raise AppBuilderServerException(self.log_id, data["code"], data["message"])

            self.result = data.get("result").get("answer", None)
            self.conversation_id = data.get("result").get("conversation_id", "")
            content = data.get("result").get("content", None)
            if content:
                for item in content:
                    if item.get("content_type") == "references":
                        references = item.get("outputs").get("references")
                        if references:
                            for ref in references:
                                key = ref["from"]
                                if key in self.extra.keys():
                                    self.extra[key].append(ref)
                                else:
                                    self.extra[key] = [ref]

    def message_iterable_wrapper(self, message):
        """
        对模型输出的 Message 对象进行包装。
        当 Message 是流式数据时，数据被迭代完后，将重新更新 content 为 blocking 的字符串。
        """

        class IterableWrapper:
            def __init__(self, stream_content):
                self._content = stream_content
                self._concat = ""
                self._extra = {}

            def __iter__(self):
                return self

            def __next__(self):
                try:
                    resp = next(self._content)
                    result_json = resp.get("result")
                    char = result_json.get("answer", "")
                    conversation_id = result_json.get("conversation_id", "")
                    content = result_json.get("content", None)
                    if content:
                        for item in content:
                            if item.get("content_type") == "references":
                                references = item.get("outputs").get("references")
                                if references:
                                    for ref in references:
                                        key = ref["from"]
                                        if key in self._extra.keys():
                                            self._extra[key].append(ref)
                                        else:
                                            self._extra[key] = [ref]
                    message.extra = self._extra  # Update the original extra
                    message.conversation_id = conversation_id
                    self._concat += char
                    return char
                except StopIteration:
                    message.content = self._concat  # Update the original content
                    raise

        from collections.abc import Generator
        if isinstance(message.content, Generator):
            # Replace the original content with the custom iterable
            message.content = IterableWrapper(message.content)
        return message

    def to_message(self):
        """将响应结果转换为Message对象。

        Returns:
            Message: Message对象。

        """
        message = ConsoleLLMMessage()
        message.id = self.log_id
        message.content = self.result
        message.extra = self.extra
        message.conversation_id = self.conversation_id
        return self.message_iterable_wrapper(message)
