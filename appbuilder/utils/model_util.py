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

import json
import proto
from typing import Optional, MutableSequence

import appbuilder
from appbuilder.core._client import HTTPClient

r"""模型名称到简称的映射.
"""
model_name_mapping = {
    "ERNIE-Bot 4.0": "eb-4",
    "ERNIE-Bot-8K": "eb-8k",
    "ERNIE-Bot": "eb",
    "ERNIE-Bot-turbo": "eb-turbo",
    "EB-turbo-AppBuilder专用版": "eb-turbo-appbuilder",
}


class GetModelListRequest(proto.Message):
    r"""获取模型列表请求体
         参数:
            apiTypefilter(str):
                根据apiType过滤，["chat", "completions", "embeddings", "text2image"]，不填包括所有的。
         """
    apiTypefilter: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1
    )


class GetModelListResponse(proto.Message):
    r"""获取模型列表返回体
         参数:
            request_id(str):
                网关层的请求ID.
            log_id(str):
                请求ID。
            success(bool):
                是否成功的返回。
            error_code(int):
                错误码。
            error_msg(str):
                错误信息。
            result(ModelListResult):
                模型列表。
         """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    log_id: str = proto.Field(
        proto.STRING,
        number=2,
    )

    success: bool = proto.Field(
        proto.BOOL,
        number=3,
    )

    error_code: int = proto.Field(
        proto.INT32,
        number=4,
    )

    error_msg: str = proto.Field(
        proto.STRING,
        number=5,
    )
    result: "ModelListResult" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="ModelListResult",
    )


class ModelListResult(proto.Message):
    r"""模型列表
         参数:
            common(ModelData):
                预置服务模型信息。
            custom(ModelData):
                自定义服务模型信息。
         """
    common: MutableSequence["ModelData"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ModelData",
    )

    custom: MutableSequence["ModelData"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="ModelData",
    )


class ModelData(proto.Message):
    r"""模型基本信息
         参数:
            name(str):
                服务名称。
            url(int):
                服务endpoint。
            apiType(str):
                服务类型：chat、completions、embeddings、text2image。
            chargeStatus(int):
                付费状态。
            versionList(int):
                服务版本列表。
         """
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )

    url: str = proto.Field(
        proto.STRING,
        number=2,
    )

    apiType: str = proto.Field(
        proto.STRING,
        number=3,
    )
    chargeStatus: str = proto.Field(
        proto.STRING,
        number=4,
    )

    versionList: MutableSequence["Version"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Version",
    )


class Version(proto.Message):
    r"""服务版本
         参数:
            id(str):
                服务版本id，仅自定义服务有该字段。
            aiModelId(str):
                发布该服务版本的模型id，仅自定义服务有该字段。
            aiModelVersionId(str):
                发布该服务版本的模型版本id，仅自定义服务有该字段。
            trainType(str):
                服务基础模型类型。
            serviceStatus(str):
                服务状态。
         """
    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    aiModelId: str = proto.Field(
        proto.STRING,
        number=2,
    )
    aiModelVersionId: str = proto.Field(
        proto.STRING,
        number=3,
    )
    trainType: str = proto.Field(
        proto.STRING,
        number=4,
    )
    serviceStatus: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Models:
    r"""
    模型工具类，提供模型列表接口。
     """

    def __init__(self,
                 client: HTTPClient = None,
                 secret_key: Optional[str] = None,
                 gateway: str = ""
                 ):
        r"""Models初始化方法.

            参数:
                client(obj:`HTTPClient`): 客户端实例，用于发送请求。
                secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "").
                gateway(str, 可选): 后端网关服务地址，默认从环境变量中获取: os.getenv("GATEWAY_URL", "")
            返回：
                无
        """
        self.http_client = client or HTTPClient(secret_key, gateway)

    def list(self, request: GetModelListRequest = None, timeout: float = None,
             retry: int = 0) -> GetModelListResponse:
        """
        返回用户的模型列表信息。

        参数:
            request (obj:`GetModelListRequest`):模型列表查询请求体。
            timeout (float, 可选): 请求的超时时间。
            retry (int, 可选): 请求的重试次数。

        返回:
            obj:`GetModelListResponse`: 模型列表返回体。
        """
        url = self.http_client.service_url("/v1/bce/wenxinworkshop/service/list")
        if request is None:
            request = GetModelListRequest()
        data = GetModelListRequest.to_json(request)
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/json'
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(url, data=data, headers=headers, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        response = GetModelListResponse.from_json(payload=json.dumps(data))
        response.request_id = request_id
        return response

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""服务response参数检查

            参数:
                data (dict) : body返回
            返回：
                无
        """
        if "error_code" in data and "error_msg" in data:
            if data["error_code"] != 0:
                raise appbuilder.AppBuilderServerException(
                    request_id=request_id,
                    service_err_code=data["error_code"],
                    service_err_message=data["error_msg"])


def map_model_name(model_name: str) -> str:
    r"""模型名称映射函数

        参数:
            model_name (str) : 模型名称
        返回：
            str: 映射后的模型名称
    """
    return model_name_mapping.get(model_name, model_name)
