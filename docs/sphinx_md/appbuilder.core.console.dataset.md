# appbuilder.core.console.dataset package

## Submodules

## appbuilder.core.console.dataset.dataset module

### *class* appbuilder.core.console.dataset.dataset.Dataset(dataset_id: str = '', dataset_name: str = '')

基类：`object`

console知识库操作工具

Examples:

```python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = '...'

dataset = appbuilder.Dataset.create_dataset("baidu-test")

# 上传文档
file_paths = ["./test.pdf"]
document_infos = dataset.add_documents(file_paths)

# 获取第一页的文档列表, 每页10条
document_list = dataset.get_documents(1, 10)

# 删除文档
document_ids = [document_infos.document_ids[0]]
dataset.delete_documents(document_ids)
```

#### add_documents(file_path_list: List[str], is_custom_process_rule: bool = False, custom_process_rule: Dict = None, is_enhanced: bool = False) → AddDocumentsResponse

向知识库中添加文档

* **参数:**
  * **file_path_list** – 文档路径列表
  * **is_custom_process_rule** – 是否使用自定义文档处理规则, 默认为False, 使用平台的默认规则，为True时使用自定义规则
  * **custom_process_rule** – 自定义文档规则，当is_custom_process_rule为True时生效，格式示例如下：
  * **{** – “separators”: [”。”, “，”],    # 文本切分符，支持这几种[ , , “？”, , “!”, “?”, “……”]
    “target_length”: 300,         # 文本切片片段长度，取值范围[300, 800]
    “overlap_rate”: 0.3           # 文本片段重叠率，取值范围[0, 0.3]
  * **}**
  * **is_enhanced** – 是否开启知识增强, 默认为False，在检索问答时通过知识点来索引到对应的切片，大模型根据切片内容生成答案，开启知识增强会调用大模型抽取更加丰富的知识点，增加切片的召回率
* **返回:**
  添加文档的响应结果，包含以下属性：
  - dataset_id (str): 知识库id
  - document_ids (List[str]): 文档id列表
* **返回类型:**
  AddDocumentsResponse

#### add_file_url *: str* *= '/v1/ai_engine/agi_platform/v1/datasets/documents'*

#### *classmethod* create_dataset(dataset_name: str)

创建知识库

* **参数:**
  **dataset_name** – 知识库名称
* **返回:**
  创建成功的知识库实例
* **返回类型:**
  [Dataset](#appbuilder.core.console.dataset.dataset.Dataset)

#### create_url *: str* *= '/v1/ai_engine/agi_platform/v1/datasets/create'*

#### delete_documents(document_ids: List[str])

删除知识库中的文档

* **参数:**
  **document_ids** – 文档id列表
* **返回:**
  None

#### delete_file_url *: str* *= '/v1/ai_engine/agi_platform/v1/datasets/document/delete'*

#### get_documents(page: int, limit: int, keyword: str = '') → DocumentListResponse

获取知识库中的文档列表

* **参数:**
  * **page** – 第几页
  * **limit** – 每页文档数
  * **keyword** – 文件名关键字，支持模糊查询
* **返回:**
  DocumentListResponses实例，返回示例：
  {
  “data”: [
  > {
  > : “id”:”d2d1bc1a-1763-4162-88b2-0dad225da16f”, # 文档id
  >   “name”: “唐诗三百首（全集）全新编辑版.pdf”, # 文档名称
  >   “created_from”: “web”, # 创建来源
  >   “created_by”: “76efed91-cf19-435d-993c-cdd901d6d13c”, # 创建人
  >   “created_at”: 1705958975, # 创建时间
  >   “indexing_status”: “indexing”, # 文档处理状态
  >   “error”: null, # 文档处理错误信息
  >   “enabled”: true, # 文档是否启用
  >   “disabled_at”: null, # 文档禁用时间
  >   “disabled_by”: null, # 文档禁用人
  >   “display_status”: “indexing”, # 文档显示状态，和前端展示状态一致
  >   “word_count”: 5024 # 文档字数

  > }

  ],
  “has_more”: false, # 是否还有下一页
  “limit”: 10, # 每页文档数
  “total”: 1, # 总页数
  “page”: 1 # 当前页
  }

#### get_file_list_url *: str* *= '/v1/ai_engine/agi_platform/v1/datasets/documents/list_page'*

#### *property* http_client

#### upload_file_url *: str* *= '/v1/ai_engine/agi_platform/v1/datasets/files/upload'*
