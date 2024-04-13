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
from typing import Union
from appbuilder.utils.collector import Collector
from appbuilder.utils.collector import AssistantKeys
from appbuilder.core.assistants import data_class
from appbuilder.core._client import HTTPClient
from appbuilder.utils.sse_util import SSEClient
from appbuilder.core.assistants.assistant_config import AssistantConfig
from appbuilder.core.assistants.assistants import Assistant, Assistants
from appbuilder.core.assistants.conversations.conversations import Conversation, Conversations
from appbuilder.core._exception import AppBuilderServerException


class Runs():
    def __init__(self) -> None:
        self._http_client = HTTPClient()

    def _find_or_retrieve_assistant(self, assistant_id: str) -> Assistant:
        assistant = Collector().get_collection(
            AssistantKeys.ASSISTANT, assistant_id)
        if not assistant:
            raise Exception(
                "Assistant with id {} does not exist".format(assistant_id))
        return assistant

    def run(self, assistant_id: str, conversation_id: Union[str, None] = None, assistant_config: Union[AssistantConfig, None] = None, extra_conversation_id: Union[str, None] = None, tool_output=None) -> data_class.RunResult:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] = os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/threads/runs"

        assistant = self._find_or_retrieve_assistant(assistant_id)
        final_assistants_config = assistant.assistant_config.to_base_model() if assistant_config is None \
            else assistant_config.merge(assistant_config)

        # 使用final_assistants_config来构造req
        req = data_class.AssistantRunRequest()
        for k, v in req.__dict__.items():
            if k in final_assistants_config:
                req.__setattr__(k, final_assistants_config[k])

        req.assistant_id = assistant.id
        req.model = "ERNIE-4.0-8K"
        req.thread_id = conversation_id if conversation_id is not None else ""
        req.stream = False
        # req.thread = extra_conversation_id
        req.tool_output = tool_output

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )
        data = response.json()
        resp = data_class.RunResult(**data)
        return resp

    def stream_run(self, assistant_id: str, conversation_id: str, assistant_config=None, extra_conversation=None, tool_output=None):
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] = os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/threads/runs"

        assistant = self._find_or_retrieve_assistant(assistant_id)
        final_assistants_config = assistant.assistant_config.to_base_model() if assistant_config is None \
            else assistant_config.merge(assistant_config)

        # 使用final_assistants_config来构造req
        req = data_class.AssistantRunRequest()
        for k, v in req.__dict__.items():
            if k in final_assistants_config:
                req.__setattr__(k, final_assistants_config[k])

        req.assistant_id = assistant.id
        req.model = "ERNIE-4.0-8K"
        req.thread_id = conversation_id if conversation_id is not None else ""
        req.stream = True
        # req.thread = extra_conversation_id
        req.tool_output = tool_output

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )

        sse_client = SSEClient(response)
        return self._iterate_events(sse_client.events())

    def _iterate_events(self, events):
        for event in events:
            try:
                event_class = event.event
                if event_class == "ping":
                    # TODO: record ping event, add timeout func
                    continue

                data = event.data
                if len(data) == 0:
                    data = event.raw
                data = json.loads(data)

                if event_class == "status":
                    result = data_class.StreamRunStatus(**data)
                elif event_class == "message":
                    result = data_class.StreamRunMessage(**data)

            except Exception as e:
                print(e)

            yield result

    def submit_tool_outputs(self, run_id: str, conversation_id: str, tool_outputs: Union[list[data_class.ToolOutput], None]) -> data_class.RunResult:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] = os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/threads/runs/submit_tool_outputs"

        req = data_class.AssistantSubmitToolOutputsRequest(
            thread_id=conversation_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )

        data = response.json()
        resp = data_class.RunResult(**data)
        return resp

    def cancel(self, run_id: str, conversation_id: str) -> data_class.RunResult:
        headers = self._http_client.auth_header()
        headers['Content-Type'] = 'application/json'
        headers["Authorization"] = os.getenv("APPBUILDER_TOKEN", "")

        url = "http://10.45.86.48/api/v1/threads/runs/cancel"

        req = data_class.AssistantRunCancelRequest(
            run_id=run_id,
            thread_id=conversation_id
        )
        response = self._http_client.session.post(
            url=url,
            headers=headers,
            json=req.model_dump(),
            timeout=None
        )

        data = response.json()
        resp = data_class.RunResult(**data)
        return resp


if __name__ == "__main__":
    os.environ["GATEWAY_URL"] = "http://10.45.86.48/"
    os.environ["APPBUILDER_TOKEN"] = "Bearer bce-v3/ALTAK-6AGZK6hjSpZmEclEuAWje/6d2d2ffc438f9f2ba66e23b21de69d96e7e5713a"

    assistant_config = AssistantConfig(
        name="test_assistant",
        description="test_desc",
        instructions="say nihao"
    )
    assistant = Assistants().create(assistant_config)

    message = data_class.AssistantMessage(content="hello")
    conversation = Conversations().create([message])

    result = Runs().stream_run(assistant.id, conversation.id)
    for r in result:
        print("\n-------")
        print(r)
        print("-------\n")
