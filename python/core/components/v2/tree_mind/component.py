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

r"""树图工具"""

import json
from urllib.parse import urlparse, unquote
from typing import Dict, List, Optional, Any
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import *
from appbuilder.core.utils import get_filename_from_url
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from appbuilder.core.components.v2.tree_mind.model import TreeMindRequest, TreeMindResponse


from appbuilder.core.component import Component

class TreeMind(Component):
    r"""
    树图工具，提供智能思维导图制作工具和丰富的模板，支持脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴、时间线等多种专业格式。
    .. code-block:: python
    
        import os
        import requests
        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["GATEWAY_URL"] = "..."
        os.environ["APPBUILDER_TOKEN"] = "..."
        treemind = appbuilder.TreeMind()
        resp = treemind.run(appbuilder.Message("生成一份年度总结的思维导图"), to_lang="en")
        print(resp.content)
        # 输出 {'from_lang':'zh', 'to_lang':'en', 'trans_result':[{'src':'你好','dst':'hello'},{'src':'中国','dst':'China'}]}
    """

    name = "tree_mind"
    version = "v1"
    manifests = [
            {
                "name": "tree_mind",
                "description": "根据用户输入的信息，生成详细智能思维导图、脑图、逻辑图、树形图、鱼骨图、组织架构图、时间轴、时间线等多种专业格式思维导图",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "用户想要生成思维导图的内容"
                        },
                    },
                    "required": [
                        "query"
                    ]
                }
            }
        ]

    def _post(self, query, **kwargs):
        if query is None or query == "":
            raise InvalidRequestArgumentError("query is empty!" )
        request = TreeMindRequest(query_text=query)
        headers = self.http_client.auth_header(kwargs.get("_sys_traceid"))

        headers['Content-Type'] = 'application/json'
        tree_mind_url = self.http_client.service_url("/v1/component/component/query_mind_open")

        payload = TreeMindRequest.model_dump(request)

        response = self.http_client.session.post(tree_mind_url, headers=headers, json=payload)
        self.http_client.check_response_header(response)
        data = response.text
        treemind_dict = json.loads(data.split("data:")[-1])
        treemind_response = TreeMindResponse(**treemind_dict)
        jump_link = treemind_response.info.downloadInfo.fileInfo.jumpLink
        img_link = treemind_response.info.downloadInfo.fileInfo.pic
        return img_link, jump_link

    @components_run_stream_trace
    def tool_eval(
            self,
            query,
            **kwargs,
    ):
        r"""调用树图查询接口
        Args:
            query (string): 用户想要生成思维导图的内容
        Returns:
            dict: 返回生成的思维导图的图片链接和跳转链接
        """

        img_link, jump_link = self._post(query, **kwargs)

        inst = "你必须遵循指令，输出无需总结，只需要将，“原样输出内容”对应的内容原样输出即可：\n"
        img_res = f"原样输出内容：![图片url]({img_link})\n"
        jump_res = f"{query}的思维导图已经为您生成好了，您可以通过这个链接编辑：编辑链接：{jump_link}。"
        end_talk = "如果您觉得这个思维导图还不够完美，或者您的想法需要更自由地表达，点击编辑按钮，对思维导图变形、变色、变内容、甚至可以添加新的元素，快来试试吧！"
        result = inst + img_res + jump_res + end_talk

        llm_result = self.create_output(
            type="text",
            text=result,
            visible_scope='llm',
            name="text",
            raw_data={"event_status": "done"}
        )
        yield llm_result
        
        img_link_result = self.create_output(
            type="image",
            text={
                "filename": get_filename_from_url(img_link),
                "url": img_link
            },
            visible_scope='all',
            name="img_link_url",
            raw_data={"event_status": "done"}
        )
        yield img_link_result

        jump_link_result = self.create_output(
            type="urls",
            text={
                "url": jump_link
            },
            visible_scope='all',
            name="jump_link_url"
        )
        yield jump_link_result


    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, **kwargs) -> Message:
        """运行组件
        Args:
            message (Message): 消息对象
        Returns:
            Message: 返回消息对象
        """
        query = message.content
        img_link, jump_link = self._post(query, **kwargs)

        result = {
            "result": "思维导图已经为您生成好了，您可以点击'img_link'对应的链接查看，如果您觉得这个思维导图还不够完美，或者您的想法需要更自由地表达，点击'edit_link'对应的链接，对思维导图变形、变色、变内容、甚至可以添加新的元素",
            "img_link": img_link,
            "edit_link": jump_link
        }
        return Message(content=result)