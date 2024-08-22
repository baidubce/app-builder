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
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core.components.llms.base import CompletionResponse


class ParseRagProResponse(CompletionResponse):

    def __init__(self, response, stream: bool = False):
        """初始化客户端状态。"""
        super().__init__(response, stream)
        self.error_no = 0
        self.error_msg = ""
        self.log_id = response.headers.get("X-Appbuilder-Request-Id", None)
        self.extra = {}
        self.token_usage = {}

        if stream:
            # 流式数据处理
            def stream_data():
                sse_client = SSEClient(response)
                for event in sse_client.events():
                    if not event:
                        continue
                    answer = self.parse_stream_data(event)
                    if answer is not None:
                        yield answer

            self.result = stream_data()
        else:
            # 非流式数据的处理
            if response.status_code != 200:
                self.error_no = response.status_code
                self.error_msg = "error"
                self.result = response.text

                raise AppBuilderServerException(self.log_id, self.error_no, self.result)

            else:
                data = response.json()

                if "code" in data and "message" in data and "requestId" in data:
                    raise AppBuilderServerException(self.log_id, data["code"], data["message"])

                if "code" in data and "message" in data and "status" in data:
                    raise AppBuilderServerException(self.log_id, data["code"], data["message"])

                res = data["result"]
                answer_message = res.get("answer_message")
                self.result = answer_message.get("content")
                self.token_usage = answer_message.get("token_usage", {})
                # 拼装百度搜索的结果
                extra = answer_message.get("extra")
                search_baidu_list = []

                for item in extra:
                    search_baidu_list.append({
                        "content": item.get("content"),
                        "icon": item.get("icon"),
                        "url": item.get("url"),
                        "ref_id": item.get("ref_num"),
                        "site_name": item.get("web_anchor"),
                        "title": item.get("title")
                    })
                self.extra = {
                    "search_baidu": search_baidu_list
                }

    def message_iterable_wrapper(self, message):
        """
        对模型输出的 Message 对象进行包装。
        当 Message 是流式数据时，数据被迭代完后，将重新更新 content 为 blocking 的字符串。
        """

        class IterableWrapper:
            def __init__(self, stream_content):
                self._content = stream_content
                self._concat = ""
                self._token_usage = {}

            def __iter__(self):
                return self

            def __next__(self):
                try:
                    result_json = next(self._content)

                    res = result_json["result"]
                    answer_message = res.get("answer_message")
                    char = answer_message.get("content", "")

                    extra = answer_message.get("extra")
                    if extra is not None:
                        search_baidu_list = []
                        for item in extra:
                            search_baidu_list.append({
                                "content": item.get("content"),
                                "icon": item.get("icon"),
                                "url": item.get("url"),
                                "ref_id": item.get("ref_num"),
                                "site_name": item.get("web_anchor"),
                                "title": item.get("title")
                            })
                        message.extra = {
                            "search_baidu": search_baidu_list
                        }
                    else:
                        message.extra = {}
                    if "token_usage" in answer_message:
                        self._token_usage = answer_message.get("token_usage")
                        message.token_usage = self._token_usage
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
