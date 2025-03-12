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
import json
import re

from typing import Optional

from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import OralQueryGenerationArgs


class OralQueryGeneration(CompletionBaseComponent):
    r"""
    口语化Query生成，可用于问答场景下对文档增强索引。
    *注：该组件推荐使用Qianfan-Agent-Speed-8K模型。*

    Examples:

    .. code-block:: python

        import os
        import appbuilder

        os.environ["APPBUILDER_TOKEN"] = '...'

        text = ('文档标题：在OPPO Reno5上使用视频超级防抖\n'
                '文档摘要：OPPO Reno5上的视频超级防抖，视频超级防抖3.0，多代视频防抖算法积累，这一代依旧超级防抖超级稳。 开启视频超级'
                '防抖 开启路径：打开「相机 > 视频 > 点击屏幕上方的“超级防抖”标识」 后置视频同时支持超级防抖和超级防抖Pro功能，开启超级'
                '防抖后手机屏幕将出现超级防抖Pro开关，点击即可开启或关闭。 除此之外，前置视频同样加持防抖算法，边走边拍也能稳定聚焦脸部'
                '，实时视频分享您的生活。')
        oral_query_generation = appbuilder.OralQueryGeneration(model='Qianfan-Agent-Speed-8K')
        answer = oral_query_generation(appbuilder.Message(text), query_type='全部', output_format='str')
        print(answer.content)
    """
    name = 'query_generation'
    version = 'v1'
    meta = OralQueryGenerationArgs

    manifests = [
        {
            "name": "query_generation",
            "description": "输入文本、待生成的query类型和输出格式，生成query，并按照要求的格式进行输出。",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "输入文本，组件会根据该输入文本生成query。"
                    },
                    "query_type": {
                        "type": "string",
                        "description": "待生成的query类型，可选问题、短语以及全部（问题 + 短语）。"
                    },
                    "output_format": {
                        "type": "string",
                        "description": "输出格式，可选json或str，str格式与老版本输出格式相同。"
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
        model=None,
        secret_key: Optional[str] = None, 
        gateway: str = "",
        lazy_certification: bool = False,
        **kwargs
    ):
        """初始化口语化Query生成模型。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。推荐使用Qianfan-Agent-Speed-8K模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(
                OralQueryGenerationArgs, model=model, secret_key=secret_key, gateway=gateway, lazy_certification=lazy_certification)
    
    def regenerate_output(self, model_output, output_format):
        """
        兼容老版本的输出格式
        """
        if not isinstance(model_output, str):
            return model_output
        
        match_obj = re.search(r'```json\n(.+)\n```', model_output, flags=re.DOTALL)

        regenerated_output = None
        if match_obj:
            regenerated_output = json.loads(match_obj.group(1))
        else:
            dict_json_match_obj = re.search(r'\{(.|\n)+\}', model_output)
            dict_json_text = dict_json_match_obj.group(0) if dict_json_match_obj else None
            regenerated_output = json.loads(dict_json_text) if dict_json_text is not None else model_output

        if output_format == 'json' or not isinstance(regenerated_output, dict):
            return json.dumps(regenerated_output, ensure_ascii=False, indent=4)

        queries = []
        for key in ['问题', '短语']:
            queries += regenerated_output.pop(key, [])
        for value in regenerated_output.values():
            queries += value
        
        regenerated_output = '\n'.join([f'{index}. {query}' for index, query in enumerate(queries, 1)])
        return regenerated_output

    def completion(self, version, base_url, request, timeout: float = None,
                   retry: int = 0):
        r"""Send a byte array of an audio file to obtain the result of speech recognition."""

        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        stream = True if request.response_mode == "streaming" else False
        
        url = self.http_client.service_url("/app/query_generation", self.base_url)
        response = self.http_client.session.post(url, json=request.params, headers=headers, timeout=timeout,
                                                 stream=stream)
        return self.gene_response(response, stream)

    @components_run_trace
    def run(self, message, query_type='全部', output_format='str', stream=False, temperature=1e-10, top_p=0.0):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (Message): 输入消息，包含query、context和answer等信息。这是一个必需的参数。
            query_type (str, 可选): 待生成的query类型，包括问题、短语和全部（问题+短语）。默认为全部。
            output_format (str, 可选): 输出格式，包括json和str，当stream为True时，只能以json形式输出。默认为str。
            stream (bool, 可选): 指定是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。
                取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            result (Message): 模型运行后的输出消息。
        
        """
        text = message.content
        assert text, 'Input text should be a valid string'
        inputs = {
            'text': text,
            'query_type': query_type
        }
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature, "top_p": top_p})
        model_config = self.get_model_config(model_config_inputs)

        request = self.gene_request('', inputs, response_mode, user_id, model_config)
        response = self.completion(self.version, self.base_url, request)

        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        result = response.to_message()
        result.content = self.regenerate_output(result.content, output_format)

        return result

    @components_run_stream_trace
    def tool_eval(self, name: str, streaming: bool = False, **kwargs):
        """
        调用函数进行工具评估。
        
        Args:
            name (str): 评估工具的名称。
            stream (bool, optional): 是否以流的形式返回结果。默认为False。
            **kwargs: 关键字参数，可以包含以下参数：
                text (str): 需要评估的文本。
                query_type (str, optional): 查询类型，默认为'全部'。
                output_format (str, optional): 输出格式，默认为'str'。
                model_configs (dict, optional): 模型配置，默认为空字典。
        
        Returns:
            如果stream为False，则返回评估结果列表；
            如果stream为True，则逐个返回评估结果。
        
        Raises:
            ValueError: 如果未提供text参数，则抛出ValueError异常。
        
        """
        text = kwargs.get('text', None)
        query_type = kwargs.get('query_type', '全部')
        output_format = kwargs.get('output_format', 'str')
        if not text:
            raise ValueError('param `text` is required')
        msg = Message(text)
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get('temperature', 1e-10)
        top_p = model_configs.get('top_p', 0.0)
        message = self.run(message=msg,
                           query_type=query_type,
                           output_format=output_format,
                           stream=streaming,
                           temperature=temperature,
                           top_p=top_p)
        if streaming:
            for data in message.content:
                yield data
        else:
            return message.content
