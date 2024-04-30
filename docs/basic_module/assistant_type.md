# Assistant API说明

`Assistant SDK` 的基础接口 与 `Assistant API` 的接口与组织方式保持一致，且一一对应，更详细的接口说明请参考 [Assistant API](https://ai.baidu.com/ai-doc/ASSISTANT/Ck3d7)

## appbuilder.assistant.assistants

#### appbuilder.assistant.assistants.create

功能：创建assistant实例

```python
def create(self,
            name: str,
            description: str,
            assistant_id: Optional[str] = "",
            model: Optional[str] = "ERNIE-4.0-8K",
            response_format: Optional[str] = 'text',
            instructions: Optional[str] = "",
            thought_instructions: Optional[str] = "",
            chat_instructions: Optional[str] = "",
            tools: Optional[list[assistant_type.AssistantTool]] = [],
            file_ids: Optional[list[str]] = [],
            metadata: Optional[dict] = {},
            ) -> assistant_type.AssistantCreateResponse:
    """
    创建助手实例
    
    Args:
        name (str): 助手名称
        description (str): 助手描述
        assistant_id (Optional[str], optional): 助手ID. Defaults to "".
        model (Optional[str], optional): 模型名称. Defaults to "ERNIE-4.0-8K".
        response_format (Optional[str], optional): 响应格式. Defaults to 'text'.
        instructions (Optional[str], optional): 指令. Defaults to "".
        thought_instructions (Optional[str], optional): 思考指令. Defaults to "".
        chat_instructions (Optional[str], optional): 聊天指令. Defaults to "".
        tools (Optional[list[assistant_type.AssistantTool]], optional): 工具列表. Defaults to [].
        file_ids (Optional[list[str]], optional): 文件ID列表. Defaults to [].
        metadata (Optional[dict], optional): 元数据. Defaults to {}.
    
    Returns:
        assistant_type.AssistantCreateResponse: 助手创建响应
    
    """
```


## appbuilder.assistant.assistants.files


#### ## appbuilder.assistant.assistants.files.create

功能：上传并创建一个文件实例，该文件与assistant和thread解耦，可以单独使用。

```python
def create(self, file_path: str, purpose: str = "assistant") -> assistant_type.AssistantFilesCreateResponse:
        """
        上传文件到助理存储中。
        
        Args:
            file_path (str): 要上传的文件路径。
            purpose (str, optional): 上传文件的用途。默认为 "assistant"。
        
        Returns:
            assistant_type.AssistantFilesCreateResponse: 上传文件后返回的响应对象。
        
        Raises:
            ValueError: 如果指定的文件路径不存在，则会引发此异常。
        """
```


## appbuilder.assistant.threads

#### appbuilder.assistant.threads.create

功能：创建一个对话线程（等价于converstaion）

```python
def create(self, messages: Optional[list[thread_type.AssistantMessage]] = []) -> thread_type.ThreadCreateResponse:
        """
        创建一个新的对话线程。
        
        Args:
            messages: 要发送给助手的消息列表。如果不传入此参数，则会创建一个空对话线程。
        
        Returns:
            一个ThreadCreateResponse对象，包含新创建的线程的相关信息。
        
        Raises:
            ValueError: 如果传入的messages参数不是列表类型。
        
        """
```

## appbuilder.assistant.threads.messages

#### appbuilder.assistant.threads.messages.create

功能：在指定的thread中，最后位置附加一条消息

```python
def create(self, 
            thread_id: str,
            content: str,
            role: Optional[str] = "user",
            file_ids: Optional[list[str]] = []) -> thread_type.AssistantMessageCreateResponse:
    """
    创建一条消息。
    
    Args:
        thread_id (str): 线程ID。
        content (str): 消息内容。
        role (Optional[str], optional): 角色，可选值为"user"或"assistant"。默认为"user"。
        file_ids (Optional[list[str]], optional): 消息中包含的文件ID列表。默认为空列表。
    
    Returns:
        thread_type.AssistantMessageCreateResponse: 消息创建响应对象。
    
    Raises:
        HttpError: 如果请求失败，则抛出HttpError异常。
    """

```


## appbuilder.assistant.threads.runs

#### appbuilder.assistant.threads.runs.run

功能：同步非流式运行方法，使用指定的assistant与thread


```python
def run(self,
        assistant_id: str,
        thread_id: Optional[str] = "",
        thread: Optional[thread_type.AssistantThread] = None,
        model: Optional[str] = "ERNIE-4.0-8K",
        response_format: Optional[str] = "text",
        instructions: Optional[str] = "",
        thought_instructions: Optional[str] = "",
        chat_instructions: Optional[str] = "",
        tools: Optional[list[assistant_type.AssistantTool]] = [],
        metadata: Optional[dict] = {},
        tool_output: Optional[thread_type.ToolOutput] = None,
        ) -> thread_type.RunResult:
    """
    Args:
        assistant_id (str): 助手id
        thread_id (Optional[str], optional): 对话id. Defaults to "".
        thread (Optional[thread_type.AssistantThread], optional): 对话信息. Defaults to None.
        model (Optional[str], optional): 模型名称. Defaults to "ERNIE-4.0-8K".
        response_format (Optional[str], optional): 返回格式. Defaults to "text".
        instructions (Optional[str], optional): 指令信息. Defaults to "".
        thought_instructions (Optional[str], optional): 思考指令信息. Defaults to "".
        chat_instructions (Optional[str], optional): 闲聊指令信息. Defaults to "".
        tools (Optional[list[assistant_type.AssistantTool]], optional): 工具列表. Defaults to [].
        metadata (Optional[dict], optional): 元数据. Defaults to {}.
        tool_output (Optional[thread_type.ToolOutput], optional): 工具输出. Defaults to None.
    
    Returns:
        thread_type.RunResult: 运行结果
    
    Raises:
        ValueError: thread_id和thread不能同时为空
    
    Note:
        1. 如果thread_id没有传，则thread必须要传值
        2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
        3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
    """
```

#### appbuilder.assistant.threads.runs.stream_run

功能：流式运行方法，使用指定的assistant与thread

```python
def stream_run(self,
                assistant_id: str,
                thread_id: Optional[str] = "",
                thread: Optional[thread_type.AssistantThread] = None,
                model: Optional[str] = "ERNIE-4.0-8K",
                response_format: Optional[str] = "text",
                instructions: Optional[str] = "",
                thought_instructions: Optional[str] = "",
                chat_instructions: Optional[str] = "",
                tools: Optional[list[assistant_type.AssistantTool]] = [],
                metadata: Optional[dict] = {},
                tool_output: Optional[thread_type.ToolOutput] = None,
                ):
    """
    启动一个流式运行的对话，用于处理对话流中的消息。
    
    Args:
        assistant_id (str): 助理ID。
        thread_id (Optional[str], optional): 线程ID，用于恢复历史对话。默认为空字符串。
        thread (Optional[thread_type.AssistantThread], optional): 线程对象，用于恢复历史对话。默认为None。
        model (Optional[str], optional): 使用的模型名称。默认为"ERNIE-4.0-8K"。
        response_format (Optional[str], optional): 响应格式，支持"text"和"json"两种格式。默认为"text"。
        instructions (Optional[str], optional): 指令文本。默认为空字符串。
        thought_instructions (Optional[str], optional): 思考指令文本。默认为空字符串。
        chat_instructions (Optional[str], optional): 聊天指令文本。默认为空字符串。
        tools (Optional[list[assistant_type.AssistantTool]], optional): 使用的工具列表。默认为空列表。
        metadata (Optional[dict], optional): 元数据字典。默认为空字典。
        tool_output (Optional[thread_type.ToolOutput], optional): 工具输出对象。默认为None。
    
    Returns:
        Iterator[thread_type.AssistantRunEvent]: 返回一个迭代器，用于遍历流式运行中的事件。
    
    Raises:
        ValueError: 如果thread_id和thread参数同时为空，则会引发ValueError异常。
    
    Note:
        1. 如果thread_id没有传，则thread必须要传值。
        2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user。
        3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user。
    """
```

#### appbuilder.assistant.threads.runs.submit_tool_outputs

功能：在流式运行中，提交本地FunctionCall的运行结果

```python
def submit_tool_outputs(self,
                        run_id: str,
                        thread_id: str,
                        tool_outputs: Optional[list[thread_type.ToolOutput]]) -> thread_type.RunResult:
    """
    向服务端提交工具输出
    
    Args:
        run_id (str): 运行ID
        thread_id (str): 线程ID
        tool_outputs (Optional[list[thread_type.ToolOutput]]): 工具输出列表，可选
    
    Returns:
        thread_type.RunResult: 运行结果
    
    """
```

#### appbuilder.assistant.threads.runs.cancel

功能：在流式运行过程，中断该thread.stream_run的运行

```python
def cancel(self, run_id: str, thread_id: str) -> thread_type.RunResult:
    """
    取消指定线程的运行
    
    Args:
        run_id (str): 运行的ID
        thread_id (str): 线程的ID
    
    Returns:
        thread_type.RunResult: 取消运行的结果
    
    """
```

