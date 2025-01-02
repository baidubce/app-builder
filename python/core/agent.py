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
import shutil
import inspect
from pydantic import BaseModel, model_validator, Extra
from typing import Optional, Dict, Any, Union
import appbuilder
from appbuilder.core.context import init_context
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.utils.logger_util import logger
from appbuilder.core.console.appbuilder_client.data_class import ToolChoiceFunction, ToolChoice, Action

# 流式场景首包超时时，最大重试次数
MAX_RETRY_COUNT = 3


class AgentRuntime(BaseModel):
    r"""
    AgentRuntime 是对组件调用的服务化封装，开发者不是必须要用 AgentRuntime 才能运行自己的组件服务。
    但 AgentRuntime 可以快速帮助开发者服务化组件服务，并且提供API、对话框等部署方式。
    此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。

    Args:
        component (Component): 可运行的 Component, 需要实现 run(message, stream, args) 方法  
        user_session_config (sqlalchemy.engine.URL|str|None): Session 输出存储配置字符串。默认使用 sqlite:///user_session.db
            遵循 sqlalchemy 后端定义，参考文档：https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
        tool_choice (ToolChoice): 可用于Agent强制执行的组件工具


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

        Session 数据管理 : 除去上述简单应用外，还支持 Session 数据管理，下面是一个例子

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
                    self.query_rewrite = QueryRewrite(model="Qianfan-Agent-Speed-8K")
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

        请求时认证 : component在创建时可以不进行认证，由AgentRuntime服务化后带入AppbuilderToken

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

        Session 信息查看 : 查看本地user_session.db数据库内部信息，下面是一个例子

        .. code-block:: python

            import sqlite3  
            import json  
            
            # 连接到 SQLite 数据库  
            # 如果文件不存在，会自动在当前目录创建:  
            user_session_path = 'your_user_session.db地址'  
            conn = sqlite3.connect(user_session_path)  
            cursor = conn.cursor()  
            
            # 执行一条 SQL 语句，列出所有表  
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
            print(cursor.fetchall())  

            # 查询appbuilder_session_messages表的列信息  
            cursor.execute("PRAGMA table_info(appbuilder_session_messages);")  
            columns_info = cursor.fetchall()  

            column_names = [info[1] for info in columns_info]  # info[1]是列名的位置  
            for column_name in column_names:  
                print(column_name)   

            # 查询特定表中的数据  
            cursor.execute("SELECT message_value FROM appbuilder_session_messages;")  
            for row in cursor.fetchall():  
                print(json.loads(row[0]))
            
            # 关闭 Connection:  
            conn.close()

    """

    component: Component
    user_session_config: Optional[Union[Any, str]] = None
    user_session: Optional[Any] = None
    tool_choice: ToolChoice = None

    class Config:
        """
        检查配置

        Attributes:
            extra (Extra): 额外属性，默认为 Extra.forbid，即禁止添加任何额外的属性
            arbitrary_types_allowed (bool): 任意类型是否允许，默认为 True
        """
        extra = Extra.forbid  # 不能传入类定义中未声明的字段
        arbitrary_types_allowed = True  # 此设置允许在模型中使用自定义类型的字段

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
        from appbuilder.core.user_session import UserSession
        values.update({
            "user_session": UserSession(values.get("user_session_config"))
        })
        return values

    def chat(self, message: Message, stream: bool = False, **args) -> Message:
        """
        执行一次对话

        Args:
            message (Message): 该次对话用户输入的 Message
            stream (bool): 是否流式请求
            **args: 其他参数，会被透传到 component

        Returns:
            Message(Message): 返回的 Message
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
            from flask import stream_with_context

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
            """
            根据component的lazy_certification属性处理请求。
            
            Args:
                无参数。
            
            Returns:
                如果stream为True，则返回流式响应（Content-Type为text/event-stream）。
                如果stream为False，则返回包含处理结果的字典。
            
            Raises:
                BadRequest: 当请求头中缺少必要的X-Appbuilder-Authorization时抛出。
                BadRequest: 当请求体中缺少必要的message字段时抛出。
                BadRequest: 当请求体中session_id字段不是字符串类型时抛出。
                BadRequest: 当请求体中stream字段不是布尔类型时抛出。
            
            """
            # 根据component是否lazy_certification，分成两种情况：
            # 1. lazy_certification为True，初始化时未被认证，每次请求都需要带入AppbuilderToken
            # 2. lazy_certification为False，初始化时已经认证，请求时不需要带入AppbuilderToken，并且带入也无效
            if self.component.lazy_certification:
                app_builder_token = None
                for key in ["X-Appbuilder-Token", "X-Appbuilder-Authorization"]:
                    if key in request.headers:
                        app_builder_token = request.headers[key]
                        break
                if not app_builder_token:
                    raise BadRequest(
                        "X-Appbuilder-Authorization is required in Headers")
                try:
                    self.component.set_secret_key_and_gateway(
                        secret_key=app_builder_token)
                except appbuilder.core._exception.BaseRPCException as e:
                    logging.error(f"failed to verify. err={e}", exc_info=True)
                    raise BadRequest("X-Appbuilder-Authorization invalid")
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
            request_id = request.headers.get("X-Appbuilder-Request-Id", str(uuid.uuid4()))
            user_id = request.headers.get("X-Appbuilder-User-Id", None)

            init_context(session_id=session_id, request_id=request_id, user_id=user_id)
            logging.info(
                f"request_id={request_id}, session_id={session_id}] message={message},"
                f" stream={stream}, data={data}, start run...")

            def gen_sse_resp():
                with app.app_context():
                    received_first_packet = False
                    retry_count = 0
                    while retry_count < MAX_RETRY_COUNT:
                        try:
                            answer = self.chat(message, stream, **data)
                        except Exception as e:  # 调用chat方法报错，直接返回
                            code = 500 if not hasattr(e, "code") else e.code
                            err_resp = {"code": code, "message": "InternalServerError", "result": None}
                            logging.error(
                                f"request_id={request_id}, session_id={session_id}, err={e}, execute self.chat failed", exc_info=True)
                            yield "data: " + json.dumps(err_resp, ensure_ascii=False) +  "\n\n"
                            return
                        else:  # 调用chat方法成功，开始生成流式事件
                            content_iterator = iter(answer.content)
                            answer.content = None
                            result = None
                            try:
                                for sub_content in content_iterator:
                                    result = copy.deepcopy(answer)
                                    result.content = sub_content
                                    yield "data: " + json.dumps({
                                        "code": 0, "message": "",
                                        "result": {
                                            "session_id": session_id,
                                            "is_completion": False,
                                            "answer_message": json.loads(result.json(exclude_none=True))
                                        }
                                    }, ensure_ascii=False) + "\n\n"
                                    received_first_packet = True
                            except Exception as e:
                                retry_count += 1
                                logging.error(
                                    f"[request_id={request_id}, session_id={session_id}] err={e}, "
                                    f"retry_count={retry_count}", exc_info=True)
                                # 如果未收到首包且重试次数小于最大重试次数，则尝试重新执行一次chat方法
                                if not received_first_packet and retry_count < MAX_RETRY_COUNT:
                                    continue
                                else:  # 其它情况返回
                                    logging.error(
                                        f"[request_id={request_id}, session_id={session_id}] err={e}, "
                                        f"retry_count={retry_count}, received_first_packet={received_first_packet}"
                                        , exc_info=True)
                                    code = 500 if not hasattr(e, "code") else e.code
                                    err_resp = {"code": code, "message": "InternalServerError", "result": None}
                                    yield "data: " + json.dumps(err_resp, ensure_ascii=False) + "\n\n"
                                    return
                            result.content = ""
                            yield "data: " + json.dumps({
                                "code": 0, "message": "",
                                "result": {
                                    "session_id": session_id,
                                    "is_completion": True,
                                    "answer_message": json.loads(result.json(exclude_none=True))
                                }
                            }, ensure_ascii=False) + "\n\n"
                            logging.info(
                                f"request_id={request_id}, session_id={session_id}]"
                                f"retry_count={retry_count}, success response", exc_info=True)
                            self.user_session._post_append()
                            return  # 正常返回

            if stream:  # 流式
                return Response(stream_with_context(gen_sse_resp()), 200,
                        {'Content-Type': 'text/event-stream; charset=utf-8'})
            if not stream:  # 非流式
                try:
                    answer = self.chat(message, stream, **data)
                    blocking_result = json.loads(copy.deepcopy(answer).json(exclude_none=True))
                    logging.debug(f"[request_id={request_id}, session_id={session_id}] blocking_result={blocking_result}")
                    self.user_session._post_append()
                    return {
                        "code": 0, "message": "",
                        "result": {"session_id": session_id, "answer_message": blocking_result}
                    }
                except Exception as e:
                    logging.error(
                        f"[request_id={request_id}, session_id={session_id}] err={e}", exc_info=True)
                    code = 500 if not hasattr(e, "code") else e.code
                    return {"code": code, "message": "InternalServerError", "result": None}

        app.add_url_rule(url_rule, 'chat', warp, methods=['POST'])
        return app

    def serve(self, host='0.0.0.0', debug=True, port=8092, url_rule="/chat"):
        """
        将 component 服务化，提供 Flask http API 接口
        
        Args:
            host (str): 服务运行的host地址，默认为'0.0.0.0'
            debug (bool): 是否开启debug模式，默认为True
            port (int): 服务运行的端口号，默认为8092
            url_rule (str): 服务的URL规则，默认为"/chat"
        
        Returns:
            None
        """
        app = self.create_flask_app(url_rule=url_rule)
        app.run(host=host, debug=debug, port=port)

    def prepare_chainlit_readme(self):
        """
        准备 Chainlit 的 README 文件
        
        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        
        说明:
            从 utils 文件夹中拷贝 chainlit.md 文件到当前工作目录下，如果当前工作目录下已存在 chainlit.md 文件，则不拷贝。
        
        """
        try:
            # 获取当前python命令执行的路径，而不是文件的位置
            cwd_path = os.getcwd()
            # 获取当前文件的路径所在文件夹
            current_file_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            chainlit_readme_path = os.path.join(
                current_file_path, "utils", "chainlit.md")

            # 拷贝chainlit_readme到cwd_path
            # 如果cwd_path下已经存在chainlit_readme，则不拷贝
            if not os.path.exists(os.path.join(cwd_path, "chainlit.md")):
                shutil.copy(chainlit_readme_path, cwd_path)
        except:
            logger.error("Failed to copy chainlit.md to current directory")

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

        self.prepare_chainlit_readme()

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

    def chainlit_agent(self, host='0.0.0.0', port=8091):
        """
        将 appbuilder client 服务化，提供 chainlit demo 页面

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

        if not isinstance(self.component, appbuilder.AppBuilderClient):
            raise ValueError(
                "chainlit_agent require component must be an instance of AppBuilderClient")
        self.prepare_chainlit_readme()

        conversation_ids = []
        interrupt_dict = {}

        def _chat(message: cl.Message):
            if len(conversation_ids) == 0:
                raise ValueError("create new conversation failed!")
            conversation_id = conversation_ids[-1]
            file_ids = []
            if len(message.elements) > 0:
                file_id = self.component.upload_local_file(
                    conversation_id, message.elements[0].path)
                file_ids.append(file_id)

            interrupt_ids = interrupt_dict.get(conversation_id, [])
            interrupt_event_id = interrupt_ids.pop() if len(interrupt_ids) > 0 else None
            action = None
            if interrupt_event_id is not None:
                action = Action.create_resume_action(interrupt_event_id)
            
            tmp_message = self.component.run(conversation_id=conversation_id, query=message.content, file_ids=file_ids,
                                      stream=True, tool_choice=self.tool_choice, action=action)
            res_message=list(tmp_message.content)
            
            interrupt_event_id = None
            for ans in res_message:
                for event in ans.events:
                    if event.content_type == "chatflow_interrupt":
                        interrupt_event_id = event.detail.get("interrupt_event_id")
                    if event.content_type == "publish_message" and event.event_type == "chatflow":
                        answer = event.detail.get("message")
                        ans.answer += answer
                        
            if interrupt_event_id is not None:
                interrupt_ids.append(interrupt_event_id)
                interrupt_dict[conversation_id] = interrupt_ids
            tmp_message.content = res_message
            return tmp_message

        @cl.on_chat_start
        async def start():
            session_id = cl.user_session.get("id")
            request_id = str(uuid.uuid4())
            init_context(session_id=session_id, request_id=request_id)
            conversation_ids.append(self.component.create_conversation())
            interrupt_dict[conversation_ids[-1]] = []

        @cl.on_message  # this function will be called every time a user inputs a message in the UI
        async def main(message: cl.Message):
            msg = cl.Message(content="")
            await msg.send()
            await msg.update()

            stream_message = _chat(message)
            detail_json_list = []
            for part in stream_message.content:
                if token := part.answer or "":
                    await msg.stream_token(token)
                for event in part.events:
                    detail = event.detail
                    detail_json = json.dumps(
                        detail, indent=4, ensure_ascii=False)
                    detail_json_list.append(detail_json)
            await msg.update()

            @cl.step(name="详细信息")
            def show_json(detail_json):
                return "```json\n" + detail_json + "\n```"
            for detail_json in detail_json_list:
                if len(detail_json) > 2:
                    show_json(detail_json)
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
