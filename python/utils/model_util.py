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
from appbuilder.utils.trace.tracer_wrapper import list_trace

r"""模型名称到简称的映射.
"""
# Note(chengmo): 模型名称到简称的映射，是一个1:n的映射关系，之前的假设是模型与简称一一对应
# 实际上，模型名称和简称之间存在多对一的关系，因此这里不能仅使用一个字典来存储名称映射信息
model_name_mapping = [
    ("ERNIE-Bot 4.0", "eb-4"),
    ("ERNIE-Bot", "eb"),
    ("ERNIE-Bot-turbo", "eb-turbo"),
    ("EB-turbo-AppBuilder专用版", "eb-turbo-appbuilder"),
    ("EB-turbo-AppBuilder专用版", "ernie_speed_appbuilder"),
]

class RemoteModel(object):
    r"""远程模型类，用于封装远程模型的名称信息.
         参数:
            name(str):
                模型名称。
            short_name(str):
                模型简称, 可能存在多个
         """
    def __init__(self, remote_name: str):
        self.remote_name = remote_name
        self.short_names = []
    
    def register_short_name(self, short_name: str):
        r"""注册模型简称.
         参数:
            short_name(str):
                模型简称。
         """
        if short_name not in self.short_names:
            self.short_names.append(short_name)

    def get_remote_name_by_short_name(self, short_name: str) -> Optional[str]:
        r"""根据模型简称获取模型名称.
         参数:
            short_name(str):
                模型简称。
         """
        # TODO(chengmo): 使用logging 替换 print，解决print多次的问题
        if short_name == "eb-turbo-appbuilder":
            print("Deprecate warning: model [eb-turbo-appbuilder] is deprecated, please use [Qianfan-Agent-Speed-8K]")

        if short_name in self.short_names:
            return self.remote_name
        return None

class RemoteModelCollector():
    r"""远程模型收集器，用于收集远程模型信息. 是一个全局单例
    有两个核心功能：
    1、注册远程模型名和本地short_name
    2、根据short_name获取远程模型名
    """
    _instance = None
    _initialized = False

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.remote_models = {}

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def register_remote_model_name(self, remote_name: str, short_name: str):
        r"""注册远程模型名和本地short_name.
         参数:
            remote_name(str):
                远程模型名称。
            short_name(str):
                模型简称。
         """
        if remote_name not in self.remote_models:
            self.remote_models[remote_name] = RemoteModel(remote_name)
        
        self.remote_models[remote_name].register_short_name(short_name)
    
    def get_remote_name_by_short_name(self, short_name: str) -> Optional[str]:
        r"""根据short_name获取远程模型名.
         参数:
            short_name(str):
                模型简称。
         """
        for remote_model in self.remote_models.values():
            remote_name = remote_model.get_remote_name_by_short_name(short_name)
            if remote_name is not None:
                return remote_name
        
        return None


remote_model_collector = RemoteModelCollector()
for remote_name, short_name in model_name_mapping:
    remote_model_collector.register_remote_model_name(remote_name, short_name)

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

    @list_trace
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
        response = GetModelListResponse.from_json(payload=json.dumps(data),  ignore_unknown_fields=True)
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
