# appbuilder.core.components.document_understanding package

## Submodules

## appbuilder.core.components.document_understanding.component module

Copyright (c) 2023 Baidu, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

> [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

### *class* appbuilder.core.components.document_understanding.component.DocumentUnderstanding(secret_key: str | None = None, gateway: str = '', lazy_certification: bool = False, instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message) | None = None, addition_instruction: [Message](appbuilder.core.md#appbuilder.core.message.Message) | None = None, file_path: str | None = None, app_id: str | None = None)

基类：[`Component`](appbuilder.core.md#appbuilder.core.component.Component)

#### get_addition_instruction(addition_instruction: str)

拼接addition_instruction

#### get_conversation_id(app_id: str)

#### get_file_id(conversation_id: str, app_id: str, file_path: str)

#### manifests *= [{'description': '该工具支持对图片以及文档内容进行理解，并基于图片以及文档内容对用户的提问进行回答，包括但不限于文档内容问答、总结摘要、内容分析。', 'name': 'document_understanding', 'parameters': {'properties': {'addition_instruction': {'description': '用户增强指令', 'type': 'string'}, 'app_id': {'description': '系统应用ID', 'type': 'string'}, 'file_path': {'description': '用户上传的文档的文件路径', 'type': 'string'}, 'instruction': {'description': '用户指令', 'type': 'string'}, 'query': {'description': '用户输入的query', 'type': 'string'}}, 'required': ['query', 'file_path', 'instruction', 'addition_instruction', 'app_id'], 'type': 'object'}}]*

#### meta

`DocumentUnderstandingArgs` 的别名

#### name *= 'document_understanding'*

#### run(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), file_path, instruction='', addition_instruction='', app_id='', stream=False, timeout=None)

run方法，用于执行长文档理解任务
:param message: 用户输入query
:param file_path: 用户输入的文件路径
:param instruction: 用户输入的人设指令
:param addition_instruction: 用户输入的增强版指令(如有)
:param app_id: 用户输入的app_id

* **返回:**
  模型运行后的输出消息。
* **返回类型:**
  result ([Message](appbuilder.core.md#appbuilder.core.message.Message))

#### tool_eval(message: [Message](appbuilder.core.md#appbuilder.core.message.Message), file_path: str, stream: bool = False, \*\*kwargs)

用于function call

#### version *= 'v1'*
