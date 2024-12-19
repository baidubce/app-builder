# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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

import requests
import json
import aiohttp
from aiohttp import ClientSession, hdrs
from appbuilder.utils.logger_util import logger
from appbuilder.utils.trace.tracer_wrapper import session_post


class InnerSession(requests.sessions.Session):

    def __init__(self, *args, **kwargs):
        """
        Initialize inner session.
        """
        super(InnerSession, self).__init__(*args, **kwargs)

    def build_curl(self, request: requests.PreparedRequest) -> str:
        """
        Generate cURL command from prepared request object.
        """
        curl = "curl -X {0} -L '{1}' \\\n".format(request.method, request.url)

        headers = [
            "-H '{0}: {1}' \\".format(k, v)
            for k, v in request.headers.items()
            if k != "Content-Length"
        ]

        if headers:
            headers[-1] = headers[-1].rstrip(" \\")
        curl += "\n".join(headers)
        if request.body:
            try:
                body = json.loads(request.body)
                body = "'{0}'".format(json.dumps(body, ensure_ascii=False))
                curl += " \\\n-d {0}".format(body)
            except:
                curl += " \\\n-d '{0}'".format(request.body)
        return curl

    def send(self, request, **kwargs):
        """
        Send request using inner session.
        """
        logger.debug("Curl Command:\n" + self.build_curl(request) + "\n")
        return super(InnerSession, self).send(request, **kwargs)

    @session_post
    def post(self, url, data=None, json=None, **kwargs):
        return super().post(url=url, data=data, json=json, **kwargs)

    @session_post
    def delete(self, url, **kwargs):
        return super().delete(url=url, **kwargs)

    @session_post
    def get(self, url, **kwargs):
        return super().get(url=url, **kwargs)

    @session_post
    def put(self, url, data=None, **kwargs):
        return super().put(url=url, data=data, **kwargs)


class AsyncInnerSession(ClientSession):

    def __init__(self, *args, **kwargs):
        """
        Initialize inner session.
        """
        super(AsyncInnerSession, self).__init__(*args, **kwargs)

    async def build_curl(self, method, url, data=None, json_data=None, **kwargs) -> str:
        """
        Generate cURL command from prepared request object.
        """
        curl = "curl -X {0} -L '{1}' \\\n".format(method, url)

        headers = kwargs.get("headers", {})
        headers_strs = [
            "-H '{0}: {1}' \\".format(k, v) for k, v in headers.items()]
        if headers_strs:
            headers_strs[-1] = headers_strs[-1].rstrip(" \\")
        curl += "\n".join(headers_strs)

        if data:
            try:
                body = "'{0}'".format(json.dumps(data, ensure_ascii=False))
                curl += " \\\n-d {0}".format(body)
            except:
                pass
        elif json_data:
            body = "'{0}'".format(json.dumps(json_data, ensure_ascii=False))
            curl += " \\\n-d {0}".format(body)

        return curl

    async def post(self, url, data=None, json=None, **kwargs):
        logger.debug("Curl Command:\n" + await self.build_curl(hdrs.METH_POST, url, data=data, json_data=json, **kwargs) + "\n")
        return await super().post(url=url, data=data, json=json, **kwargs)

    async def delete(self, url, **kwargs):
        logger.debug("Curl Command:\n" + await self.build_curl(hdrs.METH_DELETE, url, **kwargs) + "\n")
        return await super().delete(url=url, **kwargs)

    async def get(self, url, **kwargs):
        logger.debug("Curl Command:\n" + await self.build_curl(hdrs.METH_GET, url, **kwargs) + "\n")
        return await super().get(url=url, **kwargs)

    async def put(self, url, data=None, **kwargs):
        logger.debug("Curl Command:\n" + await self.build_curl(hdrs.METH_PUT, url, data=data, **kwargs) + "\n")
        return await super().put(url=url, data=data, **kwargs)
