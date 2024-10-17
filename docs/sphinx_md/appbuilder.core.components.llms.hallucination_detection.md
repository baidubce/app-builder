# appbuilder.core.components.llms.hallucination_detection package

## Submodules

## appbuilder.core.components.llms.hallucination_detection.component module

### *class* appbuilder.core.components.llms.hallucination_detection.component.HallucinationDetection(model=None, secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：`CompletionBaseComponent`

幻觉检测。输入<query, context, answer>，判断answer中是否存在幻觉。
 *注：该组件推荐使用ERNIE Speed-AppBuilder模型。*

Examples:

```python
import os
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'

hallucination_detection = appbuilder.HallucinationDetection()

query = ''
context =         '''澳门美食： 澳门新麻蒲韩国烤肉店
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
```

#### completion(version, base_url, request, timeout: float | None = None, retry: int = 0)

Send a byte array of an audio file to obtain the result of speech recognition.

* **参数:**
  * **version** (*str*) – API version.
  * **base_url** (*str*) – Base URL of the API.
  * **request** (*Request*) – Request object containing audio file and other parameters.
  * **timeout** (*float* *,* *optional*) – Timeout for the request. Defaults to None.
  * **retry** (*int* *,* *optional*) – Number of retries for the request. Defaults to 0.
* **返回:**
  Processed response object.
* **返回类型:**
  Response

#### manifests *= [{'description': '输入用户查询query、检索结果context以及根据检索结果context生成的用户查询query的回答answer，判断answer中是否存在幻觉。', 'name': 'hallucination_detection', 'parameters': {'properties': {'answer': {'description': '根据检索结果context生成的用户查询query的回答answer。', 'text': 'string'}, 'context': {'description': '检索结果。', 'text': 'string'}, 'query': {'description': '用户查询。', 'text': 'string'}}, 'required': ['query', 'context', 'answer'], 'type': 'object'}}]*

#### meta

[`HallucinationDetectionArgs`](#appbuilder.core.components.llms.hallucination_detection.component.HallucinationDetectionArgs) 的别名

#### name *: str* *= 'hallucination_detection'*

#### run(message, stream=False, temperature=1e-10, top_p=0.0)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息，包含 query、context 和 answer。是必需的参数。
  * **stream** (*bool* *,*  *可选*) – 是否以流式形式返回响应。默认为 False。
  * **temperature** (*float* *,*  *可选*) – 模型配置的温度参数，用于调整模型的生成概率。
    取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
  * **top_p** (*float* *,*  *可选*) – 影响输出文本的多样性，取值越大，生成文本的多样性越强。
    取值范围为 0.0 到 1.0，较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](appbuilder.core.md#appbuilder.core.message.Message))
* **抛出:**
  * **AssertionError** – 如果输入的 message 中缺少 query、context 或 answer。
  * **AppBuilderServerException** – 如果请求执行失败，将抛出异常，包含服务错误码和错误信息。

#### tool_eval(name: str, stream: bool = False, \*\*kwargs)

调用函数进行工具评估。

* **参数:**
  * **name** (*str*) – 函数名，当前方法未使用此参数，预留接口。
  * **stream** (*bool* *,* *optional*) – 是否以流的方式返回结果，默认为False。如果为True，则逐个返回结果；如果为False，则一次性返回所有结果。
  * **\*\*kwargs** – 

    关键字参数，包含评估所需的输入参数。
    - query (str): 查询语句。
    - context (str): 上下文信息。
    - answer (str): 参考答案。
    - model_configs (dict, optional): 模型配置信息，默认为空字典。包含以下字段：
      : - temperature (float, optional): 温度参数，用于控制生成文本的随机性，默认为1e-10。
        - top_p (float, optional): 截断概率，用于控制生成文本的质量，默认为0.0。
* **返回:**
  如果stream为False，返回包含所有评估结果的列表；如果stream为True，逐个返回评估结果。
* **抛出:**
  **ValueError** – 如果缺少query、context或answer参数，将引发此异常。

#### version *: str* *= 'v1'*

### *class* appbuilder.core.components.llms.hallucination_detection.component.HallucinationDetectionArgs(\*, name: str = '', tool_desc: Dict[str, Any] = {}, query: str, context: str, answer: str)

基类：[`ComponentArguments`](appbuilder.core.md#appbuilder.core.component.ComponentArguments)

幻觉检测配置

#### query

str
用户查询。

* **Type:**
  str

#### context

str
根据query得到的检索结果。

* **Type:**
  str

#### answer

str
基于context生成的query的答案。

* **Type:**
  str

#### answer *: str*

#### context *: str*

#### model_computed_fields *: ClassVar[dict[str, ComputedFieldInfo]]* *= {}*

A dictionary of computed field names and their corresponding ComputedFieldInfo objects.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### model_fields *: ClassVar[dict[str, FieldInfo]]* *= {'answer': FieldInfo(annotation=str, required=True, description='基于context生成的query的答案。', json_schema_extra={'valiable_name': 'answer'}), 'context': FieldInfo(annotation=str, required=True, description='根据query得到的检索结果。', json_schema_extra={'valiable_name': 'context'}), 'name': FieldInfo(annotation=str, required=False, default=''), 'query': FieldInfo(annotation=str, required=True, description='用户查询。', json_schema_extra={'valiable_name': 'query'}), 'tool_desc': FieldInfo(annotation=Dict[str, Any], required=False, default={})}*

Metadata about the fields defined on the model,
mapping of field names to [FieldInfo][pydantic.fields.FieldInfo].

This replaces Model._\_fields_\_ from Pydantic V1.

#### query *: str*
