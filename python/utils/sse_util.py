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
"""
SSE Client util
"""
from appbuilder.utils.logger_util import logger
import logging
import aiohttp


class SSEClient:
    """
    一个简易的SSE Client，用于接收服务端发送的SSE事件。
    """

    def __init__(self, event_source, char_enc="utf-8"):
        """
        通过现有的事件源初始化 SSE 客户端。
        事件源应为二进制流，并具有 close() 方法。
        这通常是实现 io.BinaryIOBase 的东西，比如 httplib 或 urllib3HTTPResponse 对象。
        """
        logger.debug(f"Initialized SSE client from event source {event_source}")
        self._event_source = event_source
        self._char_enc = char_enc

    def _read(self):
        """
        读取传入的事件源流并生成事件块。
        不幸的是，有些服务器可能会决定在响应中将事件分解为多个HTTP块。
        因此，有必要正确地将连续的响应块缝合在一起，并找到SSE分隔符（空的新行），以生成完整、正确的事件块。
        """
        data = b""
        for chunk in self._event_source:
            for line in chunk.splitlines(True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    def events(self):
        """
        从给定的输入流中读取 Server-Side-Event (SSE) 数据，并生成解析后的 Event 对象。

        Args:
            无

        Returns:
            generator: 解析后的 Event 对象的生成器。
        """
        for chunk in self._read():
            event = Event()
            # Split before decoding so splitlines() only uses \r and \n
            for line in chunk.splitlines():
                # Decode the line.
                line = line.decode(self._char_enc)
                # Lines starting with a separator are comments and are to be
                # ignored.
                if not line.strip() or line.startswith(":"):
                    continue
                logger.debug(f"raw line: {line}")
                data = line.split(":", 1)
                field = data[0]
                # Ignore unknown fields.
                if field not in event.__dict__:
                    event.raw += line
                    logger.debug(
                        f"Saw invalid field {field} while parsing Server Side Event"
                    )
                    continue

                if len(data) > 1:
                    # From the spec:
                    # "If value starts with a single U+0020 SPACE character,
                    # remove it from value."
                    if data[1].startswith(" "):
                        value = data[1][1:]
                    else:
                        value = data[1]
                else:
                    # If no value is present after the separator,
                    # assume an empty value.
                    value = ""
                # The data field may come over multiple lines and their values
                # are concatenated with each other.
                if field == "data":
                    event.__dict__[field] += value + "\n"
                    event.raw += value + "\n"
                else:
                    event.__dict__[field] = value
                    event.raw += value

            # Events with no data are not dispatched.
            if not event.data:
                if event.raw:
                    # unknown error
                    pass
                else:
                    continue
            else:
                # If the data field ends with a newline, remove it.
                if event.data.endswith("\n"):
                    event.data = event.data[0:-1]
            # Empty event names default to 'message'
            event.event = event.event or "message"
            # Dispatch the event
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(f"Dispatching {event.debug_str}...")
            else:
                logger.debug(f"Dispatching {event}...")
            yield event

    def close(self):
        """
        手动关闭事件源流。
        """
        self._event_source.close()


class AsyncSSEClient:
    """
    一个简易的SSE Client，用于接收服务端发送的SSE事件。
    """
    def __init__(self, response, char_enc='utf-8'):
        """
        通过现有的事件源response初始化 SSE 客户端。
        response应为aiohttp.ClientResponse实例
        """
        self._response = response
        self._char_enc = char_enc

    async def _read(self):
        """
        读取传入的事件源流并生成事件块。
        """
        data = b''
        async for chunk in self._response.content.iter_any():
            for line in chunk.splitlines(True):
                data += line
                if data.endswith((b'\r\r', b'\n\n', b'\r\n\r\n')):
                    yield data
                    data = b''
        if data:
            yield data

    async def events(self):
        """
        从给定的输入流中读取 Server-Side-Event (SSE) 数据，并生成解析后的 Event 对象。
        Returns:
            generator: 解析后的 Event 对象的生成器。
        """
        async for chunk in self._read():
            event = Event()
            # Split before decoding so splitlines() only uses \r and \n
            for line in chunk.splitlines():
                # Decode the line.
                line = line.decode(self._char_enc)
                # Lines starting with a separator are comments and are to be ignored.
                if not line.strip() or line.startswith(':'):
                    continue

                data = line.split(':', 1)
                field = data[0]
                # Ignore unknown fields.
                if field not in event.__dict__:
                    event.raw += line
                    continue

                if len(data) > 1:
                    # From the spec:
                    # "If value starts with a single U+0020 SPACE character,
                    # remove it from value."
                    if data[1].startswith(' '):
                        value = data[1][1:]
                    else:
                        value = data[1]
                else:
                    # If no value is present after the separator,
                    # assume an empty value.
                    value = ''

                # The data field may come over multiple lines and their values are concatenated with each other.
                if field == 'data':
                    event.__dict__[field] += value + '\n'
                    event.raw += value + '\n'
                else:
                    event.__dict__[field] = value
                    event.raw += value

            # Events with no data are not dispatched.
            if not event.data:
                continue

            # If the data field ends with a newline, remove it.
            if event.data.endswith('\n'):
                event.data = event.data[0:-1]

            # Empty event names default to 'message'
            event.event = event.event or 'message'
            
            yield event


class Event(object):
    """
    事件流中的事件。
    """

    def __init__(self, id=None, event="message", data="", retry=None):
        self.id = id
        self.event = event
        self.data = data
        self.retry = retry
        self.raw = ""

    def __str__(self):
        s = f"{self.event} event"
        if self.id:
            s += f" #{self.id}"
        if self.data:
            s += f", {len(self.data)} byte"
        else:
            s += ", no data"
        if self.retry:
            s += f", retry in {self.retry} ms"
        return s

    @property
    def debug_str(self):
        s = f"{self.event} event"
        if self.id:
            s += f" #{self.id}"
        if self.data:
            s += f", {len(self.data)} byte, DATA<<{self.data}>>"
        else:
            s += ", no data"
        if self.raw:
            s += f", RAW<<{self.raw}>>"
        else:
            s += ", no raw"
        if self.retry:
            s += f", retry in {self.retry} ms"
        return s
