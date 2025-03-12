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

from pydantic import BaseModel, Field
from typing import Optional

from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace
from .base import HallucinationDetectionArgs
        

class HallucinationDetection(CompletionBaseComponent):
    """
    幻觉检测。输入<query, context, answer>，判断answer中是否存在幻觉。
    *注：该组件推荐使用Qianfan-Agent-Speed-8K模型。*

    Examples:

    .. code-block:: python

        import os
        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ['APPBUILDER_TOKEN'] = '...'

        hallucination_detection = appbuilder.HallucinationDetection()

        query = ''
        context = \
        '''澳门美食： 澳门新麻蒲韩国烤肉店
        在澳门一年四季之中除了火锅，烤肉也相当受欢迎。提到韩烧，有一间令我印象最深刻，就是号称韩国第一的烤肉店－新麻蒲韩国烤肉店，光是韩国的分店便多达四百多间，海外分店更是遍布世界各地，2016年便落户澳门筷子基区，在原本已经食肆林立的地方一起百花齐放！店内的装修跟韩国分店还完度几乎没差，让食客彷如置身于韩国的感觉，还要大赞其抽风系统不俗，离开时身上都不会沾上烤肉味耶！
        时间：周一至周日 下午5:00 - 上午3:00
        电话：＋853 2823 4012
        地址：澳门筷子基船澳街海擎天第三座地下O号铺96号
        必食推介:
        护心肉二人套餐
        来新麻蒲必试的有两样东西，现在差不多每间烤肉店都有炉边烤蛋，但大家知道吗？原来新麻蒲就是炉边烤蛋的开创者，既然是始祖，这已经是个非吃不可的理由！还有一款必试的就是护心肉，即是猪的横隔膜与肝中间的部分，每头猪也只有200克这种肉，非常珍贵，其味道吃起来有种独特的肉香味，跟牛护心肉一样精彩！
        秘制猪皮
        很多怕胖的女生看到猪皮就怕怕，但其实猪皮含有大量胶原蛋白，营养价值很高呢！这里红通通的猪皮还经过韩国秘制酱汁处理过，会有一点点辣味。烤猪皮的时候也需特别注意火侯，这样吃起来才会有外脆内Q的口感！'''
        answer = '澳门新麻蒲烤肉店并不是每天开门。'

        inputs = {'query': query, 'context': context, 'answer': answer}
        msg = appbuilder.Message(inputs)
        result = hallucination_detection.run(msg)

        print(result)
    """
    name = 'hallucination_detection'
    version = 'v1'
    meta = HallucinationDetectionArgs

    manifests = [
        {
            "name": "hallucination_detection",
            "description": "输入用户查询query、检索结果context以及根据检索结果context生成的用户查询query的回答answer，判断answer" \
                           "中是否存在幻觉。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户查询。"
                    },
                    "context": {
                        "type": "string",
                        "description": "检索结果。"
                    },
                    "answer": {
                        "type": "string",
                        "description": "根据检索结果context生成的用户查询query的回答answer。"
                    }
                },
                "required": [
                    "query",
                    "context",
                    "answer"
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
        """初始化幻觉检测组件。
        
        Args:
            model (str|None): 模型名称，用于指定要使用的千帆模型。推荐使用Qianfan-Agent-Speed-8K模型。
            secret_key (str, 可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
            gateway (str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            lazy_certification (bool, 可选): 延迟认证，为True时在第一次运行时认证. Defaults to False.
        
        Returns:
            None
        
        """
        super().__init__(HallucinationDetectionArgs,
                         model=model,
                         secret_key=secret_key,
                         gateway=gateway,
                         lazy_certification=lazy_certification)

    def completion(self, version, base_url, request, timeout: float = None,
                   retry: int = 0):
        """
        Send a byte array of an audio file to obtain the result of speech recognition.
        
        Args:
            version (str): API version.
            base_url (str): Base URL of the API.
            request (Request): Request object containing audio file and other parameters.
            timeout (float, optional): Timeout for the request. Defaults to None.
            retry (int, optional): Number of retries for the request. Defaults to 0.
        
        Returns:
            Response: Processed response object.
        
        """
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"

        stream = True if request.response_mode == "streaming" else False
        
        url = self.http_client.service_url("/app/hallucination_detection", self.base_url)
        response = self.http_client.session.post(url, json=request.params, headers=headers, timeout=timeout,
                                                 stream=stream)
        return self.gene_response(response, stream)

    @components_run_trace
    def run(self, message, stream=False, temperature=1e-10, top_p=0.0):
        """
        使用给定的输入运行模型并返回结果。
        
        Args:
            message (Message): 输入消息，包含 query、context 和 answer。是必需的参数。
            stream (bool, 可选): 是否以流式形式返回响应。默认为 False。
            temperature (float, 可选): 模型配置的温度参数，用于调整模型的生成概率。
                取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
            top_p (float, 可选): 影响输出文本的多样性，取值越大，生成文本的多样性越强。
                取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
        
        Returns:
            result (Message): 模型运行后的输出消息。
        
        Raises:
            AssertionError: 如果输入的 message 中缺少 query、context 或 answer。
            AppBuilderServerException: 如果请求执行失败，将抛出异常，包含服务错误码和错误信息。
        """
        inputs = message.content
        query = inputs.pop('query', None)
        assert query, 'You must input query and query should not be empty'
        assert 'context' in inputs and inputs['context'], 'You must input context and context should not be empty'
        assert 'answer' in inputs and inputs['answer'], 'You must input answer and answer should not be empty'
        response_mode = "streaming" if stream else "blocking"
        user_id = message.id
        model_config_inputs = ModelArgsConfig(**{"stream": stream, "temperature": temperature, "top_p": top_p})
        model_config = self.get_model_config(model_config_inputs)

        request = self.gene_request(query, inputs, response_mode, user_id, model_config)
        response = self.completion(self.version, self.base_url, request)

        if response.error_no != 0:
            raise AppBuilderServerException(service_err_code=response.error_no, service_err_message=response.error_msg)

        result = response.to_message()

        return result

    @components_run_stream_trace
    def tool_eval(self, name: str, stream: bool = False, **kwargs):
        """
        调用函数进行工具评估。
        
        Args:
            name (str): 函数名，当前方法未使用此参数，预留接口。
            stream (bool, optional): 是否以流的方式返回结果，默认为False。如果为True，则逐个返回结果；如果为False，则一次性返回所有结果。
            **kwargs: 关键字参数，包含评估所需的输入参数。
        
                - query (str): 查询语句。
                - context (str): 上下文信息。
                - answer (str): 参考答案。
                - model_configs (dict, optional): 模型配置信息，默认为空字典。包含以下字段：
                    - temperature (float, optional): 温度参数，用于控制生成文本的随机性，默认为1e-10。
                    - top_p (float, optional): 截断概率，用于控制生成文本的质量，默认为0.0。
        
        Returns:
            如果stream为False，返回包含所有评估结果的列表；如果stream为True，逐个返回评估结果。
        
        Raises:
            ValueError: 如果缺少query、context或answer参数，将引发此异常。
        """
        query = kwargs.get('query', None)
        context = kwargs.get('context', None)
        answer = kwargs.get('answer', None)
        if not query or not context or not answer:
            raise ValueError('param `query` and `context` and `answer` are required')
        msg = Message({'query': query, 'context': context, 'answer': answer})
        model_configs = kwargs.get('model_configs', {})
        temperature = model_configs.get('temperature', 1e-10)
        top_p = model_configs.get('top_p', 0.0)
        message = self.run(message=msg,
                           stream=stream,
                           temperature=temperature,
                           top_p=top_p)
        if stream:
            for data in message.content:
                yield data
        else:
            return message.content