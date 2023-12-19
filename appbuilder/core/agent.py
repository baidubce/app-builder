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
import sys
import os 
import logging
import uuid
import json
import inspect
from pydantic import BaseModel, root_validator, Extra
from typing import Optional, Dict, List, Any

import appbuilder
from appbuilder.core.context import UserSession
from appbuilder.core.component import Component
from appbuilder.core.message import Message


class AgentBase(BaseModel):
    """
    AgentBase 是对组件调用的服务化封装，开发者不是必须要用 AgentBase 才能运行自己的组件服务。
    但 AgentBase 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。
    此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。
  
    Examples:

        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="ernie-bot-4"
            )
            agent = appbuilder.AgentBase(component=component)
            message = appbuilder.Message({"query": "你好"})
            session_id = agent._generate_session_id()
            print(agent.chat(message, session_id))
            
        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="ernie-bot-4"
            )
            agent = appbuilder.AgentBase(component=component)
            agent.serve(debug=False, port=8091)
            
        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="ernie-bot-4"
            )
            agent = appbuilder.AgentBase(component=component)
            agent.chainlit_demo(port=8091)
    """
    component: Component
    user_session_handle: UserSession

    class Config:
        """
        检查配置
        """
        extra = Extra.forbid # 不能传入类定义中未声明的字段
        arbitrary_types_allowed = True # 此设置允许在模型中使用自定义类型的字段

    @root_validator(pre=True)
    def init(cls, values: Dict) -> Dict:
        """
        初始化 AgentBase
        
        Args:
            component (Component): 可运行的 Component
            user_session_config (str|None): Session 配置字符串，遵循 sqlalchemy 后端定义，参考文档
              https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
        
        Returns:
            None
        """
        user_session_config = values.get("user_session_config")
        if "user_session_config" in values:
            values.pop("user_session_config")
        values.update({
            "component": values.get("component"),
            "user_session_handle": UserSession(user_session_config),
        })
        return values

    def _generate_session_id(self):
        """
        生成 Session ID
        
        Args:
            None
        
        Returns:
            str
        """
        return str(uuid.uuid4())
        
    def _get_user_session(self, session_id: str, limit: int) -> List[Message]:
        """
        获取历史对话数据
        
        Args:
            session_id (str): Session ID
            limit (int): 获取最近的几条 session 数据
        
        Returns:
            List[Message]
        """
        return self.user_session_handle.get_session_messages(session_id, limit)

    def _save_user_session(
        self, 
        session_id: str, 
        query_message: Message, 
        answer_message: Message,
        extra: Dict = {},
    ) -> None:
        """
        保存一条对话数据
        
        Args:
            session_id (str): Session ID
            query_message (Message): 该次对话用户输入的 Message
            answer_message (Message): 该次对话模型输出的 Message
            extra (dict): 该次对话额外需要存储的数据
        
        Returns:
            None
        """
        self.user_session_handle.save_session_message(
            session_id, query_message, answer_message, extra)

    def chat(self, message: Message, session_id: str, stream: bool=False, **args) -> Message:
        """
        执行一次对话。对话历史会被存储到 session_id 对应的 Session 中
        
        Args:
            message (Message): 该次对话用户输入的 Message
            session_id (str): Session ID
            stream (bool): 是否流式请求
            **args: 其他参数，会被透传到 component
        
        Returns:
            Message
        """
        # user session is a list of Messages
        user_session = self._get_user_session(session_id, limit=10)
        params = inspect.signature(self.component.run).parameters
        # online chat interface
        if "user_session" in params:
            answer = self.component.run(message=message, user_session=user_session, stream=stream, **args)
        else:
            answer = self.component.run(message=message, stream=stream, **args)
        if stream:
            def iterator(iters):
                concat_answer = ""
                for it in iters:
                    concat_answer += it
                    yield it
                self._save_user_session(session_id, message, Message(concat_answer))
            return Message(iterator(answer.content))
        else:
            self._save_user_session(session_id, message, answer)
            return answer
        
    def serve(self, host='0.0.0.0', debug=True, port=8092):
        """
        将 component 服务化，提供 Flask http API 接口
        
        Args:
            host (str): 服务 host
            debug (bool): 是否是 debug 模式
            port (int): 服务 port
        
        Returns:
            None
        """
        # serve agent chat interface
        from flask import Flask, current_app, request, Response
        from flask_restful import reqparse, Resource
        from werkzeug.exceptions import BadRequest

        app = Flask(__name__)

        @app.errorhandler(BadRequest)
        def handle_bad_request(e):
            return {"code": 400, "message": 'Bad request, Please check your data.', "result": None}, 400
            
        @app.errorhandler(RuntimeError)
        def handle_bad_request(e):
            return {"code": 1000, "message": f'RuntimeError: {e}', "result": None}, 200

        @app.route('/chat', methods=['POST'])
        def warp():
            data = request.get_json()
            if "message" not in data:
                raise BadRequest("message is required")
            message = Message(data.pop('message'))
            if "session_id" not in data:
                session_id = self._generate_session_id()
            else:
                session_id = data.pop("session_id")
                if not isinstance(session_id, str):
                    raise BadRequest("session_id must be str type")
            if "stream" not in data:
                stream = False
            else:
                stream = data.pop("stream")
                if not isinstance(stream, bool):
                    raise BadRequest("stream must be bool type")

            try:
                answer = self.chat(message, session_id, stream, **data)
                if stream:
                    def gen_sse_resp(stream_message):
                        with app.app_context():
                            for it in stream_message.content:
                                d = {
                                    "code": 0, "message": "",
                                    "result": {
                                        "session_id": session_id, 
                                        "answer_message": json.loads(Message(it).json(exclude_none=True)),
                                    }
                                }
                                yield "data: " + json.dumps(d, ensure_ascii=False) + "\n\n"
                    return Response(
                        gen_sse_resp(answer), 200, 
                        {'Content-Type': 'text/event-stream; charset=utf-8'},
                    )
                else:
                    return {
                        "code": 0, "message": "",
                        "result": {
                            "session_id": session_id,
                            "answer_message": json.loads(answer.json(exclude_none=True)),
                        }
                    }
            except Exception as e:
                logging.error(e, exc_info=True)
                raise RuntimeError(e)
            
        app.run(host=host, debug=debug, port=port)
        
    def chainlit_demo(self, host='0.0.0.0', port=8091):
        """
        将 component 服务化，提供 chainlit demo 页面
        
        Args:
            host (str): 服务 host
            port (int): 服务 port
        
        Returns:
            None
        """
        import chainlit as cl
        import chainlit.cli
        import click
        from click.testing import CliRunner
        
        @cl.on_message  # this function will be called every time a user inputs a message in the UI
        async def main(message: cl.Message):
            session_id = cl.user_session.get("id")
            msg = cl.Message(content="")
            await msg.send()
            stream_message = self.chat(Message(message.content), session_id=session_id, stream=True)

            for part in stream_message.content:
                if token := part or "":
                    await msg.stream_token(token)
            await msg.update()

        # start chainlit service
        if os.getenv('APPBUILDER_RUN_CHAINLIT') == '1':
            pass
        else:
            os.environ['APPBUILDER_RUN_CHAINLIT'] = '1'
            target = sys.argv[0]
            runner = CliRunner()
            runner.invoke(
                chainlit.cli.chainlit_run, [target, '--watch', "--port", port, "--host", host])
