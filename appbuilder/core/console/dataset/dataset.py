from typing import List, Dict
from appbuilder.core._client import HTTPClient
from appbuilder.core.console.dataset.model import FileListResponse, AddFileResponse
import json
import os


class Dataset:
    """
    console知识库操作工具
    Examples:
        .. code-block:: python
        import appbuilder
        import os

        os.environ["APPBUILDER_TOKEN"] = '...'

        dataset = appbuilder.Dataset.create_dataset("baidu-test")

        # 上传文档
        file_paths = ["./test.pdf"]
        file_info = dataset.add_files(file_paths)

        # 获取第一页的文档列表, 每页10条
        file_list = dataset.get_file_list(1, 10)

        # 删除文档
        file_ids = [file_info.document_ids[0]]

    """
    create_url: str = "/v1/ai_engine/agi_platform/v2/datasets/create"
    add_file_url: str = "/v1/ai_engine/agi_platform/v2/datasets/documents"
    get_file_list_url: str = "/v1/ai_engine/agi_platform/v2/datasets/documents/list_page"
    delete_file_url: str = "/v1/ai_engine/agi_platform/v2/datasets/document/delete"
    upload_file_url: str = "/v1/ai_engine/agi_platform/v2/datasets/files/upload"

    def __init__(self, dataset_id: str = "", dataset_name: str = ""):
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
        """
        创建知识库
        传参：
            dataset_name: 知识库名称
        返回:
            Dataset实例
        """
        payload = json.dumps({"name": dataset_name})
        http_client = HTTPClient()
        headers = http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = http_client.session.post(url=http_client.service_url(cls.create_url),
                                            headers=headers, data=payload)
        http_client.check_response_header(response)
        http_client.check_response_json(response.json())
        response = response.json()["result"]
        return Dataset(dataset_id=response["id"], dataset_name=response["name"])

    def add_files(self, file_path_list: List[str], is_custom_process_rule: bool = False,
                  custom_process_rule: Dict = None) -> AddFileResponse:
        """
        向知识库中添加文档
        传参：
        file_path_list: 文档路径列表
        is_custom_process_rule: 是否使用自定义文档处理规则, 默认为False, 使用平台的默认规则，为True时使用自定义规则
        custom_process_rule: 自定义文档规则，当is_custom_process_rule为True时生效，格式示例如下：
        {
        "separators": ["。", "，"],    # 文本切分符，支持这几种[ , , "？", , "!", "?", "……"]
        "target_length": 300,         # 文本切片片段长度，取值范围[300, 800]
        "overlap_rate": 0.3           # 文本片段重叠率，取值范围[0, 1]
        }
        返回：
        """
        file_ids = []
        for file_path in file_path_list:
            upload_res = self._upload_file(file_path)
            file_ids.append(upload_res["id"])
        payload = {"dataset_id": self.dataset_id, "file_ids": file_ids,
                   "is_custom_process_rule": is_custom_process_rule}
        if is_custom_process_rule and custom_process_rule:
            payload["custom_process_rule"] = custom_process_rule
        payload = json.dumps(payload)
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.add_file_url),
                                                 headers=headers, data=payload)
        self.http_client.check_response_header(response)
        self.http_client.check_response_json(response.json())
        res = AddFileResponse.model_validate(response.json()["result"])
        return res

    def _upload_file(self, file_path: str):
        """
        上传文档
        传参：
            file_path: 文档路径
        返回:
            上传文档的信息
        """
        headers = self.http_client.auth_header()
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = self.http_client.session.post(url=self.http_client.service_url(self.upload_file_url),
                                                     files=files, headers=headers)
            self.http_client.check_response_header(response)
            self.http_client.check_response_json(response.json())
            res = response.json()["result"]
        return res

    def delete_files(self, document_ids: List[str]):
        """
        删除知识库中的文档
        参数：
            document_ids: 文档id列表
        返回:
        """
        for document_id in document_ids:
            self._delete_file(document_id)

    def _delete_file(self, document_id):
        """
        删除知识库中的文档
        参数：
            document_id: 文档id
        返回:
        """
        payload = json.dumps({"dataset_id": self.dataset_id, "document_id": document_id})
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.delete_file_url),
                                                 headers=headers, data=payload)
        self.http_client.check_response_header(response)
        self.http_client.check_response_json(response.json())

    def get_file_list(self, page: int, limit: int, keyword: str = "") -> FileListResponse:
        """
        获取知识库中的文档列表
        参数：
            page: 第几页
            limit: 每页文档数
            keyword: 文件名关键字，支持模糊查询
        返回:
            返回示例：
            {
            "data": [
                {
                    "id": "d2d1bc1a-1763-4162-88b2-0dad225da16f", # 文档id
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
        self.http_client.check_response_json(response.json())
        res = FileListResponse.model_validate(response.json()["result"])
        return res
