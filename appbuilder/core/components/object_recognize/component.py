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

"""object recognize component."""

import base64
import json


from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.core._exception import AppBuilderServerException
from appbuilder.core.components.object_recognize.model import *


class ObjectRecognition(Component):
    r"""
       提供通用物体及场景识别能力，即对于输入的一张图片（可正常解码，且长宽比适宜），输出图片中的多
       个物体及场景标签。

       Examples:

       ... code-block:: python

           import appbuilder
           object_recognition = appbuilder.ObjectRecognition()
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           with open("./object_recognition_test.jepg", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """

    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 通用物体识别

                    参数:
                       message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                       或 Message(content={"url": "https://image/download/url"}).
                       timeout (float, 可选): HTTP超时时间
                       retry (int, 可选)： HTTP重试次数

                     返回: message (obj: `Message`): 模型识别结果. 举例: Message(content={"result":[{"keyword":"苹果",
                     "score":0.94553,"root":"植物-蔷薇科"},{"keyword":"姬娜果","score":0.730442,"root":"植物-其它"},
                     {"keyword":"红富士","score":0.505194,"root":"植物-其它"}]})
        """
        inp = ObjectRecognitionInMsg(**message.content)
        req = ObjectRecognitionRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = ObjectRecognitionOutMsg(**result_dict)
        return Message(content=out.dict())

    def _recognize(self, request: ObjectRecognitionRequest, timeout: float = None,
                  retry: int = 0) -> ObjectRecognitionResponse:
        r"""调用底层接口进行通用物体与场景识别
                   参数:
                       request (obj: `ObjectRecognitionRequest`) : 通用物体与场景识别输入参数
                   返回：
                       response (obj: `ObjectRecognitionResponse`): 通用物体与场景识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")

        data = ObjectRecognitionRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v2/advanced_general")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id,data)
        object_response = ObjectRecognitionResponse.from_json(payload=json.dumps(data))
        object_response.request_id = request_id
        return object_response

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request (dict) : 通用物体与场景识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )
