from typing import List, Dict
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.dataset.model import DocumentListResponse, AddDocumentsResponse
from appbuilder.core.constants import MAX_DOCUMENTS_NUM, SUPPORTED_FILE_TYPE
import json
import os
from appbuilder.utils.func_utils import deprecated
from appbuilder.utils.trace.tracer_wrapper import client_tool_trace


class Dataset:
    r"""
    console知识库操作工具
    
    Examples:
    
    .. code-block:: python
        
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

    """
    create_url: str = "/v1/ai_engine/agi_platform/v1/datasets/create"
    add_file_url: str = "/v1/ai_engine/agi_platform/v1/datasets/documents"
    get_file_list_url: str = "/v1/ai_engine/agi_platform/v1/datasets/documents/list_page"
    delete_file_url: str = "/v1/ai_engine/agi_platform/v1/datasets/document/delete"
    upload_file_url: str = "/v1/ai_engine/agi_platform/v1/datasets/files/upload"

    def __init__(self, dataset_id: str = "", dataset_name: str = ""):
        r"""
        初始化Dataset实例

        Args:
            dataset_id: 知识库ID
            dataset_name: 知识库名称

        Returns:
            Dataset: 知识库实例
        """
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self._http_client = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client

    @classmethod
    def create_dataset(cls, dataset_name: str):
        r"""
        创建知识库
        
        Args:
            dataset_name: 知识库名称
            
        Returns:
            Dataset: 创建成功的知识库实例
        """
        payload = json.dumps({"name": dataset_name})
        http_client = HTTPClient()
        headers = http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = http_client.session.post(url=http_client.service_url(cls.create_url),
                                            headers=headers, data=payload)
        http_client.check_response_header(response)
        http_client.check_console_response(response)
        response = response.json()["result"]
        return Dataset(dataset_id=response["id"], dataset_name=response["name"])

    @deprecated()
    def add_documents(self, file_path_list: List[str], is_custom_process_rule: bool = False,
                      custom_process_rule: Dict = None, is_enhanced: bool = False) -> AddDocumentsResponse:
        r"""
        向知识库中添加文档
        
        Args:
            file_path_list: 文档路径列表
            is_custom_process_rule: 是否使用自定义文档处理规则, 默认为False, 使用平台的默认规则，为True时使用自定义规则
            custom_process_rule: 自定义文档规则，当is_custom_process_rule为True时生效，格式示例如下：
            {
                "separators": ["。", "，"],    # 文本切分符，支持这几种[ , , "？", , "!", "?", "……"]
                "target_length": 300,         # 文本切片片段长度，取值范围[300, 800]
                "overlap_rate": 0.3           # 文本片段重叠率，取值范围[0, 0.3]
            }
            is_enhanced: 是否开启知识增强, 默认为False，在检索问答时通过知识点来索引到对应的切片，大模型根据切片内容生成答案，开启知识增强会调用大模型抽取更加丰富的知识点，增加切片的召回率
            
        Returns:
            AddDocumentsResponse: 添加文档的响应结果，包含以下属性：
            - dataset_id (str): 知识库id
            - document_ids (List[str]): 文档id列表
        """
        for file_path in file_path_list:
            file_type = file_path.split(".")[-1].lower()
            if file_type not in SUPPORTED_FILE_TYPE:
                raise ValueError(f"Unsupported file type: {file_path}, only support file types: {SUPPORTED_FILE_TYPE}")

        documents = self.get_documents(1, MAX_DOCUMENTS_NUM)
        current_documents_num = len(documents.data)
        if len(file_path_list) + current_documents_num > MAX_DOCUMENTS_NUM:
            raise ValueError(f"too much documents. at most upload {MAX_DOCUMENTS_NUM} documents per dataset，left {MAX_DOCUMENTS_NUM-current_documents_num} documents can be uploaded")

        file_ids = []
        for file_path in file_path_list:
            upload_res = self._upload_document(file_path)
            file_ids.append(upload_res["id"])
        payload = {"dataset_id": self.dataset_id, "file_ids": file_ids,
                   "is_custom_process_rule": is_custom_process_rule, "is_enhanced": is_enhanced}
        if is_custom_process_rule and custom_process_rule:
            payload["custom_process_rule"] = custom_process_rule
        payload = json.dumps(payload)
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.add_file_url),
                                                 headers=headers, data=payload)
        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        res = AddDocumentsResponse.parse_obj(response.json()["result"])
        return res

    def _upload_document(self, file_path: str):
        r"""
        上传文档
        
        Args:
            file_path: 文档路径
            
        Returns:
            上传文档的信息
        """
        headers = self.http_client.auth_header()
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = self.http_client.session.post(url=self.http_client.service_url(self.upload_file_url),
                                                     files=files, headers=headers)
            self.http_client.check_response_header(response)
            self.http_client.check_console_response(response)
            res = response.json()["result"]
        return res

    @deprecated()
    def delete_documents(self, document_ids: List[str]):
        r"""
        删除知识库中的文档
        
        Args:
            document_ids: 文档id列表

        Returns:
            None
        """
        for document_id in document_ids:
            self._delete_document(document_id)

    def _delete_document(self, document_id):
        """
        删除知识库中的文档
        参数：
            document_id: 文档id
        """
        payload = json.dumps({"dataset_id": self.dataset_id, "document_id": document_id})
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.delete_file_url),
                                                 headers=headers, data=payload)
        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)

    @deprecated()
    def get_documents(self, page: int, limit: int, keyword: str = "") -> DocumentListResponse:
        r"""
        获取知识库中的文档列表
        
        Args:
            page: 第几页
            limit: 每页文档数
            keyword: 文件名关键字，支持模糊查询
            
        Returns:
            DocumentListResponses实例，返回示例：
            {
            "data": [
                {
                    "id":"d2d1bc1a-1763-4162-88b2-0dad225da16f", # 文档id
                    "name": "唐诗三百首（全集）全新编辑版.pdf", # 文档名称
                    "created_from": "web", # 创建来源
                    "created_by": "76efed91-cf19-435d-993c-cdd901d6d13c", # 创建人
                    "created_at": 1705958975, # 创建时间
                    "indexing_status": "indexing", # 文档处理状态
                    "error": null, # 文档处理错误信息
                    "enabled": true, # 文档是否启用
                    "disabled_at": null, # 文档禁用时间
                    "disabled_by": null, # 文档禁用人
                    "display_status": "indexing", # 文档显示状态，和前端展示状态一致
                    "word_count": 5024 # 文档字数
                }
            ],
            "has_more": false, # 是否还有下一页
            "limit": 10, # 每页文档数
            "total": 1, # 总页数
            "page": 1 # 当前页
            }
        """
        payload = json.dumps({"dataset_id": self.dataset_id, "page": page, "limit": limit, "keyword": keyword})
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.get_file_list_url),
                                                 headers=headers, data=payload)
        self.http_client.check_response_header(response)
        self.http_client.check_console_response(response)
        res = DocumentListResponse.parse_obj(response.json()["result"])
        return res
