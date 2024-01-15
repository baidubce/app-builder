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
import itertools
from typing import List

from appbuilder.core._client import HTTPClient
from appbuilder.utils.model_util import GetModelListRequest, Models, model_name_mapping


def utils_get_user_agent():
    return 'appbuilder-sdk-python/{}'.format("__version__")


def get_model_list(secret_key: str = "", api_type_filter: List[str] = [], is_available: bool = False) -> list:
    """
    返回用户的模型列表。

    参数:
        secret_key(str,可选): 用户鉴权token, 默认从环境变量中获取: os.getenv("APPBUILDER_TOKEN", "")。
        api_type_filter(List[str], 可选): 根据apiType过滤，["chat", "completions", "embeddings", "text2image"]，不填包括所有的。
        is_available(bool, 可选): 是否返回可用模型列表, 默认返回所有模型。

    返回:
        list: 模型列表。
    """
    request = GetModelListRequest()
    request.apiTypefilter = api_type_filter
    model = Models(secret_key=secret_key)
    response = model.list(request)
    models = []

    for model in itertools.chain(response.result.common, response.result.custom):
        if is_available and model.chargeStatus not in ["OPENED", "FREE"]:
            continue
        models.append(model.name)
    return models


def convert_cloudhub_url(client, qianfan_url: str) -> str:
    """将千帆url转换为AppBuilder url"""
    qianfan_url_prefix = "rpc/2.0/ai_custom/v1/wenxinworkshop"
    cloudhub_url_prefix = "rpc/2.0/cloud_hub/v1/bce/wenxinworkshop/ai_custom/v1"
    index = str.find(qianfan_url, qianfan_url_prefix)
    if index == -1:
        raise ValueError(f"{qianfan_url} is not a valid qianfan url")
    url_suffix = qianfan_url[index + len(qianfan_url_prefix):]
    return "{}/{}{}".format(client.gateway, cloudhub_url_prefix, url_suffix)


class ModelUtils:
    """ 模型工具类 """

    def __init__(self, client, model_name):
        """根据模型名称获取并初始化模型信息"""
        self.model_info = None
        self.client = client
        self.model_name = model_name
        for key, value in model_name_mapping.items():
            if self.model_name == value:
                self.model_name = key
                break
        response = Models(client).list()
        for model in itertools.chain(response.result.common, response.result.custom):
            if model.name == self.model_name:
                self.model_info = model
                break
        if not self.model_info:
            raise ValueError(f"Model[{model_name}] not available! "
                             f"You can query available models through: appbuilder.get_model_list()")

    def get_model_url(self) -> str:
        """获取模型在工作台网关的请求url"""
        return convert_cloudhub_url(self.client, self.model_info.url)

    def get_model_type(self) -> str:
        """获取模型类型"""
        return self.model_info.apiType