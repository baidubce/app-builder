"""
Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os

import requests

import json
from typing import Optional
from appbuilder.core.components.document_understanding.base import DocumentUnderstandingArgs

from appbuilder.core.message import Message
from appbuilder.core.component import Component
import base64

class DocumentUnderstanding(Component):
    """
    DocumentUnderstanding
    """
    name = "document_understanding"
    version = "v1"
    meta = DocumentUnderstandingArgs
    manifests = [{
        "name": "document_understanding",
        "description": "该工具支持对图片以及文档内容进行理解，并基于图片以及文档内容对用户的提问进行回答，包括但不限于文档内容问答、"
                       "总结摘要、内容分析。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "用户输入的query"
                },
                "file_path": {
                    "type": "string",
                    "description": "用户上传的文档的文件路径"
                },
                "instruction": {
                    "type": "string",
                    "description": "用户指令"
                },
                "addition_instruction": {
                    "type": "string",
                    "description": "用户增强指令"
                },
            },
            "required": ["query", "file_path", "instruction", "addition_instruction"]
        }
    }]
    def __init__(
            self,
            secret_key: Optional[str] = None,
            gateway: str = "",
            lazy_certification: bool = False,
            instruction: Optional[Message] = None,
            addition_instruction: Optional[Message] = None,
            file_path: Optional[str] = None,

    ):
        """初始化DocumentUnderstanding组件。

        Args:
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.

        Returns:
            None
        """
        super().__init__(DocumentUnderstandingArgs,
                         secret_key=secret_key,
                         gateway=gateway,
                         lazy_certification=lazy_certification)
        self.instruction = instruction,
        self.addition_instruction = addition_instruction
        self.file_path = file_path


    def get_addition_instruction(self, addition_instruction: str):
        """拼接addition_instruction"""
        return "，指令：" + addition_instruction

    def file_to_base64(self, file_path: str):
        try:
            # 打开文件并读取内容
            with open(file_path, "rb") as file:
                file_data = file.read()

            # 将文件数据转换为base64格式
            base64_encoded_data = base64.b64encode(file_data)

            # 将base64字节数据转换为字符串
            base64_message = base64_encoded_data.decode('utf-8')

            return base64_message
        except:
            return f"文件未找到，请检查文件路径是否正确。"

    def run(self,
            message: Message,
            file_path,
            instruction="",
            addition_instruction="",
            uid=None,
            trace_id=None,
            conversation_id=None,
            stream=False,
            timeout=None):
        '''
        run方法，用于执行长文档理解任务
        Args:
            message: 用户输入query
            file_path: 用户输入的文件路径
            instruction: 用户输入的人设指令
            addition_instruction: 用户输入的增强版指令(如有)

        Returns:
            result (Message): 模型运行后的输出消息。

        '''
        file_data = self.file_to_base64(file_path)
        file_name = file_path.split("/")[-1]
        file_type = file_name.split(".")[-1].lower()

        support_file_type = ["pdf", "docx", "xlsx", "png", "jpg", "jpeg", "txt"]
        if file_type not in support_file_type:
            raise Exception(f"不支持解析{file_type}类型的文件，当前仅支持解析以下几种文件类型：{support_file_type}")
        payload = json.dumps({
            "component": "DocumentUnderstanding",
            "stream": stream,
            "component_init_args": {
                "instruction": instruction,
                "addition_instruction": self.get_addition_instruction(addition_instruction),
                "file_data": file_data,
                "file_name": file_name,
            },
            "system": {
                "uid": uid,
                "traceid": trace_id,
                "conversation_id": conversation_id,
                "appbuilder_token": f"Bearer {os.getenv('APPBUILDER_TOKEN', '')}"
            },
            "user": {
                "query": message.content
            }
        })
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/json'
        headers['user-agent'] = 'vscode-restclient'
        headers['x-appbuilder-from'] = 'sdk'
        headers['x-appbuilder-authorization'] = f"Bearer {os.getenv('APPBUILDER_TOKEN', '')}"
        url = "http://copilot-test.now.baidu-int.com/dte/api/v2/component/tool_eval"
        response = self.http_client.session.post(url, headers=headers, data=payload, timeout=timeout, stream=stream)
        self.http_client.check_response_header(response)
        if response.status_code == 200:
            if stream:
                # 处理流式响应，逐行生成数据
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        yield decoded_line  # 使用yield逐行输出结果
            else:
                result = response.json()
                if result["code"] == 0:
                    yield result["result"].get("text")
                else:
                    raise Exception(f"服务请求失败: {result['message']}")
        else:
            response.raise_for_status()

    def tool_eval(self,
                  message: Message,
                  file_path: str,
                  stream: bool = False,
                  **kwargs):
        """用于function call
        """
        instruction = kwargs.get("instruction", "")
        addition_instruction = kwargs.get("addition_instruction", "")
        uid = kwargs.get("uid", "")
        trace_id = kwargs.get("trace_id", "")
        conversation_id = kwargs.get("conversation_id", "")

        result = self.run(message,
                          file_path,
                          instruction=instruction,
                          addition_instruction=addition_instruction,
                          uid=uid,
                          trace_id=trace_id,
                          conversation_id=conversation_id,
                          stream=stream)
        return result
