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

from appbuilder.core.component import Component
from appbuilder.core.components.table_ocr.model import *
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException


class TableOCR(Component):
    r"""
       支持识别图片/PDF格式文档中的表格内容，返回各表格的表头表尾内容、单元格文字内容及其行列位置信息，全面覆盖各类表格样式，包括常规有线表格、
       无线表格、含合并单元格表格。同时，支持多表格内容识别。

       Examples:

       ... code-block:: python

           import appbuilder
           table_ocr = appbuilder.TableOCR()
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           with open("./table_ocr_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """

    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 表格文字识别

                    参数:
                       message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                       或 Message(content={"url": "https://image/download/url"}).
                       timeout (float, 可选): HTTP超时时间
                       retry (int, 可选)： HTTP重试次数

                     返回: message (obj: `Message`): 识别结果. 举例: Message(name=msg, content={'tables_result': [{
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
                   retry: int = 0) -> TableOCRResponse:
        r"""调用底层接口进行表格文字识别
                   参数:
                       request (obj: `TableOCRRequest`) : 表格文字识别输入参数
                   返回：
                       response (obj: `TableOCRResponse`): 表格文字识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")

        data = TableOCRRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/ocr/v1/table")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
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
