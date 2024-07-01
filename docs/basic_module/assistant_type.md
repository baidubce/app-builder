# Assistant API说明

`Assistant SDK` 的基础接口 与 `Assistant API` 的接口与组织方式保持一致，且一一对应，更详细的接口说明请参考 [Assistant API](https://ai.baidu.com/ai-doc/ASSISTANT/Ck3d7)

## appbuilder.assistant.assistants

#### appbuilder.assistant.assistants.create

功能：创建assistant实例

```python
def create(self,
            name: str,
            description: str,
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

- appbuilder.assistant.assistants.create 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#1%E5%88%9B%E5%BB%BAassistant)

- appbuilder.assistant.assistants.create 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)

```python
class AssistantCreateRequest(BaseModel):
    model: str = Field(default="ERNIE-4.0-8K")  # 使用的模型
    name: str = Field(default="", min_length=1, max_length=128, pattern="^[\u4e00-\u9fa50-9a-zA-Z_-]+$")  # 助理名称
    description: str = Field(default="", max_length=512)  # 助理描述
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: str = Field(default="你是百度制作的AI助手", max_length=4096)  # 助理的通用指令
    thought_instructions: str = Field(default="", max_length=4096)  # 助理的思维指令
    chat_instructions: str = Field(default="", max_length=4096)  # 助理的聊天指令
    tools: list[AssistantTool] = Field(default=[], max_length=10)  # 助理使用的工具列表
    file_ids: list[str] = Field(default=[], max_length=10)  # 关联文件的ID列表
    metadata: dict = Field(default={}, max_length=16)  # 元数据
```

- appbuilder.assistant.assistants.create 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

```python
class AssistantCreateResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    object: Optional[str] = ""  # 助理对象标识
    name: Optional[str] = ""  # 助理名称
    description: Optional[str] = ""  # 助理描述
    instructions: Optional[str]  # 助理的通用指令
    tools: Optional[list[AssistantTool]] = Field(default=[])  # 助理使用的工具列表
    created_at: Optional[int] = 0  # 助理创建时间戳
    thought_instructions: Optional[str] = ""  # 助理的思维指令
    chat_instructions: Optional[str] = ""  # 助理的聊天指令
    response_format: Optional[ResponseFormat] = Field(default=ResponseFormat.TEXT)  # 响应格式
    file_ids: Optional[list[str]] = Field(default=[])  # 关联文件的ID列表
    metadata: Optional[dict] = Field(default={}, max_length=16)  # 元数据
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

- appbuilder.assistant.assistants.update 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#2%E4%BF%AE%E6%94%B9assistant)

- appbuilder.assistant.assistants.update 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-1)

```python
class AssistantUpdateRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    model: str = Field(default="ERNIE-4.0-8K")  # 使用的模型
    name: str = Field(default="", min_length=1, max_length=128, pattern="^[\u4e00-\u9fa50-9a-zA-Z_-]+$")   # 助理名称
    description: str = Field(default="", max_length=512)  # 助理描述
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: str = Field(default="你是百度制作的AI助手", max_length=4096)  # 助理的通用指令
    thought_instructions: str = Field(default="", max_length=4096)  # 助理的思维指令
    chat_instructions: str = Field(default="", max_length=4096)  # 助理的聊天指令
    tools: list[AssistantTool] = Field(default=[], max_length=10)  # 助理使用的工具列表
    file_ids: list[str] = Field(default=[], max_length=10)  # 关联文件的ID列表
    metadata: dict = Field(default={}, max_length=16)  # 元数据
```

- appbuilder.assistant.assistants.update 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-1)

```python
class AssistantUpdateResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    model: Optional[str] = ""  # 助理对象标识
    name: Optional[str] = ""  # 助理名称
    description: Optional[str] = ""  # 助理描述
    response_format: Optional[ResponseFormat] = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: Optional[str]  # 助理的通用指令
    created_at: Optional[int] = 0  # 助理创建时间戳
    thought_instructions: Optional[str] = ""  # 助理的思维指令
    chat_instructions: Optional[str] = ""  # 助理的聊天指令
    tools: Optional[list[AssistantTool]] = Field(default=[])  # 助理使用的工具列表
    file_ids: Optional[list[str]] = Field(default=[])  # 关联文件的ID列表
    metadata: Optional[dict] = Field(default={}, max_length=16)  # 元数据
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

- appbuilder.assistant.assistants.list 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#3-%E6%9F%A5%E8%AF%A2assistant%E5%88%97%E8%A1%A8)

- appbuilder.assistant.assistants.list 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-2)

```python
class AssistantListRequest(BaseModel):
    limit: Optional[int] =   Field(default=20) # 列举结果数量上限
    order: Optional[AssistantListRole] =   Field(default= AssistantListRole.DESC) # 排序字段
    after: Optional[str] =   Field(default="") # 查询指定assistant_id之后创建的Assistant
    before: Optional[str] =   Field(default="") # 查询指定assistant_id之前创建的Assistant
```

- appbuilder.assistant.assistants.list 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-2)

```python
class AssistantListResponse(BaseModel):
    object: str = "list" # 结构类型，返回值固定为 list
    data: Optional[list[AssistantCreateResponse]] = Field(default=[]) # Assistant对象列表
    first_id: Optional[str] = "" # 返回的列表中第一条assistant的id
    last_id: Optional[str] = "" # 返回的列表中最后一条assistant的id
    has_more: bool = False # 是否还有更多的数据
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

- appbuilder.assistant.assistants.query 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#4-%E6%9F%A5%E8%AF%A2assistant)

- appbuilder.assistant.assistants.query 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-3)

```python
class AssistantQueryRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
```

- appbuilder.assistant.assistants.query 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-3)

```python
class AssistantQueryResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    object: Optional[str] = ""  # 助理对象标识
    name: Optional[str] = ""  # 助理名称
    description: Optional[str] = ""  # 助理描述
    instructions: Optional[str]  # 助理的通用指令
    tools: Optional[list[AssistantTool]] = Field(default=[])  # 助理使用的工具列表
    created_at: Optional[int] = 0  # 助理创建时间戳
    thought_instructions: Optional[str] = ""  # 助理的思维指令
    chat_instructions: Optional[str] = ""  # 助理的聊天指令
    response_format: Optional[ResponseFormat] = Field(default=ResponseFormat.TEXT)  # 响应格式
    file_ids: Optional[list[str]] = Field(default=[])  # 关联文件的ID列表
    metadata: Optional[dict] = Field(default={}, max_length=16)  # 元数据 
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

- appbuilder.assistant.assistants.delete 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#5-%E5%88%A0%E9%99%A4assistant)

- appbuilder.assistant.assistants.delete 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-4)

```python
class AssistantDeleteRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
```

- appbuilder.assistant.assistants.delete 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-4)

```python
class AssistantDeleteResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    object: Optional[str] = ""  # 助理对象标识
    deleted: bool = False  # 删除状态
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

- appbuilder.assistant.assistants.mount_files 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#6-%E6%8C%82%E8%BD%BDfile%E5%88%B0assistant)

- appbuilder.assistant.assistants.mount_files 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-5)

```python
class AssistantFilesRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    file_id: Optional[str] = ""  # File对象的id
```

- appbuilder.assistant.assistants.mount_files 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-5)

```python
class AssistantFilesResponse(BaseModel):
    id: Optional[str] = ""  # File对象的id，值等于入参
    object: Optional[str] = ""  # 助理对象标识
    created_at: Optional[int] = 0  # 助理创建时间戳
    assistant_id: Optional[str] = ""  # Assistant对象的id，值等于入参
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

- appbuilder.assistant.assistants.mounted_files_list 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#7-%E6%9F%A5%E8%AF%A2assistant%E6%8C%82%E8%BD%BD%E7%9A%84file%E5%88%97%E8%A1%A8)

- appbuilder.assistant.assistants.mounted_files_list 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-6)

```python
class AssistantFilesDeleteRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    file_id: Optional[str] = ""  # File对象的id
```

- appbuilder.assistant.assistants.mounted_files_list 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-6)

```python
class AssistantFilesContentResponse(BaseModel):
    content_type:Optional[str] = ""  # 文件类型
    content :Optional[bytes] =b"" # 二进制流数据
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

- appbuilder.assistant.assistants.unmount_files 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#8-%E8%A7%A3%E7%BB%91assistant%E6%8C%82%E8%BD%BD%E7%9A%84file)

- appbuilder.assistant.assistants.unmount_files 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-7)

```python
class AssistantFilesDeleteRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    file_id: Optional[str] = ""  # File对象的id
```

- appbuilder.assistant.assistants.unmount_files 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qluzl0y5e#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-7)

```python
class AssistantFilesDeleteResponse(BaseModel):
    id: str = ""  # 文件ID
    object: str = ""  # 文件对象标识
    deleted: bool = False  # 是否删除成功	
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

- appbuilder.assistant.assistants.files.create 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#1%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6)

- appbuilder.assistant.assistants.files.create 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)

```python
file_path (str): 要上传的文件路径。
purpose (str, optional): 上传文件的用途。默认为 "assistant"。
```

- appbuilder.assistant.assistants.files.create 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

```python
class AssistantFilesCreateResponse(BaseModel):
    id: str = ""  # 文件ID
    bytes: int = 0  # 文件大小（字节）
    object: str = ""  # 文件对象标识
    purpose: str = ""  # 文件用途
    create_at: int = 0  # 文件创建时间戳
    filename: str = ""  # 文件名
    classification_id: str = ""  # 文件分类ID
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

- appbuilder.assistant.assistants.files.list 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#2%E6%9F%A5%E8%AF%A2%E5%B7%B2%E4%B8%8A%E4%BC%A0%E7%9A%84%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8)

- appbuilder.assistant.assistants.files.list 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-1)

```python
class AssistantFilesListResponse(BaseModel):
    object :str = "list"
    data: list[AssistantFilesListData] = []
```
**注：**AssistantFilesListData类即为AssistantFilesQueryResponse类

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

- appbuilder.assistant.assistants.files.query 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#3%E6%9F%A5%E8%AF%A2%E5%B7%B2%E4%B8%8A%E4%BC%A0%E7%9A%84%E6%96%87%E4%BB%B6%E4%BF%A1%E6%81%AF)

- appbuilder.assistant.assistants.files.query 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-2)

```python
file_id (str): 文件ID
```

- appbuilder.assistant.assistants.files.query 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-2)

```python
class AssistantFilesQueryResponse(BaseModel):
    id: str = ""  # 文件ID
    bytes: int = 0  # 文件大小（字节）
    object: str = ""  # 文件对象标识
    purpose: str = ""  # 文件用途
    censored :AuditStatus = Field()  # 审核状态
    create_at: int = 0  # 文件创建时间戳
    filename: str = ""  # 文件名
    classification_id: str = ""  # 文件分类ID
    file_type: str = "" # 文件类型
```

#### appbuilder.assistant.assistants.files.delete

功能：根据file_id删除一个已上传的文件

```python
def delete(self,
        file_id: str,
    ) -> assistant_type.AssistantFilesDeleteResponse:
"""
删除文件
Args:
    file_id (str): 文件ID
Returns:
    assistant_type.AssistantFilesDeleteResponse: 删除文件后的响应对象。
Raises:
    无
"""
```

- appbuilder.assistant.assistants.files.delete 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#4%E5%88%A0%E9%99%A4%E6%96%87%E4%BB%B6)

- appbuilder.assistant.assistants.files.delete 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-3)

```python
file_id (str): 文件ID
```

- appbuilder.assistant.assistants.files.delete 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-3)

```python
class AssistantFilesDeleteResponse(BaseModel):
    id: str = ""  # 文件ID
    object: str = ""  # 文件对象标识
    deleted: bool = False  # 是否删除成功	
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

- appbuilder.assistant.assistants.files.download 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#5%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6)

- appbuilder.assistant.assistants.files.download 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-4)

```python
file_id (str): 文件ID
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

- appbuilder.assistant.assistants.files.content 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#6%E6%9F%A5%E7%9C%8B%E6%96%87%E4%BB%B6%E5%86%85%E5%AE%B9)

- appbuilder.assistant.assistants.files.content 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/ulv0g1t3x#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-5)

```python
file_id (str): 文件ID
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

- appbuilder.assistant.threads.create 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#1-%E5%88%9B%E5%BB%BAthread)

- appbuilder.assistant.threads.create 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)

```python
class ThreadCreateRequest(BaseModel):
    messages: list[AssistantMessage]
```

- appbuilder.assistant.threads.create 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

```python
class ThreadCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    created_at: int = 0
    metadata: dict = {}
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

- appbuilder.assistant.threads.query 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#2-%E6%9F%A5%E8%AF%A2thread)

- appbuilder.assistant.threads.query 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-1)

```python
class ThreadQueryRequest(BaseModel):
    thread_id: str
```

- appbuilder.assistant.threads.query 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-1)

```python
class ThreadQueryResponse(BaseModel):
    id: str = ""
    object: str = ""
    created_at: int = 0
    metadata: dict = {}
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

- appbuilder.assistant.threads.delete 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#3-%E5%88%A0%E9%99%A4thread)

- appbuilder.assistant.threads.delete 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-2)

```python
class ThreadDeleteRequest(BaseModel):
    thread_id: str
```

- appbuilder.assistant.threads.delete 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-2)

```python
class ThreadDeleteResponse(BaseModel):
    id: str = ""
    object: str = ""
    deleted: bool = False
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

- appbuilder.assistant.threads.update 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#4-%E4%BF%AE%E6%94%B9thread)

- appbuilder.assistant.threads.update 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-3)

```python
class ThreadUpdateRequest(BaseModel):
    thread_id: str
    metadata: Optional[dict] = Field(default={}, max_length=16)
```

- appbuilder.assistant.threads.update 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/Nlv0g3e50#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-3)

```python
class ThreadUpdateResponse(BaseModel):
    id: str = ""
    object: str = ""
    created_at: Optional[int] = 0
    metadata: Optional[dict] = {}
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

- appbuilder.assistant.threads.messages.create 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#1-%E5%88%9B%E5%BB%BAmessage)

- appbuilder.assistant.threads.messages.create 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)

```python
class AssistantMessageCreateRequest(BaseModel):
    thread_id: str
    role: AssistantMessageRole = Field(
        default=AssistantMessageRole.USER)
    content: str
    file_ids: Optional[list[str]] =  Field(default=[], max_length=10)
```

- appbuilder.assistant.threads.messages.create 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

```python
class AssistantMessageCreateResponse(BaseModel):
    id: str = ""
    object: str = ""
    role: AssistantMessageRole = Field(
        default=AssistantMessageRole.USER)
    content: Optional[list[AssistantContent]] = []
    created_at: int = 0
    thread_id: str = ""
    assistant_id: Optional[str] = ""
    run_id: Optional[str] = ""
    file_ids: Optional[list[str]] = []
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

- appbuilder.assistant.threads.messages.list 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#2-%E6%9F%A5%E8%AF%A2thread%E4%B8%8B%E7%9A%84message%E5%88%97%E8%A1%A8)

- appbuilder.assistant.threads.messages.list 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-1)

```python
class AssistantMessageListRequest(BaseModel):
    thread_id: str
    limit: int = -20
    order: AssistantMessageListRole = Field(
        default=AssistantMessageListRole.DESC)
    after: str = ""
    before: str = ""
```

- appbuilder.assistant.threads.messages.list 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-1)

```python
class AssistantMessageListResponse(BaseModel):
    object: str = ""
    data: list[AssistantMessageListResponseData] = []
    first_id: Optional[str] = ""
    last_id: Optional[str] = ""
    has_more: bool = False
```
**注：**AssistantMessageListResponseData类即为AssistantMessageQueryResponse类

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

- appbuilder.assistant.threads.messages.query 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#3-%E6%9F%A5%E8%AF%A2%E6%8C%87%E5%AE%9Amessage)

- appbuilder.assistant.threads.messages.query 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-2)

```python
class AssistantMessageQueryRequest(BaseModel):
    thread_id: str
    message_id: str
```

- appbuilder.assistant.threads.messages.query 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-2)

```python
class AssistantMessageQueryResponse(BaseModel):
    id: str = ""
    object: str = ""
    role: AssistantMessageRole = Field()
    content: Optional[list[AssistantContent]] = []
    created_at: int = 0
    thread_id: str = ""
    assistant_id: Optional[str] = ""
    run_id: Optional[str] = ""
    file_ids: Optional[list[str]] = []
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

- appbuilder.assistant.threads.messages.update 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#4-%E4%BF%AE%E6%94%B9message%E5%AF%B9%E8%B1%A1)

- appbuilder.assistant.threads.messages.update 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-3)

```python
class AssistantMessageUpdateRequest(BaseModel):
    thread_id: str
    message_id: str
    content: Optional[str] 
    file_ids: Optional[list[str]] = []
```

- appbuilder.assistant.threads.messages.update 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-3)

```python
class AssistantMessageUpdateResponse(BaseModel):
    id: str = ""
    object: str = ""
    role: AssistantMessageRole = Field(default=AssistantMessageRole.USER)
    content: Optional[list[AssistantContent]] = []
    created_at: int = 0
    thread_id: str = ""
    assistant_id: Optional[str] = ""
    run_id: Optional[str] = ""
    file_ids: Optional[list[str]] = []
```

#### appbuilder.assistant.threads.messages.files

功能：查询一个Message对象下的文件列表

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

- appbuilder.assistant.threads.messages.files 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#5-%E6%9F%A5%E8%AF%A2message%E4%B8%8B%E7%9A%84%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8)

- appbuilder.assistant.threads.messages.files 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-4)

```python
class AssistantMessageFilesRequest(BaseModel):
    thread_id: str
    message_id: str
    limit: int = -20
    order : AssistantMessageListRole = Field(
        default=AssistantMessageListRole.DESC)
    after: str = ""
    before: str = ""
```

- appbuilder.assistant.threads.messages.files 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/qlv0g47sk#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-4)

```python
class AssistantMessageFilesResponse(BaseModel):
    object: str = ""
    data: list[AssistantContentFilesData] = []
    first_id: Optional[str] = ""
    last_id: Optional[str] = ""
    has_more: bool = False
```
**注：**AssistantContentFilesData类即为AssistantFilesResponse类


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
        model_parameters: Optional[public_type.AssistantModelParameters] = None,
        user_info: Optional[public_type.AssistantUserInfo] = None,
        user_loc: Optional[public_type.AssistantUserLoc] = None,
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
        model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型运行参数. Defaults to None.
        user_info (Optional[public_type.AssistantUserInfo], optional): 用户身份信息. Defaults to None.
        user_loc (Optional[public_type.AssistantUserLoc], optional): 用户定位信息. Defaults to None.
    Returns:
        thread_type.RunResult: 运行结果

    Raises:
        ValueError: thread_id和thread不能同时为空,model_parameters的各个参数不在规定范围内

    Note:
        1. 如果thread_id没有传，则thread必须要传值
        2. 如果这里不传值，thread_id查出来的历史对话，最后一条消息的role必须为user
        3. 如果这里传值，则需要保证thread_id查出来的历史对话 + 本轮追加的thread对话，最后一条消息的role必须为user
    """
```

- appbuilder.assistant.threads.runs.run 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#1-%E8%BF%90%E8%A1%8C)

- appbuilder.assistant.threads..runs.run 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0)

```python
class AssistantRunRequest(BaseModel):
    thread_id: Optional[str] = Field(default="")
    model: str = Field(default="ERNIE-4.0-8K")
    assistant_id: Optional[str] = Field(default="")
    metadata: Optional[dict] =  Field(default={}, max_length=16)
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)
    instructions: Optional[str] = Field(default="", max_length=4096)
    thought_instructions: Optional[str] = Field(default="", max_length=4096)
    chat_instructions: Optional[str] = Field(default="", max_length=4096)
    stream: Optional[bool] = False
    model_parameters: Optional[AssistantModelParameters] = AssistantModelParameters()
    class Config:
        extra = "forbid"
        protected_namespaces = ()
    thread: Optional[AssistantThread] = None
    tools: Optional[list[AssistantTool]] = []
    tool_output: Optional[ToolOutput] = None
    user_info: Optional[AssistantUserInfo] = None
    user_loc: Optional[AssistantUserLoc] = None
```

- appbuilder.assistant.threads..runs.run 的[流式响应参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E6%B5%81%E5%BC%8F%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

- appbuilder.assistant.threads..runs.run 的[非流式响应参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E9%9D%9E%E6%B5%81%E5%BC%8F%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0)

```python
class RunResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""

    model: str = ""
    instructions: str = ""
    thought_instructions: str = ""
    chat_instructions: str = ""
    tools: Optional[list[AssistantTool]] = None
    file_ids: Optional[list[str]] = None

    status: str = ""
    required_action: Optional[RequiredAction] = None
    last_error: Optional[LastError] = None
    final_answer: Optional[FinalAnswer] = None
    created_at: int = 0
    started_at: int = 0
    expired_at: int = 0
    cancelled_at: int = 0
    failed_at: int = 0
    completed_at: int = 0
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
        model_parameters: Optional[public_type.AssistantModelParameters] = None,
        user_info: Optional[public_type.AssistantUserInfo] = None,
        user_loc: Optional[public_type.AssistantUserLoc] = None,
        ) -> Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]:
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
    model_parameters (Optional[public_type.AssistantModelParameters], optional): 模型参数对象。默认为None。

    Returns:
    Union[thread_type.StreamRunStatus, thread_type.StreamRunMessage, None]: 返回一个迭代器，每次迭代返回一个处理结果对象，可能是 StreamRunStatus 或 StreamRunMessage。

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

- appbuilder.assistant.threads.runs.submit_tool_outputs 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#2-%E6%B5%81%E5%BC%8F%E8%B0%83%E7%94%A8%E6%97%B6%E6%8F%90%E4%BA%A4%E5%B7%A5%E5%85%B7%E8%BE%93%E5%87%BA)

- appbuilder.assistant.threads..runs.submit_tool_outputs 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-1)

```python
class AssistantSubmitToolOutputsRequest(BaseModel):
    thread_id: str = Field(default="", min_length=1)
    run_id: str = Field(default="", min_length=1)
    tool_outputs: Optional[list[ToolOutput]] = Field(default=[], min_length=1)
```

- appbuilder.assistant.threads..runs.submit_tool_outputs 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E5%93%8D%E5%BA%94%E8%AF%B4%E6%98%8E-1)


```python
class RunResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""

    model: str = ""
    instructions: str = ""
    thought_instructions: str = ""
    chat_instructions: str = ""
    tools: Optional[list[AssistantTool]] = None
    file_ids: Optional[list[str]] = None

    status: str = ""
    required_action: Optional[RequiredAction] = None
    last_error: Optional[LastError] = None
    final_answer: Optional[FinalAnswer] = None
    created_at: int = 0
    started_at: int = 0
    expired_at: int = 0
    cancelled_at: int = 0
    failed_at: int = 0
    completed_at: int = 0
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

- appbuilder.assistant.threads.runs.cancel 对应的 [Assistant API 链接](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#3-%E6%B5%81%E5%BC%8F%E8%B0%83%E7%94%A8%E6%97%B6%E5%8F%96%E6%B6%88%E8%BF%90%E8%A1%8C)

- appbuilder.assistant.threads..runs.cancel 的[请求参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0-2)

```python
class AssistantRunCancelRequest(BaseModel):
    thread_id: str = Field(default="", min_length=1)
    run_id: str = Field(default="", min_length=1)

```

- appbuilder.assistant.threads..runs.cancel 的[响应参数](https://cloud.baidu.com/doc/AppBuilder/s/dlv0g4x9m#%E5%93%8D%E5%BA%94%E5%8F%82%E6%95%B0-1)


```python
class RunResult(BaseModel):
    id: str = ""
    object: str = ""
    assistant_id: str = ""
    thread_id: str = ""

    model: str = ""
    instructions: str = ""
    thought_instructions: str = ""
    chat_instructions: str = ""
    tools: Optional[list[AssistantTool]] = None
    file_ids: Optional[list[str]] = None

    status: str = ""
    required_action: Optional[RequiredAction] = None
    last_error: Optional[LastError] = None
    final_answer: Optional[FinalAnswer] = None
    created_at: int = 0
    started_at: int = 0
    expired_at: int = 0
    cancelled_at: int = 0
    failed_at: int = 0
    completed_at: int = 0

```


## appbuilder.assistant公共类

- AssistantTool

```python
class AssistantTool(BaseModel):
    """
    表示助理工具的模型。

    Attributes:
        type (str): 工具的类型，默认为 'function'。
        function (AssistantFunction): 功能的实例。
    """
    type: str = 'function'
    function: AssistantFunction = None
```

- AssistantContent

```python
class AssistantContent(BaseModel):
    """
    表示助理内容的模型。

    Attributes:
        type (str): 内容类型，默认为 "text"。
        text (Optional[AssistantText]): 文本内容的实例，默认为None。
    """
    type: str = "text"
    text: Optional[AssistantText] = None
```

- AssistantText

```python
class AssistantText(BaseModel):
    """
    表示助理文本内容的模型。

    Attributes:
        value (str): 文本的值。
        annotations (Optional[list[str]]): 文本的注解列表，默认为None。
    """
    value: str = ""
    annotations: Optional[list[str]] = None
```

- ResponseFormat

```python
class ResponseFormat(str, Enum):
    """
    表示响应格式的枚举类型。

    Values:
        TEXT: 文本格式。
        JSON_OBJECT: JSON对象格式。
    """
    TEXT = 'text'
    JSON_OBJECT = 'json_object'
```

- AssistantModelParameters
  - AssistantThoughtParameters
  - AssistantChatParameters

```python
class AssistantModelParameters(BaseModel):
    """
    表示助理模型的参数的模型。
    Attributes:
        chat_parameters (Optional[AssistantChatParameters]): 聊天参数的实例，默认为None。
        thought_parameters (Optional[AssistantThoughtParameters]): 思考参数的实例，默认为None。
    """
    chat_parameters: Optional[AssistantChatParameters] = AssistantChatParameters()
    thought_parameters: Optional[AssistantThoughtParameters] = AssistantThoughtParameters()


class AssistantThoughtParameters(BaseModel):
    """
    表示助理思考参数的模型。
    Attributes:
        temperature (Optional[float]): 	采样温度，较高的数值会使输出更随机。取值范围严格大于0，小于等于1，默认为0.01。
        top_p (Optional[float]): top_p，核采样方法的概率阈值，影响输出文本的多样性，较低的数值会使输出的文本更加多样性。取值范围大于等于0，小于等于1，默认为0。
        penalty_score (Optional[float]): 惩罚分数，影响输出文本的多样性和质量，较高的数值使输出的文本更加多样性。取值范围大于等于1，小于等于2，默认为1.0。
    """
    temperature: Optional[float] = 0.01
    top_p: Optional[float] = 0
    penalty_score: Optional[float] = 1.0


class AssistantChatParameters(BaseModel):
    """
    表示助理聊天参数的模型。
    Attributes:
        temperature (Optional[float]): 	采样温度，较高的数值会使输出更随机。取值范围严格大于0，小于等于1，默认为0.8。
        top_p (Optional[float]): top_p，核采样方法的概率阈值，影响输出文本的多样性，较低的数值会使输出的文本更加多样性。取值范围大于等于0，小于等于1，默认为0.8。
        penalty_score (Optional[float]): 惩罚分数，影响输出文本的多样性和质量，较高的数值使输出的文本更加多样性。
    """
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 0.8
    penalty_score: Optional[float] = 1.0
```


-AssistantUserInfo

```python
class AssistantUserInfo(BaseModel):
    """
    表示用户信息。
    Attributes:
        id (Optional[str]): 用户ID，默认为None。
        name (Optional[str]): 用户名称，默认为None。
        nickname (Optional[str]): 用户昵称，默认为None。
        watermark (Optional[str]): 用户水印，默认为None。
        intro (Optional[str]): 用户简介，默认为None。
        baidu_id (Optional[str]): 用户百度ID，默认为None。
    """
    id:Optional[str] = None
    name:Optional[str] = None
    nickname:Optional[str] = None
    watermark:Optional[str] = None
    intro:Optional[str] = None
    baidu_id: Optional[str] = None 
```

- AssistantUserLoc

```python
class AssistantUserLoc(BaseModel):
    """
    表示用户位置信息。
    Attributes:
        loc (Optional[str]): 用户当前的地理位置信息，使用json格式描述
        uip (Optional[str]): 用户的ipv4地址
        uipv6 (Optional[str]): 用户的ipv6地址
    """
    loc:Optional[str] = None
    uip:Optional[str] = None
    uipv6:Optional[str] = None

```