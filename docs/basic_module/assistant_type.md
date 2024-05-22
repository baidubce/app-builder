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

#### appbuilder.assistant.assistants.update

功能：根据assistant_id修改一个已创建的Assistant

```python
def update(self,
               assistant_id: str,
               model: Optional[str],
               name: Optional[str],
               description: Optional[str],
               instructions: Optional[str] = "",
               tools: Optional[list[assistant_type.AssistantTool]] = [],
               thought_instructions: Optional[str] = "",
               chat_instructions: Optional[str] = "",
               response_format: Optional[str] = "text",
               file_ids: Optional[list[str]] = [],
               metadata: Optional[dict] = {}
               ) -> assistant_type.AssistantUpdateResponse:
        """
        根据assistant_id修改一个已创建的Assistant
        
        Args:
            assistant_id (str): 助手ID。
            model (Optional[str]): 助手模型。
            name (Optional[str]): 助手名称。
            description (Optional[str]): 助手描述。
            response_format (Optional[str], optional): 响应格式。默认为None。
            instructions (Optional[str], optional): 助手指令。默认为None。
            thought_instructions (Optional[str], optional): 思考指令。默认为None。
            chat_instructions (Optional[str], optional): 聊天指令。默认为None。
            tools (Optional[list[assistant_type.AssistantTool]], optional): 助手工具列表。默认为空列表。
            file_ids (Optional[list[str]], optional): 文件ID列表。默认为空列表。
            metadata (Optional[dict], optional): 助手元数据。默认为空字典。
        
        Returns:
            assistant_type.AssistantUpdateResponse: 助手更新响应。
        
        """
```

#### appbuilder.assistant.assistants.list

功能：查询当前用户已创建的assistant列表

```python
def list(self,
             limit: Optional[int] = 20,
             order: Optional[str] = "desc",
             after: Optional[str] = "",
             before: Optional[str] = "",
             ) -> assistant_type.AssistantListResponse:
        """
        查询当前用户已创建的assistant列表
        
        Args:
            limit (Optional[int], optional): 返回助手列表的最大数量，默认为20。
            order (Optional[str], optional): 返回助手列表的排序方式，可选值为"asc"或"desc"，默认为"desc"。
            after (Optional[str], optional): 返回助手列表中id在指定id之后的助手，默认为空字符串。
            before (Optional[str], optional): 返回助手列表中id在指定id之前的助手，默认为空字符串。
        
        Returns:
            assistant_type.AssistantListResponse: 助手列表响应体。
        
        """
```

#### appbuilder.assistant.assistants.query

功能：根据assistant_id查询Assistant信息

```python
def query(self,
              assistant_id: Optional[str]) -> assistant_type.AssistantQueryResponse:
        """
        根据assistant_id查询Assistant信息
        
        Args:
            assistant_id (Optional[str]): 助手ID
        
        Returns:
            assistant_type.AssistantQueryResponse: 助手查询响应结果
        
        Raises:
            HTTPError: 请求失败，抛出HTTPError异常
        """
```

#### appbuilder.assistant.assistants.delete

功能：根据assistant_id删除指定Assitant

```python
def delete(self,
               assistant_id: Optional[str]) -> assistant_type.AssistantDeleteResponse:
        """
        根据assistant_id删除指定Assitant
        
        Args:
            assistant_id (Optional[str]): 待删除的助手实例ID。
        
        Returns:
            assistant_type.AssistantDeleteResponse: 删除助手实例后的响应结果。
        
        Raises:
            HttpRequestError: 发送HTTP请求时发生错误。
        
        """
```

#### appbuilder.assistant.assistants.mount_files

功能：指定file_id和assistant_id，挂载File到对应的Assistant

```python
def mount_files(self,
            assistant_id: Optional[str],
            file_id: Optional[str]
            ) -> assistant_type.AssistantFilesResponse:
        """
        指定file_id和assistant_id，挂载File到对应的Assistant
        
        Args:
            assistant_id (Optional[str]): 助理ID。
            file_id (Optional[str]): 文件ID。
        
        Returns:
            assistant_type.AssistantFilesResponse: 助理文件列表响应对象。
        
        """
```

#### appbuilder.assistant.assistants.mounted_files_list

功能：查询Assistant挂载的File列表

```python
def mounted_files_list(self,
                   assistant_id: Optional[str],  
                   limit: Optional[int] = 20,
                   order: Optional[str] =  'desc' , 
                   after: Optional[str] =  "", 
                   before: Optional[str] =  "") -> assistant_type.AssistantMountedFilesListResponse:
        """
        查询Assistant挂载的File列表
        
        Args:
            assistant_id (Optional[str]): 助手ID，为空时获取当前登录用户的助手文件列表。
            limit (Optional[int], optional): 每页最多显示多少个文件。默认为20。
            order (Optional[AssistantListRole], optional): 文件列表排序方式。可选值为 'asc' 或 'desc'。默认为 'desc'。
            after (Optional[str], optional): 返回文件ID大于该值的文件列表。默认为空字符串。
            before (Optional[str], optional): 返回文件ID小于该值的文件列表。默认为空字符串。
        
        Returns:
            assistant_type.AssistantFilesListResponse: 包含文件列表信息的响应对象。
        
        """
```

#### appbuilder.assistant.assistants.unmount_files

功能：指定assistant_id和file_id，解绑Assistant中对应File的关联

```python
def unmount_files(self,
                     assistant_id: Optional[str],
                     file_id: Optional[str]
                     ) -> assistant_type.AssistantFilesDeleteResponse:
        """
        指定assistant_id和file_id，解绑Assistant中对应File的关联
        
        Args:
            assistant_id (Optional[str]): 助理ID。
            file_id (Optional[str]): 文件ID。
        Returns:
            assistant_type.AssistantFilesDeleteResponse: 响应对象。
        """
```

## appbuilder.assistant.assistants.files


#### appbuilder.assistant.assistants.files.create

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

#### appbuilder.assistant.assistants.files.list

功能：列出存储中的文件列表

```python
def list(self) -> assistant_type.AssistantFilesListResponse:
        """
        列出存储中的文件列表
        
        Args:
            无
        
        Returns:
            assistant_type.AssistantFilesListResponse: 文件列表的响应对象，包含以下属性：
        
        Raises:
            assistant_type.AssistantError: 请求发生错误时抛出，具体错误信息可通过 `error_msg` 属性获取
        """
```

#### appbuilder.assistant.assistants.files.query

功能：根据文件ID查询文件信息

```python
def query(self,
            file_id: str,
        ) -> assistant_type.AssistantFilesQueryResponse:
    """
    根据文件ID查询文件信息
    
    Args:
        file_id (str): 文件ID
    
    Returns:
        assistant_type.AssistantFilesQueryResponse: 文件查询响应对象
    
    Raises:
        TypeError: 如果file_id不是str类型
        ValueError: 如果file_id不存在
    """
```


#### appbuilder.assistant.assistants.files.download

功能：下载文件

```python
def download(self,
                 file_id:str,
                 file_path:str="", # 要求若文件路径不为空，需要以/结尾，默认下载到当前文件夹
                 timeout:Optional[int]=None,
                 ):
        """
        下载文件
        
        Args:
            file_id (str): 文件ID
            file_path (str, optional): 文件保存路径，默认为空字符串。如果未指定，则使用文件名的默认值。要求若文件路径不为空，需要以/结尾。
            timeout (Optional[int], optional): 请求超时时间，单位秒。如果未指定，则使用默认超时时间。
        
        Returns:
            None
        
        Raises:
            TypeError: 当file_path或file_id类型不为str时引发此异常。
            ValueError: 当file_id为空或None时，或file_path不是文件目录时引发此异常。
            FileNotFoundError: 当指定的文件路径或文件不存在时引发此异常。
            OSError: 当磁盘空间不足时引发此异常。
            HTTPConnectionException: 当请求失败时引发此异常。
            Exception: 当发生其他异常时引发此异常。
        """
```

#### appbuilder.assistant.assistants.files.content

功能：获取指定文件的内容

```python
def content(self,
            file_id:str,
            timeout:Optional[int]=None):
    """
    获取指定文件的内容
    
    Args:
        file_id (str): 文件ID
        timeout (Optional[int], optional): 请求超时时间，单位秒. Defaults to None.
    
    Returns:
        assistant_type.AssistantFilesContentResponse: 包含文件内容的响应对象
    
    Raises:
        TypeError: 当file_id不是字符串类型时引发此异常
        FileNotFoundError: 当指定的文件路径不存在时引发此异常
        HTTPConnectionException: 当请求失败时引发此异常
    
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

#### appbuilder.assistant.threads.query

功能：查询对话线程信息。

```python
def query(self,
              thread_id:str)->thread_type.ThreadQueryResponse:
        """
        查询对话线程信息。
        Args:
            thread_id: 要查询的对话线程ID。
        Returns:
            一个ThreadQueryResponse对象，包含对话线程的相关信息。
        Raises:
            ValueError: 如果传入的thread_id参数不是字符串类型。
        """
```

#### appbuilder.assistant.threads.delete

功能：删除对话线程。

```python
def delete(self,
               thread_id:str)->thread_type.ThreadDeleteResponse:
        """
        删除对话线程。
        Args:
            thread_id: 要删除的对话线程ID。
        Returns:
            一个ThreadDeleteResponse对象，包含对话线程的相关信息。
        Raises:
            ValueError: 如果传入的thread_id参数不是字符串类型。
        """
```

#### appbuilder.assistant.threads.update

功能：

```python
def update(self,
            thread_id:str ,
            metadata:Optional[dict] ={} )->thread_type.ThreadUpdateResponse:
    """
    更新线程信息
    
    Args:
        thread_id (str): 线程ID
        metadata (Optional[dict], optional): 线程元数据. 默认为空字典.
    
    Returns:
        thread_type.ThreadUpdateResponse: 线程更新响应
    
    Raises:
        TypeError: 如果metadata不是字典类型
        ValueError: 如果metadata的键超过64个字符或值超过512个字符
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

#### appbuilder.assistant.threads.messages.update

功能：修改Message对象，允许content和file_ids字段

```python
def update(self,
               thread_id: str,
               message_id: str,
               content: Optional[str],
               file_ids: Optional[list[str]] = []) -> thread_type.AssistantMessageUpdateResponse:
        """
        修改Message对象，允许content和file_ids字段
        Args:
            thread_id (str): 线程ID。
            message_id (str): 消息ID。
            content (Optional[str], optional): 消息内容。默认为空字符串。
            file_ids (Optional[list[str]], optional): 消息中包含的文件ID列表。默认为空列表。
        Returns:
            thread_type.AssistantMessageUpdateResponse: 消息更新响应对象。
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
```

#### appbuilder.assistant.threads.messages.list

功能：查询指定Thread下的Message列表

```python
def list(self,
            thread_id: str,
            limit: int = 20,
            order: str = "desc",
            after: str = "",
            before: str = "") -> thread_type.AssistantMessageListResponse:
        """
        查询指定Thread下的Message列表
        Args:
            thread_id (str): 线程ID。
            limit (int, optional): 返回消息的最大数量，取值范围为[1,20]。默认为-20。
            order (Optional[str], optional): 排序方式，可选值为"asc"或"desc"。默认为"desc"。
            after (Optional[str], optional): 查询指定message_id之后创建的Message。
            before (Optional[str], optional): 查询指定message_id之前创建的Message
            
        Returns:
            thread_type.AssistantMessageListResponse: 查询thread下的message列表响应对象。
            
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
```

#### appbuilder.assistant.threads.messages.query

功能：根据message_id查询指定Message的信息

```python
def query(self,
            thread_id:str,
            message_id:str) -> thread_type.AssistantMessageQueryResponse:
        """
        根据message_id查询指定Message的信息
        
        Args:
            thread_id (str): 线程ID
            message_id (str): 消息ID
        
        Returns:
            thread_type.AssistantMessageQueryResponse: 消息信息响应
            
        Raises:
            HttpError: 如果请求失败，则抛出HttpError异常。
        """
```

#### appbuilder.assistant.threads.messages.files

功能：获取指定消息 ID 的附件信息。

```python
def files(self,
              thread_id:str,
              message_id:str,
              limit:Optional[int] =  20,
              order:Optional[str] = "desc",
              after:Optional[str] = "",
              before:Optional[str] = "") -> thread_type.AssistantMessageFilesResponse:
        """
        获取指定消息 ID 的附件信息。
        
        Args:
            thread_id (str): 线程 ID。
            messsages_id (str): 消息 ID。
            limit (Optional[int], optional): 返回结果的最大数量，默认为 20。
            order (Optional[str], optional): 排序方式，可选值为 "asc" 或 "desc"，默认为 "desc"。
            after (Optional[str], optional): 返回结果的时间范围，只返回时间晚于该时间戳的消息附件，默认为空。
            before (Optional[str], optional): 返回结果的时间范围，只返回时间早于该时间戳的消息附件，默认为空。
        
        Returns:
            thread_type.AssistantMessageFilesResponse: 附件信息响应对象。
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

