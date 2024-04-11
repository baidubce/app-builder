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

from appbuilder.core.assistants import data_class

class AssistantConfig(object):
    def __init__(self, name: str, description: str, meatadata: dict = {}, response_format: str = "text",
                 instructions: str = "", thought_instructions: str = "", chat_instructions: str = "",
                 builtin_tools: list[str] = [], thirdparty_tools: list = [], file_ids: list = [], model: str="ERNIE-4.0-8K", **kwargs):
        self._name = name
        self._description = description
        self._metadata = meatadata
        self._response_format = response_format
        self._instructions = instructions
        self._thought_instructions = thought_instructions
        self._chat_instructions = chat_instructions
        self._builtin_tools = builtin_tools
        self._thirdparty_tools = thirdparty_tools
        self._file_ids = file_ids
        self._model = model

    def length_check(self) -> bool:
        """
        检查各个 str 类型的子属性长度之和是否超过 4096，如果超过则返回 False，否则返回 True。

        Args:
            无

        Returns:
            bool: 如果各个 str 类型的子属性长度之和未超过 4096，返回 True；否则返回 False。
        """
        length = len(self._name) + len(self._description) + len(self._response_format) + \
            len(self._instructions) + len(self._thought_instructions) + \
            len(self._chat_instructions)
        if length > 4096:
            return False
        return True
    
    # def find_custom_tool(self, tool_call: ToolCall):
    #     pass

    def get_assistant_tool_list(self):
        tool_list = []
        if self._builtin_tools:
            for tool in self._builtin_tools:
                tool_list.append(data_class.AssistantTool(**tool))
        return tool_list

    def get_tools_descr(self):
        pass


    def to_base_model(self):
        return {
            'name': self._name,
            'description': self._description,
            'metadata': self._metadata,
            'response_format': self._response_format,
            'instructions': self._instructions,
            'thought_instructions': self._thought_instructions,
            'chat_instructions': self._chat_instructions,
            'tools': self.get_assistant_tool_list(),
            'file_ids': self._file_ids,
        }

    # 比较两个 AssistantConfig 对象是否相同, 相同则返回 True，否则返回 False
    # 若不相同，输出一个表格，展示存在diff的字段
    def compare(self, assistant_config: 'AssistantConfig') -> bool:
        """
        比较两个 AssistantConfig 对象是否相同。
        Args:
            assistant_config (AssistantConfig): 需要比较的 AssistantConfig 对象。
        Returns:
            bool: 若两个 AssistantConfig 对象相同，返回 True；否则返回 False。
        """
        same_flag = True

        if self._name != assistant_config.name or \
           self._description != assistant_config.description or \
           self._metadata != assistant_config.metadata or \
           self._response_format != assistant_config.response_format or \
           self._instructions != assistant_config.instructions or \
           self._thought_instructions != assistant_config.thought_instructions or \
           self._chat_instructions != assistant_config.chat_instructions or \
           self._file_ids != assistant_config.file_ids:
            same_flag = False

        return same_flag

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def metadata(self):
        return self._metadata

    @property
    def response_format(self):
        return self._response_format

    @property
    def instructions(self):
        return self._instructions

    @property
    def thought_instructions(self):
        return self._thought_instructions

    @property
    def chat_instructions(self):
        return self._chat_instructions

    @property
    def tools(self):
        return self._tools

    @property
    def file_ids(self):
        return self._file_ids
    
    @property
    def model(self):
        return self._model

    def __str__(self):
        return "AssistantConfig(name={}, description={}, metadata={}, response_format={}, instructions={}, thought_instructions={}, chat_instructions={}, builtin_tools={}, thirdparty_tools={} file_ids={})".format(self._name, self._description, self._metadata,
                                                                                                                                                                                         self._response_format, self._instructions, self._thought_instructions,
                                                                                                                                                                                         self._chat_instructions, self._builtin_tools, self._thirdparty_tools, self._file_ids)

    def __repr__(self):
        return self.__str__()

    def __deepcopy__(self, memo):
        return AssistantConfig(name=self._name, description=self._description, meatadata=self._metadata, response_format=self._response_format, instructions=self._instructions, thought_instructions=self._thought_instructions, chat_instructions=self._chat_instructions, tools=self._tools, file_ids=self._file_ids)

    def __getstate__(self):
        return self.__dict__

if __name__ == '__main__':
    assistant_config = AssistantConfig(name='test', description='test', metadata=None, response_format='text', instructions='test', thought_instructions='test', chat_instructions='test', tools=[], file_ids=[])