# appbuilder.core.components.ppt_generation_from_instruction package

## Submodules

## appbuilder.core.components.ppt_generation_from_instruction.component module

### *class* appbuilder.core.components.ppt_generation_from_instruction.component.PPTGenerationFromInstruction(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

指令生成PPT，可通过传入对PPT的描述或者自定义参数进行生成。

### 示例

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromInstruction()
input_data = {
    'text': '生成一个介绍北京的PPT。',
    'custom_data': {},
    'complex': 3,
    'user_name': '百度千帆AppBuilder'
}
answer = ppt_generator(appbuilder.Message(input_data))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float | None = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 作业ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – 当PPT生成请求失败时抛出异常

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float | None = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – PPT生成任务的唯一标识符
  * **request_times** (*int* *,* *optional*) – 轮询请求的次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 每次轮询请求之间的间隔时间（秒），默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间（秒）。如果未设置，则使用http_client的默认超时时间。
* **返回:**
  PPT生成状态码。
  : - 1：正在生成
    - 2：生成完成
    - 3：生成失败
* **返回类型:**
  int
* **抛出:**
  **Exception** – PPT生成过程中出现异常时抛出。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据输入指令生成PPT。', 'name': 'ppt_generation_from_instruction', 'parameters': {'properties': {'text': {'description': '用户请求生成PPT的指令。', 'example': '生成一个介绍北京的PPT。', 'text': 'string'}}, 'required': ['text'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromInstructionArgs` 的别名

#### name *= 'ppt_generation_from_instruction'*

#### ppt_generation(post_data: dict, timeout: float | None = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 请求数据
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None.
* **返回:**
  任务ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求失败

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int* *,* *optional*) – 轮询请求结果次数，默认为60。
  * **poll_request_interval** (*int* *,* *optional*) – 轮询请求的间隔时间（秒），默认为5。
* **返回:**
  模型运行后的输出消息，包含PPT下载链接。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)

#### tool_eval(stream: bool = False, \*\*kwargs)

评估给定的文本内容。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器形式返回结果，默认为False。如果为True，则逐个生成下载链接；如果为False，则直接返回下载链接。
  * **\*\*kwargs** – 关键字参数，可以传递其他参数，但当前只使用 ‘text’ 参数。
* **返回:**
  如果 stream 为 False，则返回一个包含下载链接的字符串；如果 stream 为 True，则逐个生成下载链接。
* **抛出:**
  **ValueError** – 如果 ‘text’ 参数为空，则抛出此异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*
