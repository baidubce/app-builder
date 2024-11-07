# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
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

"""table ocr component."""

import base64
import json

from appbuilder.core import utils
from appbuilder.core.component import Component
from appbuilder.core.components.table_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException, InvalidRequestArgumentError
from appbuilder.utils.trace.tracer_wrapper import components_run_trace, components_run_stream_trace


class TableOCR(Component):
    r"""
       支持识别图片中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、
       无线表格、含合并单元格表格。同时，支持多表格内容识别。

       Examples:

       .. code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           table_ocr = appbuilder.TableOCR()
           with open("./table_ocr_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """

    name = "table_ocr"
    version = "v1"
    manifests = [
        {
            "name": "table_ocr",
            "description": "需要识别图片中的表格内容，使用该工具, 但不支持html后缀文件的识别",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "待识别图片的文件名"
                    }
                },
                "required": ["file_names"]
            }
        }
    ]

    @HTTPClient.check_param
    @components_run_trace
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        """
        表格文字识别
        
        Args:
            message (Message): 输入图片或图片url下载地址用于执行识别操作。
                举例: Message(content={"raw_image": b"..."})
                或 Message(content={"url": "https://image/download/url"})。
            timeout (float, 可选): HTTP超时时间。
            retry (int, 可选): HTTP重试次数。
        
        Returns:
            message (Message): 识别结果。
                举例: Message(name=msg, content={'tables_result': [{
                'table_location': [{'x': 15, 'y': 15}, {'x': 371, 'y': 15}, {'x': 371, 'y': 98}, {'x': 15,
                'y': 98}], 'header': [], 'body': [{'cell_location': [{'x': 15, 'y': 15}, {'x': 120, 'y': 15},
                {'x': 120, 'y': 58}, {'x': 15, 'y': 58}], 'row_start': 0, 'row_end': 1, 'col_start': 0,
                'col_end': 1, 'words': '参数'}, {'cell_location': [{'x': 120, 'y': 15}, {'x': 371, 'y': 15},
                {'x': 371, 'y': 58}, {'x': 120, 'y': 58}], 'row_start': 0, 'row_end': 1, 'col_start': 1,
                'col_end': 2, 'words': '值'}, {'cell_location': [{'x': 15, 'y': 58}, {'x': 120, 'y': 58},
                {'x': 120, 'y': 98}, {'x': 15, 'y': 98}], 'row_start': 1, 'row_end': 2, 'col_start': 0,
                'col_end': 1, 'words': 'Content-Type'}, {'cell_location': [{'x': 120, 'y': 58}, {'x': 371,
                'y': 58}, {'x': 371, 'y': 98}, {'x': 120, 'y': 98}], 'row_start': 1, 'row_end': 2, 'col_start':
                1, 'col_end': 2, 'words': 'application/x-www-form-urlencoded'}], 'footer': []}]}, mtype=dict)
        
        """
        inp = TableOCRInMsg(**message.content)
        req = TableOCRRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        req.cell_contents = "false"
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = TableOCROutMsg(**result_dict)
        return Message(content=out.model_dump())

    def _recognize(self, request: TableOCRRequest, timeout: float = None,
                   retry: int = 0, request_id: str = None) -> TableOCRResponse:
        r"""调用底层接口进行表格文字识别
                   参数:
                       request (obj: `TableOCRRequest`) : 表格文字识别输入参数
                   返回：
                       response (obj: `TableOCRResponse`): 表格文字识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError(
                "request format error, one of image or url must be set")

        data = TableOCRRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header(request_id)
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/table")
        response = self.http_client.session.post(
            url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        res = TableOCRResponse.from_json(json.dumps(data))
        res.request_id = request_id
        return res

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 表格文字识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )

    def get_table_markdown(self, tables_result):
        """
        将表格识别结果转换为Markdown格式。
        
        Args:
            tables_result (list): 表格识别结果列表，每个元素是一个包含表格数据的字典，其中包含表格体（body）等字段。
        
        Returns:
            list: 包含Markdown格式表格的字符串列表。
        
        """
        markdowns = []
        for table in tables_result:
            cells = table["body"]
            max_row = max(cell['row_end'] for cell in cells)
            max_col = max(cell['col_end'] for cell in cells)
            # 初始化表格数组
            table_arr = [[''] * max_col for _ in range(max_row)]
            # 填充表格数据
            for cell in cells:
                row = cell['row_start']
                col = cell['col_start']
                table_arr[row][col] = cell['words']

            markdown_table = ""
            for row in table_arr:
                markdown_table += "| " + " | ".join(row) + " |\n"
            # 生成分隔行
            separator = "| " + " | ".join(['---'] * max_col) + " |\n"
            # 插入分隔行在表头下方
            header, body = markdown_table.split('\n', 1)
            markdown_table = header + '\n' + separator + body
            markdowns.append(markdown_table)
        return markdowns

    @components_run_stream_trace
    def tool_eval(self, name: str, streaming: bool, **kwargs):
        """
        对传入文件进行处理，并返回处理结果。
        
        Args:
            name (str): 工具的名称。
            streaming (bool): 是否为流式处理。若为True，则以生成器形式返回结果；若为False，则直接返回结果。
            **kwargs: 关键字参数，包含以下参数：
                traceid (str): 请求的唯一标识符。
                file_names (List[str]): 文件名列表，表示需要处理的文件名。
                files (List[str]): 同file_names，用于兼容老版本接口。
                file_urls (Dict[str, str]): 文件名和对应URL的映射字典。
        
        Returns:
            若streaming为True，则以生成器形式返回处理结果，每个元素为包含type和text的字典，type固定为"text"，text为处理结果的JSON字符串。
            若streaming为False，则直接返回处理结果的JSON字符串。
        
        Raises:
            InvalidRequestArgumentError: 若传入文件名在file_urls中未找到对应的URL，则抛出此异常。
        
        """
        result = {}
        traceid = kwargs.get("traceid")
        file_names = kwargs.get("file_names", None)
        if not file_names:
            file_names = kwargs.get("files")
        file_urls = kwargs.get("file_urls", {})
        for file_name in file_names:
            if utils.is_url(file_name):
                file_url = file_name
            else:
                file_url = file_urls.get(file_name, None)
            if file_url is None:
                raise InvalidRequestArgumentError(
                    f"request format error, file {file_name} url does not exist"
                )
            req = TableOCRRequest()
            req.url = file_url
            req.cell_contents = "false"
            resp = self._recognize(req, request_id=traceid)
            tables_result = proto.Message.to_dict(resp)["tables_result"]
            markdowns = self.get_table_markdown(tables_result)
            result[file_name] = markdowns

        result = json.dumps(result, ensure_ascii=False)
        if streaming:
            yield {
                "type": "text",
                "text": result,
                "visible_scope": 'llm',
            }
            yield {
                "type": "text",
                "text": "",
                "visible_scope": "user",
            }
        else:
            return result
