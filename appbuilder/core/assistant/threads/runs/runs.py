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
import json
from typing import Optional
from appbuilder.core.assistant.type import thread_type
from appbuilder.core.assistant.type import assistant_type
from appbuilder.core._client import AssistantHTTPClient
from appbuilder.utils.sse_util import SSEClient


class Runs():
    def __init__(self) -> None:
        self._http_client = AssistantHTTPClient()

    def run(self,
            assistant_id: str,
            thread_id: Optional[str] = "",
            thread: Optional[thread_type.AssistantThread] = None,
            model: Optional[str] = "ERNIE-4.0-8K",
            response_format: Optional[str] = "text",
            instructions: Optional[str] = "",
            thought_instructions: Optional[str] = "",
            chat_instructions: Optional[str] = "",
            tools: Optional[list[assistant_type.AssistantTool]] = [],
            metadata: Optional[dict] = {},
            tool_output: Optional[thread_type.ToolOutput] = None,
            ) -> thread_type.RunResult:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs")

        """
        注意：
            1. 若thread_id没有传，则thread必须要传值
            2. 若这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
            3. 若这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
        """
        if thread_id == "" and thread is None:
            raise ValueError("Runs().run() 参数thread_id和thread不能同时为空")

        req = thread_type.AssistantRunRequest(
            thread_id=thread_id,
            thread=thread,
            model=model,
            assistant_id=assistant_id,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            stream=False,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp

    def stream_run(self,
                   assistant_id: str,
                   thread_id: Optional[str] = "",
                   thread: Optional[thread_type.AssistantThread] = None,
                   model: Optional[str] = "ERNIE-4.0-8K",
                   response_format: Optional[str] = "text",
                   instructions: Optional[str] = "",
                   thought_instructions: Optional[str] = "",
                   chat_instructions: Optional[str] = "",
                   tools: Optional[list[assistant_type.AssistantTool]] = [],
                   metadata: Optional[dict] = {},
                   tool_output: Optional[thread_type.ToolOutput] = None,
                   ):
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs")

        """
        注意：
            1. 若thread_id没有传，则thread必须要传值
            2. 若这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
            3. 若这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
        """
        if thread_id == "" and thread is None:
            raise ValueError("Runs().run() 参数thread_id和thread不能同时为空")

        req = thread_type.AssistantRunRequest(
            thread_id=thread_id,
            thread=thread,
            model=model,
            assistant_id=assistant_id,
            response_format=response_format,
            instructions=instructions,
            thought_instructions=thought_instructions,
            chat_instructions=chat_instructions,
            stream=True,
            tools=tools,
            metadata=metadata,
            tool_output=tool_output
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            stream=True,
            timeout=None
        )
        self._http_client.check_response_header(response)
        sse_client = SSEClient(response)
        return self._iterate_events(sse_client.events())

    def _iterate_events(self, events):
        for event in events:
            try:
                event_class = event.event
                if event_class == "ping":
                    # TODO(chengmo): record ping event, add timeout func
                    continue

                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)

                if event_class == "status":
                    result = thread_type.StreamRunStatus(**data)
                elif event_class == "message":
                    result = thread_type.StreamRunMessage(**data)

            except Exception as e:
                print(e)

            yield result

    def submit_tool_outputs(self,
                            run_id: str,
                            thread_id: str,
                            tool_outputs: Optional[list[thread_type.ToolOutput]]) -> thread_type.RunResult:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/submit_tool_outputs")

        req = thread_type.AssistantSubmitToolOutputsRequest(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp

    def cancel(self, run_id: str, thread_id: str) -> thread_type.RunResult:
        headers = self._http_client.auth_header()
        url = self._http_client.service_url("/v2/threads/runs/cancel")

        req = thread_type.AssistantRunCancelRequest(
            run_id=run_id,
            thread_id=thread_id
        )
        
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        self._http_client.check_response_header(response)

        data = response.json()
        request_id = self._http_client.response_request_id(response)
        self._http_client.check_assistant_response(request_id, data)

        resp = thread_type.RunResult(**data)
        return resp


if __name__ == "__main__":
    os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"

    from appbuilder.core.assistant.assistants import Assistants
    assistant = Assistants().create(
        name="Abc-_123",
        description="服务机器人"
    )

    from appbuilder.core.assistant.threads import Threads
    thread = Threads().create()

    from appbuilder.core.assistant.threads import Messages
    Messages().create(
        thread_id=thread.id,
        content="hello"
    )

    result = Runs().stream_run(
        assistant_id=assistant.id,
        thread_id=thread.id,
        instructions="每句话开头加上我是秦始皇")
    # print(result)
    for r in result:
        print("\n-------")
        print(r)
        print("-------\n")
