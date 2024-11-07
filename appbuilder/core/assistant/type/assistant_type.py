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

from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from enum import Enum
from appbuilder.core.assistant.type import (
    AssistantTool,
    ResponseFormat
)

# AssistantFilesCreateResponse类，用于描述创建助理文件后的响应信息
class AssistantFilesCreateResponse(BaseModel):
    id: str = ""  # 文件ID
    bytes: int = 0  # 文件大小（字节）
    object: str = ""  # 文件对象标识
    purpose: str = ""  # 文件用途
    create_at: int = 0  # 文件创建时间戳
    filename: str = ""  # 文件名
    classification_id: str = ""  # 文件分类ID
    
class AuditStatus(int,Enum):
    AUDITING = -1, # 审核中 
    NOT_AUDITED = 0, # 未审核
    APPROVED = 1, # 审核通过
    REJECTED = 2, # 审核不通过
    NEEDS_FURTHER_AUDIT = 3, # 需要进一步审核
    AUDIT_FAILED_SERVICE_EXCEPTION = 4, # 审核失败（服务异常）
    AUDIT_FAILED_TIMEOUT = 5, # 审核失败（审核超时）


class AssistantFilesListData(BaseModel):
    id: str = ""  # 文件ID
    bytes: int = 0  # 文件大小（字节）
    object: str = ""  # 文件对象标识
    purpose: str = ""  # 文件用途
    censored :AuditStatus = Field()  # 审核状态
    create_at: int = 0  # 文件创建时间戳
    filename: str = ""  # 文件名
    classification_id: str = ""  # 文件分类ID
    file_type: str = "" # 文件类型
    

class AssistantFilesListResponse(BaseModel):
    object :str = "list"
    data: list[AssistantFilesListData] = []
    

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
    
class AssistantFilesDeleteResponse(BaseModel):
    id: str = ""  # 文件ID
    object: str = ""  # 文件对象标识
    deleted: bool = False  # 是否删除成功	

# AssistantCreateRequest类，用于描述创建助理的请求参数
class AssistantCreateRequest(BaseModel):
    model: str = Field(default="ERNIE-4.0T-8K")  # 使用的模型
    name: str = Field(default="", min_length=1, max_length=128, pattern="^[\u4e00-\u9fa50-9a-zA-Z_-]+$")  # 助理名称
    description: str = Field(default="", max_length=512)  # 助理描述
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: str = Field(default="你是百度制作的AI助手", max_length=4096)  # 助理的通用指令
    thought_instructions: str = Field(default="", max_length=4096)  # 助理的思维指令
    chat_instructions: str = Field(default="", max_length=4096)  # 助理的聊天指令
    tools: list[AssistantTool] = Field(default=[], max_length=10)  # 助理使用的工具列表
    file_ids: list[str] = Field(default=[], max_length=10)  # 关联文件的ID列表
    metadata: dict = Field(default={}, max_length=16)  # 元数据


# AssistantCreateResponse类，用于描述创建助理后的响应信息
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

class AssistantUpdateRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    model: str = Field(default="ERNIE-4.0T-8K")  # 使用的模型
    name: str = Field(default="", min_length=1, max_length=128, pattern="^[\u4e00-\u9fa50-9a-zA-Z_-]+$")   # 助理名称
    description: str = Field(default="", max_length=512)  # 助理描述
    response_format: ResponseFormat = Field(default=ResponseFormat.TEXT)  # 响应格式
    instructions: str = Field(default="你是百度制作的AI助手", max_length=4096)  # 助理的通用指令
    thought_instructions: str = Field(default="", max_length=4096)  # 助理的思维指令
    chat_instructions: str = Field(default="", max_length=4096)  # 助理的聊天指令
    tools: list[AssistantTool] = Field(default=[], max_length=10)  # 助理使用的工具列表
    file_ids: list[str] = Field(default=[], max_length=10)  # 关联文件的ID列表
    metadata: dict = Field(default={}, max_length=16)  # 元数据
    
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
    
    
class AssistantListRole(str, Enum):
    DESC = 'desc'
    ASC = 'asc'

class AssistantListRequest(BaseModel):
    limit: Optional[int] =   Field(default=20) # 列举结果数量上限
    order: Optional[AssistantListRole] =   Field(default= AssistantListRole.DESC) # 排序字段
    after: Optional[str] =   Field(default="") # 查询指定assistant_id之后创建的Assistant
    before: Optional[str] =   Field(default="") # 查询指定assistant_id之前创建的Assistant
    
class AssistantListResponse(BaseModel):
    object: str = "list" # 结构类型，返回值固定为 list
    data: Optional[list[AssistantCreateResponse]] = Field(default=[]) # Assistant对象列表
    first_id: Optional[str] = "" # 返回的列表中第一条assistant的id
    last_id: Optional[str] = "" # 返回的列表中最后一条assistant的id
    has_more: bool = False # 是否还有更多的数据
    
class AssistantQueryRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    
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
    
    
class AssistantDeleteRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    
    
class AssistantDeleteResponse(BaseModel):
    id: Optional[str] = ""  # 助理ID
    object: Optional[str] = ""  # 助理对象标识
    deleted: bool = False  # 删除状态
    
class AssistantFilesRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    file_id: Optional[str] = ""  # File对象的id
    
class AssistantFilesResponse(BaseModel):
    id: Optional[str] = ""  # File对象的id，值等于入参
    object: Optional[str] = ""  # 助理对象标识
    created_at: Optional[int] = 0  # 助理创建时间戳
    assistant_id: Optional[str] = ""  # Assistant对象的id，值等于入参
    
class AssistantMountedFilesListRequest(BaseModel):
    assistant_id: Optional[str] = ""  # Assistant对象的id
    limit: Optional[int] =   Field(default=20) # 列举结果数量上限
    order: AssistantListRole = Field(default= AssistantListRole.DESC) # 排序字段
    after: Optional[str] =   Field(default="") # 查询指定file_id之后创建的File
    before: Optional[str] =   Field(default="") # 查询指定file_id之前创建的File

class AssistantMountedFilesListResponse(BaseModel):
    object: str = "list" # 结构类型，返回值固定为 list
    data: Optional[list[AssistantFilesResponse]] = Field(default=[]) # file对象列表
    first_id: Optional[str] = "" # 返回的列表中第一条assistant的id
    last_id: Optional[str] = "" # 返回的列表中最后一条assistant的id
    has_more: bool = False # 是否还有更多的数据
    
class AssistantFilesDeleteRequest(BaseModel):
    assistant_id: Optional[str] = ""  # 助理ID
    file_id: Optional[str] = ""  # File对象的id
    
    
class AssistantFilesContentResponse(BaseModel):
    content_type:Optional[str] = ""  # 文件类型
    content :Optional[bytes] =b"" # 二进制流数据
    