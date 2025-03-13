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
from deprecated import deprecated
from pydantic import BaseModel, model_validator, Extra
from typing import Optional, Dict, Any, Union
import appbuilder
from appbuilder.core.context import init_context
from appbuilder.core.component import Component
from appbuilder.core.message import Message
from appbuilder.utils.logger_util import logger
from appbuilder.utils.flask_deploy import FlaskRuntime
from appbuilder.utils.chainlit_deploy import ChainlitRuntime
from appbuilder.core.console.appbuilder_client.data_class import ToolChoiceFunction, ToolChoice, Action

# 流式场景首包超时时，最大重试次数
MAX_RETRY_COUNT = 3

@deprecated(reason="deplecated. Use FlaskRuntime or ChainlitRuntime instead")
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
    flask_deploy: FlaskRuntime = None
    chainlit_deploy: ChainlitRuntime = None

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
        flask_deploy = appbuilder.FlaskRuntime(
            component=values.get("component"),
            user_session_config=values.get("user_session_config"),
            user_session=values.get("user_session")
        )
        chainlit_deploy = appbuilder.ChainlitRuntime(
            component=values.get("component"),
            user_session_config=values.get("user_session_config"),
            user_session=values.get("user_session"),
            tool_choice=values.get("tool_choice")
        )
        values.update({
            "flask_deploy": flask_deploy,
            "chainlit_deploy": chainlit_deploy
        })
        return values

    @deprecated(reason="deplecated. Use FlaskRuntime.chat or ChainlitRuntime.chat() instead")
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

    @deprecated(reason="deplecated. Use FlaskRuntime.create_flask_app() instead")
    def create_flask_app(self, url_rule="/chat"):
        """ 
        创建 Flask 应用，主要用于 Gunicorn 这样的 WSGI 服务器来运行服务。

        Args:
            None

        Returns:
            Flask
        """
        app = self.flask_deploy.create_flask_app(url_rule=url_rule)
        return app

    @deprecated(reason="deplecated. Use FlaskRuntime.serve() instead")
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

    @deprecated(reason="deplecated. Use ChainlitRuntime.chainlit_component() instead")
    def chainlit_demo(self, host='0.0.0.0', port=8091):
        """
        将 component 服务化，提供 chainlit demo 页面

        Args:
            host (str): 服务 host
            port (int): 服务 port

        Returns:
            None
        """
        self.chainlit_deploy.chainlit_component(host=host, port=port)

    @deprecated(reason="deplecated. Use ChainlitRuntime.chainlit_agent() instead")
    def chainlit_agent(self, host='0.0.0.0', port=8091):
        """
        将 appbuilder client 服务化，提供 chainlit demo 页面

        Args:
            host (str): 服务 host
            port (int): 服务 port

        Returns:
            None
        """
        self.chainlit_deploy.chainlit_component(host=host, port=port)