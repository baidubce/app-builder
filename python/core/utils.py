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
import time
import itertools
from typing import List
from urllib.parse import urlparse, unquote
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import TypeNotSupportedException, ModelNotSupportedException
from appbuilder.utils.model_util import GetModelListRequest, Models, RemoteModelCollector
from functools import lru_cache


def utils_get_user_agent():
    return 'appbuilder-sdk-python/{}'.format("__version__")

# Todo(chengmo): 此处返回的模型名称为原始名称，并非推荐使用的short name
# 应当返回一个详细的列表，告知用户原始名 + 对应的short名
# 同时考虑是否返回每个模型可用的余额
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
    api_type_set = {"chat", "completions", "embeddings", "text2image"}
    if api_type_filter and not set(api_type_filter).issubset(api_type_set):
        raise TypeNotSupportedException(
            f"mismatched argument api_type_filter, expected in {api_type_set}"
        )
    request = GetModelListRequest()
    request.apiTypefilter = api_type_filter
    model = Models(secret_key=secret_key)
    response = model.list(request)
    models = []

    for model in itertools.chain(response.result.common, response.result.custom):
        if is_available and (model.chargeStatus not in ["OPENED", "FREE"] or
                             not any(version.serviceStatus == "Done" for version in model.versionList)):
            continue
        models.append(model.name)
    return models

def get_filename_from_url(url):
    """从给定URL中提取文件名"""
    parsed_url = urlparse(url)
    # 提取路径部分
    path = parsed_url.path
    # 从路径中获取文件名
    filename = path.split('/')[-1]
    # 解码URL编码的文件名
    return unquote(filename)

def convert_cloudhub_url(client: HTTPClient, qianfan_url: str) -> str:
    """将千帆url转换为AppBuilder url"""
    qianfan_url_prefix = "rpc/2.0/ai_custom/v1/wenxinworkshop"
    cloudhub_url_prefix = "rpc/2.0/cloud_hub/v1/bce/wenxinworkshop/ai_custom/v1"
    index = str.find(qianfan_url, qianfan_url_prefix)
    if index == -1:
        raise ValueError(f"url format error, {qianfan_url} is not a valid qianfan url")
    url_suffix = qianfan_url[index + len(qianfan_url_prefix):]
    return "{}/{}{}".format(client.gateway, cloudhub_url_prefix, url_suffix)


def is_url(string):
    """
    判断字符串是否是URL
    :param string:
    :return:
    """
    result = urlparse(string)
    return all([result.scheme, result.netloc])


def ttl_lru_cache(seconds_to_live: int, maxsize: int = 128):
    """
    Time aware lru caching
    """
    def wrapper(func):
        @lru_cache(maxsize)
        def inner(__ttl, *args, **kwargs):
            # Note that __ttl is not passed down to func,
            # as it's only used to trigger cache miss after some time
            return func(*args, **kwargs)
        return lambda *args, **kwargs: inner(time.time() // seconds_to_live, *args, **kwargs)
    return wrapper


class ModelInfo:
    """ 模型信息类 """

    def __init__(self, client: HTTPClient):
        """根据模型名称获取并初始化模型信息"""
        self.client = client
        response = Models(client).list()
        self.model_list = [*response.result.common, *response.result.custom]

    def get_model_url(self, model_name: str) -> str:
        """获取模型在工作台网关的请求url"""
        short_name = model_name
        remote_model_name_collector = RemoteModelCollector()
        origin_name = remote_model_name_collector.get_remote_name_by_short_name(short_name)
        if not origin_name:
            origin_name = short_name
        for model in self.model_list:
            if model.name == origin_name:
                return convert_cloudhub_url(self.client, model.url)
        raise ModelNotSupportedException(f"Model[{model_name}] not available! "
                                         f"You can query available models through: appbuilder.get_model_list()")

    def get_model_type(self, model_name: str) -> str:
        """获取模型类型"""
        short_name = model_name
        remote_model_name_collector = RemoteModelCollector()
        origin_name = remote_model_name_collector.get_remote_name_by_short_name(short_name)
        if not origin_name:
            origin_name = short_name
        for model in self.model_list:
            if model.name == origin_name:
                return model.apiType
        raise ModelNotSupportedException(f"Model[{model_name}] not available! "
                                         f"You can query available models through: appbuilder.get_model_list()")
