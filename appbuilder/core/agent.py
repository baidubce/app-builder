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
import copy
import os 
import logging
import uuid
import json
import inspect
from pydantic import BaseModel, model_validator, Extra
from typing import Optional, Dict, List, Any, Union
import sqlalchemy

import appbuilder
from appbuilder.core.context import init_context
from appbuilder.core.user_session import UserSession
from appbuilder.core.component import Component
from appbuilder.core.message import Message


class AgentRuntime(BaseModel):
    """
    AgentRuntime 是对组件调用的服务化封装，开发者不是必须要用 AgentRuntime 才能运行自己的组件服务。
    但 AgentRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。
    此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。
  
    AgentRuntime 接受两个参数:
        component (Component): 可运行的 Component, 需要实现 run(message, stream, **args) 方法  
        user_session_config (sqlalchemy.engine.URL|str|None): Session 输出存储配置字符串。默认使用 sqlite:///user_session.db
            遵循 sqlalchemy 后端定义，参考文档：https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls

    Examples:

        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="eb-4"
            )
            agent = appbuilder.AgentRuntime(component=component)
            message = appbuilder.Message({"query": "你好"})
            print(agent.chat(message, stream=False))
            
        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="eb-4"
            )
            user_session_config = "sqlite:///foo.db"
            agent = appbuilder.AgentRuntime(
                component=component, user_session_config=user_session_config)
            agent.serve(debug=False, port=8091)
            
        .. code-block:: python

            import os
            import sys
            import appbuilder
            os.environ["APPBUILDER_TOKEN"] = '...'

            component = appbuilder.Playground(
                prompt_template="{query}",
                model="eb-4"
            )
            agent = appbuilder.AgentRuntime(component=component)
            agent.chainlit_demo(port=8091)


    ** Session 数据管理 **: 除去上述简单应用外，还支持 Session 数据管理，下面是一个例子

    Examples:

        .. code-block:: python
            import os
            import sys
            from appbuilder.core.component import Component
            from appbuilder import (
                AgentRuntime, UserSession, Message, QueryRewrite, Playground,
            )

            os.environ["APPBUILDER_TOKEN"] = '...'

            class PlaygroundWithHistory(Component):
                def __init__(self):
                    super().__init__()
                    self.query_rewrite = QueryRewrite(model="ERNIE Speed-AppBuilder")
                    self.play = Playground(
                        prompt_template="{query}",
                        model="eb-4"
                    )

                def run(self, message: Message, stream: bool=False):
                    user_session = UserSession()
                    # 获取 Session 历史数据
                    history_queries = user_session.get_history("query", limit=1)
                    history_answers = user_session.get_history("answer", limit=1)

                    if history_queries and history_answers:
                        history = []
                        for query, answer in zip(history_queries, history_answers):
                            history.extend([query.content, answer.content])
                        logging.info(f"history: {history}")
                        message = self.query_rewrite(
                            Message(history + [message.content]), rewrite_type="带机器人回复")
                    logging.info(f"message: {message}") 
                    answer = self.play.run(message, stream)
                    # 保存本轮数据
                    user_session.append({
                        "query": message,
                        "answer": answer,
                    }) 
                    return answer

            agent = AgentRuntime(component=PlaygroundWithHistory())
            agent.chainlit_demo(port=8091)

    ** 请求时认证 **: component在创建时可以不进行认证，由AgentRuntime服务化后带入AppbuilderToken

    Examples:

        .. code-block:: python

            import appbuilder
            
            component = appbuilder.Playground(
                prompt_template="{query}",
                model="eb-4",
                lazy_certification=True, # 在创建时不进行认证
            )
            agent = appbuilder.AgentRuntime(component=component)
            agent.serve(debug=False, port=8091)
 
        .. code-block:: shell
            curl --location 'http://0.0.0.0:8091/chat' \
                --header 'Content-Type: application/json' \
                --header 'X-Appbuilder-Token: ...' \
                --data '{
                    "message": "你是谁",
                    "stream": false
                }'

    """
    component: Component
    user_session_config: Optional[Union[sqlalchemy.engine.URL, str]] = None
    user_session: Optional[UserSession] = None

    class Config:
        """
        检查配置
        """
        extra = Extra.forbid # 不能传入类定义中未声明的字段
        arbitrary_types_allowed = True # 此设置允许在模型中使用自定义类型的字段

    @model_validator(mode='before')
    @classmethod
    def init(cls, values: Dict) -> Dict:
        """
        初始化 AgentRuntime，UserSession 会在这里被初始化
        
        Args:
            values (Dict): 初始化参数
        Returns:
            None
        """
        # 初始化 UserSession
        values.update({
            "user_session": UserSession(values.get("user_session_config"))
        })
        return values

    def chat(self, message: Message, stream: bool=False, **args) -> Message:
        """
        执行一次对话
        
        Args:
            message (Message): 该次对话用户输入的 Message
            stream (bool): 是否流式请求
            **args: 其他参数，会被透传到 component
        
        Returns:
            Message
        """
        return self.component.run(message=message, stream=stream, **args)
        
    def create_flask_app(self, url_rule="/chat"):
        """ 
        创建 Flask 应用，主要用于 Gunicorn 这样的 WSGI 服务器来运行服务。
        
        Args:
            None
        
        Returns:
            Flask
        """
        # lazy import flask
        try:
            from flask import Flask, current_app, request, Response
            from flask_restful import reqparse, Resource
            from werkzeug.exceptions import BadRequest
        except ImportError:
            raise ImportError("Flask module is not installed. Please install it using 'pip install "
                              "flask~=2.3.2 flask-restful==0.3.9'.")
        app = Flask(__name__)
        app.json.ensure_ascii = False

        @app.errorhandler(BadRequest)
        def handle_bad_request(e):
            return {"code": 400, "message": f'{e}', "result": None}, 400
            
        @app.errorhandler(Exception)
        def handle_bad_request(e):
            if hasattr(e, "code"):
                return {"code": e.code, "message": str(e), "result": None}, 200
            else:
                return {"code": 500, "message": "Internal Server Error", "result": None}, 200

        def warp():
            # 根据component是否lazy_certification，分成两种情况：
            # 1. lazy_certification为True，初始化时未被认证，每次请求都需要带入AppbuilderToken
            # 2. lazy_certification为False，初始化时已经认证，请求时不需要带入AppbuilderToken，并且带入也无效
            if self.component.lazy_certification:
                if "X-Appbuilder-Token" not in request.headers:
                    raise BadRequest("X-Appbuilder-Token is required in Headers")
                try:
                    app_builder_token = request.headers["X-Appbuilder-Token"]
                    self.component.set_secret_key_and_gateway(secret_key=app_builder_token)
                except appbuilder.core._exception.BaseRPCException as e:
                    logging.error(f"failed to verify. err={e}", exc_info=True)
                    raise BadRequest("X-Appbuilder-Token invalid")
                except Exception as e:
                    logging.error(f"failed to verify. err={e}", exc_info=True)
                    raise e
            else:
                pass

            data = request.get_json()
            if "message" not in data:
                raise BadRequest("message is required")
            message = Message(data.pop('message'))
            if "session_id" not in data:
                session_id = str(uuid.uuid4())
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
            request_id = str(uuid.uuid4())

            init_context(session_id=session_id, request_id=request_id)
            logging.info(f"[request_id={request_id}, session_id={session_id}] message={message}, stream={stream}, data={data}")
            try:
                answer = self.chat(message, stream, **data)
                if stream:
                    def gen_sse_resp(stream_message):
                        with app.app_context():
                            try:
                                content_iterator = iter(stream_message.content)
                                prev_content = next(content_iterator)
                                prev_result = copy.deepcopy(stream_message)
                                prev_result.content = prev_content
                                for sub_content in content_iterator:
                                    logging.info(f"[request_id={request_id}, session_id={session_id}] streaming_result={prev_result}")
                                    yield "data: " + json.dumps({
                                            "code": 0, "message": "", 
                                            "result": {
                                                "session_id": session_id, 
                                                "is_completion": False, 
                                                "answer_message": json.loads(prev_result.json(exclude_none=True))
                                            }
                                        }, ensure_ascii=False) + "\n\n"
                                    prev_result = copy.deepcopy(stream_message)
                                    prev_result.content = sub_content
                                logging.info(f"[request_id={request_id}, session_id={session_id}] streaming_result={prev_result}")
                                yield "data: " + json.dumps({
                                        "code": 0, "message": "", 
                                        "result": {
                                            "session_id": session_id, 
                                            "is_completion": True, 
                                            "answer_message": json.loads(prev_result.json(exclude_none=True))
                                        }
                                    }, ensure_ascii=False) + "\n\n"
                                self.user_session._post_append()
                            except Exception as e:
                                code = 500 if not hasattr(e, "code") else e.code
                                err_resp = {"code": code, "message": str(e), "result": None}
                                logging.error(f"[request_id={request_id}, session_id={session_id}] err={e}", exc_info=True)
                                yield "data: " + json.dumps(err_resp, ensure_ascii=False) + "\n\n"
                    return Response(
                        gen_sse_resp(answer), 200, 
                        {'Content-Type': 'text/event-stream; charset=utf-8'},
                    )
                else:
                    blocking_result = json.loads(copy.deepcopy(answer).json(exclude_none=True))
                    logging.info(f"[request_id={request_id}, session_id={session_id}] blocking_result={blocking_result}")
                    self.user_session._post_append()
                    return {
                        "code": 0, "message": "", 
                        "result": {"session_id": session_id, "answer_message": blocking_result}
                    }
            except Exception as e:
                logging.error(f"[request_id={request_id}, session_id={session_id}] err={e}", exc_info=True)
                raise e

        app.add_url_rule(url_rule, 'chat', warp, methods=['POST'])
        return app

    def serve(self, host='0.0.0.0', debug=True, port=8092, url_rule="/chat"):
        """ 
        将 component 服务化，提供 Flask http API 接口
        
        Args:
            host (str): 服务 host
            debug (bool): 是否是 debug 模式
            port (int): 服务 port
        
        Returns:
            None
        """
        app = self.create_flask_app(url_rule=url_rule)
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
        # lazy import chainlit
        try:
            import chainlit as cl
            import chainlit.cli
        except ImportError:
            raise ImportError("chainlit module is not installed. Please install it using 'pip install "
                              "chainlit~=1.0.200'.")
        import click
        from click.testing import CliRunner
        
        @cl.on_message  # this function will be called every time a user inputs a message in the UI
        async def main(message: cl.Message):
            session_id = cl.user_session.get("id")
            request_id = str(uuid.uuid4())
            init_context(session_id=session_id, request_id=request_id)
            msg = cl.Message(content="")
            await msg.send()
            stream_message = self.chat(Message(message.content), stream=True)

            for part in stream_message.content:
                if token := part or "":
                    await msg.stream_token(token)
            await msg.update()
            self.user_session._post_append()

        # start chainlit service
        if os.getenv('APPBUILDER_RUN_CHAINLIT') == '1':
            pass
        else:
            os.environ['APPBUILDER_RUN_CHAINLIT'] = '1'
            target = sys.argv[0]
            runner = CliRunner()
            runner.invoke(
                chainlit.cli.chainlit_run, [target, '--watch', "--port", port, "--host", host])

