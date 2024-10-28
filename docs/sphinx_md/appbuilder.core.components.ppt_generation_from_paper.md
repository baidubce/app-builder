# appbuilder.core.components.ppt_generation_from_paper package

## Submodules

## appbuilder.core.components.ppt_generation_from_paper.component module

### *class* appbuilder.core.components.ppt_generation_from_paper.component.PPTGenerationFromPaper(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

论文生成PPT。

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromPaper()
user_input = {
    'file_key': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'
}
answer = ppt_generator(appbuilder.Message(user_input))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float | None = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None.
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求失败

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float | None = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **request_times** (*int* *,* *optional*) – 请求次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 请求间隔时间，默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None，即不设置超时时间。
* **返回:**
  PPT生成状态码。
  : - 1: PPT正在生成中
    - 2: PPT生成完成
    - 3: PPT生成失败
* **返回类型:**
  int
* **抛出:**
  **Exception** – PPT生成失败或请求失败时抛出异常。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据上传的论文生成PPT。', 'name': 'ppt_generation_from_paper', 'parameters': {'properties': {'file_key': {'description': '用户上传的论文的链接。', 'text': 'string'}}, 'required': ['file_key'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromPaperArgs` 的别名

#### name *= 'ppt_generation_from_paper'*

#### ppt_generation(post_data: dict, timeout: float | None = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 发送的POST请求体数据
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  返回的任务ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – 如果PPT生成请求失败，抛出异常

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create-thesis'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int*) – 轮询请求结果次数，默认为60次。
  * **poll_request_interval** (*int*) – 轮询请求的间隔时间（秒），默认为5秒。
* **返回:**
  模型运行后的输出消息，包含PPT下载链接。
* **返回类型:**
  [Message](appbuilder.core.md#appbuilder.core.message.Message)
* **抛出:**
  **Exception** – 当输入参数中缺少必要的键时，抛出异常。

#### tool_eval(stream: bool = False, \*\*kwargs)

使用指定的file_key来评估并获取相应的结果。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器的方式逐项返回结果，默认为False。
  * **\*\*kwargs** – 关键字参数，用于传递其他参数，目前仅支持file_key。
* **返回:**
  如果stream为False，则直接返回结果。
  如果stream为True，则逐个返回结果。
* **抛出:**
  **ValueError** – 如果参数file_key为空，则抛出异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*
