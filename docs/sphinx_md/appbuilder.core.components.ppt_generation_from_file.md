# appbuilder.core.components.ppt_generation_from_file package

## Submodules

## appbuilder.core.components.ppt_generation_from_file.component module

### *class* appbuilder.core.components.ppt_generation_from_file.component.PPTGenerationFromFile(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

文件生成PPT。

Examples:

```python
import os
import appbuilder

os.environ["APPBUILDER_TOKEN"] = '...'

ppt_generator = appbuilder.PPTGenerationFromFile()
user_input = {
    'file_url': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx'
}
answer = ppt_generator(appbuilder.Message(user_input))
print(answer.content)
```

#### get_ppt_download_link(job_id: str, timeout: float | None = None)

获取PPT下载链接

* **参数:**
  * **job_id** (*str*) – 任务ID
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None。
* **返回:**
  PPT下载链接
* **返回类型:**
  str
* **抛出:**
  **Exception** – PPT生成请求错误

#### get_ppt_download_link_url *= '/ppt/text2ppt/apps/ppt-download'*

#### get_ppt_generation_status(job_id: str, request_times: int = 60, request_interval: int = 5, timeout: float | None = None)

轮询查看PPT生成状态

* **参数:**
  * **job_id** (*str*) – PPT生成任务的唯一标识符
  * **request_times** (*int* *,* *optional*) – 轮询请求次数，默认为60次。
  * **request_interval** (*int* *,* *optional*) – 每次轮询请求的间隔时间（秒），默认为5秒。
  * **timeout** (*float* *,* *optional*) – 请求的超时时间（秒），默认为None，即无超时限制。
* **返回:**
  PPT生成状态码，1表示正在生成，2表示生成完成，3表示生成失败。
* **返回类型:**
  int
* **抛出:**
  **Exception** – 如果PPT生成状态码不为2（生成完成），则抛出异常。

#### get_ppt_generation_status_url *= '/ppt/text2ppt/apps/ppt-result'*

#### manifests *= [{'description': '根据上传的文件（非论文）生成PPT。', 'name': 'ppt_generation_from_file', 'parameters': {'properties': {'file_url': {'description': '用户上传的文件的链接。', 'text': 'string'}}, 'required': ['file_url'], 'type': 'object'}}]*

#### meta

`PPTGenerationFromFileArgs` 的别名

#### name *= 'ppt_generation_from_file'*

#### ppt_generation(post_data: dict, timeout: float | None = None)

创建PPT生成任务

* **参数:**
  * **post_data** (*dict*) – 包含PPT生成任务所需数据的字典
  * **timeout** (*float* *,* *optional*) – 请求超时时间，默认为None，表示不设置超时时间。
* **返回:**
  PPT生成任务的Job ID
* **返回类型:**
  str
* **抛出:**
  **Exception** – 如果PPT生成任务请求失败，抛出异常

#### ppt_generation_url *= '/ppt/text2ppt/apps/ppt-create-file'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), poll_request_times=60, poll_request_interval=5) → [Message](appbuilder.core.md#appbuilder.core.message.Message)

使用给定的输入运行模型并返回结果。

* **参数:**
  * **message** ([*Message*](appbuilder.core.md#appbuilder.core.message.Message)) – 输入消息，用于传入请求参数。
  * **poll_request_times** (*int*) – 轮询请求结果次数。
  * **poll_request_interval** (*int*) – 轮询请求的间隔时间（秒）。
* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](appbuilder.core.md#appbuilder.core.message.Message))

#### tool_eval(stream: bool = False, \*\*kwargs)

用于执行function call的功能。

* **参数:**
  * **stream** (*bool* *,* *optional*) – 是否以生成器的方式返回结果，默认为False。
  * **\*\*kwargs** – 任意关键字参数，目前只支持’file_url’。
* **返回:**
  如果stream为False，则返回一个字符串，表示ppt下载链接。
  如果stream为True，则返回一个生成器，生成器产生一个字符串，表示ppt下载链接。
* **抛出:**
  **ValueError** – 如果’file_url’为空，则抛出异常。

#### uniform_prefix *= '/api/v1/component/component'*

#### version *: str*
