"""chainlit deploy"""
import os, sys
import shutil
import json
from typing import Any, Optional, Union
from click.testing import CliRunner
import uuid
import logging

import appbuilder
from appbuilder.core.component import Component, Content
from appbuilder.core.message import Message
from appbuilder.utils.logger_util import logger
from appbuilder.core.context import init_context
from appbuilder.core.user_session import UserSession
from appbuilder.core.console.appbuilder_client.data_class import ToolChoice, Action


class ChainlitRuntime(object):
    """ChainlitRuntime 是对组件和应用调用的chainlit服务化封装，开发者不是必须要用 ChainlitRuntime 才能运行自己的组件服务。
    ChainlitRuntime 可以快速帮助开发者服务化组件服务，并且提供对话框部署功能。
    此外，结合 Component 和 Message 自带的运行和调试接口，可以方便开发者快速获得一个调试 Agent 的服务。

    Examples:

    .. code-block:: python

        import os
        import sys
        import appbuilder
        from appbuilder.utils.chainlit_deploy import ChainlitRuntime
        os.environ["APPBUILDER_TOKEN"] = '...'

        component = appbuilder.Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = ChainlitRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        print(agent.chat(message, stream=False))

    .. code-block:: python

        import os
        import sys
        import appbuilder
        from appbuilder.utils.chainlit_deploy import ChainlitRuntime
        from 
        os.environ["APPBUILDER_TOKEN"] = '...'

        component = appbuilder.Playground(
            prompt_template="{query}",
            model="eb-4"
        )
        agent = ChainlitRuntime(component=component)
        message = appbuilder.Message({"query": "你好"})
        print(agent.chat(message, stream=False))

    .. code-block:: python

        import os
        import sys
        import appbuilder
        from appbuilder.utils.chainlit_deploy import ChainlitRuntime
        from appbuilder.core.components.v2 import SimilarQuestion
        os.environ["APPBUILDER_TOKEN"] = '...'
        component = SimilarQuestion()
        agent = ChainlitRuntime(component=component)
        agent.chainlit_component_debug(
            port=8092, 
            tool_eval_args={},
            query_name = "query"
        )

    Session 数据管理 : 除去上述简单应用外，还支持 Session 数据管理，下面是一个例子

    .. code-block:: python

        import os
        import sys
        from appbuilder.core.component import Component
        from appbuilder import (
            ChainlitRuntime, UserSession, Message, QueryRewrite, Playground,
        )

        os.environ["APPBUILDER_TOKEN"] = '...'

        class PlaygroundWithHistory(Component):
            def __init__(self):
                super().__init__()
                self.query_rewrite = QueryRewrite(model="Qianfan-Agent-Speed-8k")
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

        agent = ChainlitRuntime(component=PlaygroundWithHistory())
        agent.chainlit_component(port=8091)

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
    def __init__(self,
            component: Component,
            user_session_config: Optional[Union[Any, str]] = None,
            user_session: Optional[UserSession] = None,
            tool_choice: ToolChoice = None 
        ):
        """init

        Args:
            component (Component): 需要服务化的组件实例
            user_session_config (sqlalchemy.engine.URL|str|None): Session 输出存储配置字符串。默认使用 sqlite:///user_session.db
                遵循 sqlalchemy 后端定义，参考文档：https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
            user_session (UserSession): 用户会话管理器，如果不指定则自动生成一个默认的 UserSession
            tool_choice (ToolChoice): 可用于Agent强制执行的组件工具

        """
        self.component = component
        if user_session is None:
            if user_session_config is None:
                self.user_session = UserSession()
                logger.info("init user_session with default UserSession")
            else:
                self.user_session = UserSession(user_session_config)
                logger.info("init user_session with user_session_config")
        else:
            self.user_session = user_session
        self.tool_choice = tool_choice
        self._prepare_chainlit_readme()
    
    def chat(self, message: Message, stream: bool = False, **kwargs) -> Message:
        """
        执行一次对话

        Args:
            message (Message): 该次对话用户输入的 Message
            stream (bool): 是否流式请求
            **args: 其他参数，会被透传到 component

        Returns:
            Message(Message): 返回的 Message
        """
        return self.component.run(message=message, stream=stream, **kwargs)

    def _prepare_chainlit_readme(self):
        """
        准备 Chainlit 的 README 文件
        从 utils 文件夹中拷贝 chainlit.md 文件到当前工作目录下，如果当前工作目录下已存在 chainlit.md 文件，则不拷贝。
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            None 
        """
        try:
            # 获取当前python命令执行的路径，而不是文件的位置
            cwd_path = os.getcwd()
            # 获取当前文件的路径所在文件夹
            current_file_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            chainlit_readme_path = os.path.join(
                current_file_path, "utils/chainlit.md")
            logger.debug(f"chainlit_readme_path:{chainlit_readme_path}")
            if not os.path.exists(chainlit_readme_path):
                raise FileNotFoundError(f"Chainlit readme file not found at {chainlit_readme_path}")
            
            # 拷贝chainlit_readme到cwd_path
            # 如果cwd_path下已经存在chainlit_readme，则不拷贝
            if not os.path.exists(os.path.join(cwd_path, "chainlit.md")):
                shutil.copy(chainlit_readme_path, cwd_path)
                logger.info("chainlit readme file copied successfully")
        except:
            logger.error("Failed to copy chainlit.md to current directory")   

    def chainlit_component(self, host='0.0.0.0', port=8091):
        """
        将 component 服务化，提供 chainlit demo 页面

        Args:
            host (str): 服务 host
            port (int): 服务 port

        Returns:
            None
        """
        try:
            import chainlit as cl
            import chainlit.cli
        except ImportError:
            raise ImportError("chainlit module is not installed. Please install it using 'pip install "
                                "chainlit'.")
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

        if os.getenv('APPBUILDER_RUN_CHAINLIT') == '1':
            pass
        else:
            os.environ['APPBUILDER_RUN_CHAINLIT'] = '1'
            target = sys.argv[0]
            runner = CliRunner()
            runner.invoke(
                chainlit.cli.chainlit_run, [target, '--watch', "--port", port, "--host", host])
        
    def chainlit_component_debug(
            self, 
            host='0.0.0.0', 
            port=8092, 
            query_name: str = "query",
            tool_eval_args: dict = {}):
        """componnet tool_eval"""
        """
        将 appbuilder component 服务化，内部调用组件tool_eval方法，提供 chainlit demo 页面和各类型输出的渲染效果。
        注意：目前只支持新协议组件

        Args:
            host (str): 服务 host
            port (int): 服务 port
            query_name(str): 组件tool_eval运行时接收自然语言输入的变量名
            tool_eval_args(dict): 组件tool_eval运行需要的其他参数

        Returns:
            None
        """
        try:
            import chainlit as cl
            import chainlit.cli
        except ImportError:
            raise ImportError("chainlit module is not installed. Please install it using 'pip install "
                                "chainlit'.")

        def _chat(message: cl.Message):
            query = message.content
            tool_eval_args.update({query_name: query})
            tool_result = self.component.tool_eval(**tool_eval_args)
            try:
                message_result = _convert_componentoutput_to_msg(tool_result)
                yield from message_result
            except Exception as e:
                text = "组件输出报错：" + str(e)
                elements = [
                    cl.Text(
                        name="error",
                        content=text
                    )
                ]
                message_result = cl.Message(
                    content="组件输出报错",
                    elements=elements
                )
                yield message_result

        def _echart_to_plotly(echarts_data):
            """把echart图表数据转换为plotly.graph_objects.Figure图片"""
            try:
                import plotly.graph_objects as go
            except ImportError:
                raise ImportError("plotly module is not installed. Please install it using 'pip install plotly'")

            fig = go.Figure()

            # 处理不同的图表类型
            for series in echarts_data.get('series', []):
                if "dataset" in echarts_data:
                    data = echarts_data['dataset'][0]["source"]
                else:
                    data = series['data']

                if series['type'] == 'bar':
                    fig.add_trace(go.Bar(
                        x=echarts_data['xAxis']['data'],
                        y=data,
                        name=series.get('name', '')
                    ))
                elif series['type'] == 'line':
                    if 'xAxis' in echarts_data and 'data' in echarts_data['xAxis']:
                        x = echarts_data['xAxis']['data']
                        y = data
                    else:
                        x = [point[0] for point in data]
                        y = [point[1] for point in data]
                    fig.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        mode='lines+markers',
                        name=series.get('name', '')
                    ))
                elif series['type'] == 'scatter':
                    fig.add_trace(go.Scatter(
                        x=[point[0] for point in data],
                        y=[point[1] for point in data],
                        mode='markers',
                        name=series.get('name', '')
                    ))
                elif series['type'] == 'pie':
                    fig.add_trace(go.Pie(
                        labels=[item['name'] for item in data],
                        values=[item['value'] for item in data],
                        name=series.get('name', '')
                    ))
                elif series['type'] in ['tree', 'treemap']:
                    data = data[0]['children']
                    def process_data(data, parent=""):
                        labels = []
                        parents = []
                        for item in data:
                            labels.append(item['name'])
                            parents.append(parent)
                            if item['children']:
                                child_labels, child_parents = process_data(item['children'], item['name'])
                                labels.extend(child_labels)
                                parents.extend(child_parents)
                        return labels, parents

                    labels, parents = process_data(data)

                    # 创建Treemap图
                    fig.add_trace(go.Treemap(
                        labels=labels,
                        parents=parents
                    ))
                elif series['type'] == 'funnel':
                    fig.add_trace(go.Funnel(
                        y=[item['name'] for item in data],
                        x=[item['value'] for item in data]
                    ))
                elif series['type'] == 'radar':
                    indicator_data = echarts_data["radar"]["indicator"]
                    series_data = data[0]["value"]
                    for indicator in indicator_data:
                        fig.add_trace(go.Scatterpolar(
                            r=series_data,
                            theta=[indicator["name"]] * len(series_data),
                            fill="toself",
                            name=indicator["name"],
                            subplot="polar"
                        ))

            # 更新布局
            layout_update = {
                'title': echarts_data.get('title', {}).get('text', ''),
                'legend': dict(orientation='h', yanchor='bottom', y=-0.2),
                'margin': dict(t=70, r=100, b=50, l=20)
            }

            if 'radar' in echarts_data:
                layout_update['polar'] = {
                    'radialaxis': {'visible': True},
                    'angularaxis': {'visible': True}
                }
            else:
                layout_update['xaxis_title'] = echarts_data.get('xAxis', {}).get('name', '')
                if 'yAxis' in echarts_data:
                    yaxis = echarts_data['yAxis']
                    if isinstance(yaxis, list):
                        yaxis = yaxis[0]
                else:
                    yaxis = {}
                layout_update['yaxis_title'] = yaxis.get('name', '')

            fig.update_layout(**layout_update)
            return fig

        def _convert_code(name: str, code: str):
            """把组件code输出转换为code格式的Text输出"""
            from pygments.lexers import guess_lexer
            try:
                lexer = guess_lexer(code)
                language = lexer.name
            except:
                language = ""
            logging.info(f"langauge: {language}")
            return cl.Text(
                name=name,
                content=code,
                display="inline",
                language=language
            )

        def _convert_text(text):
            """解析组件Text输出，主要提取echart图表数据"""
            elements = []
            import re
            pattern = r'\n\n```echarts-option\n(.*?)\n```'
            echarts_match = re.search(pattern, text.info, re.DOTALL)
            if echarts_match:
                echarts_data = echarts_match.group(1)
                logging.info(f"chart data: {echarts_data}")
                echarts_data_list = json.loads(echarts_data)
                for echarts_data in echarts_data_list:
                    fig = _echart_to_plotly(echarts_data)
                    elements.append(cl.Plotly(
                        name="chart",
                        figure=fig,
                        display="inline"
                    ))

                rest = text.info[echarts_match.end():].strip()
                if rest:
                    elements.append(cl.Text(
                        name="text",
                        content=rest,
                        display = "inline"
                    ))
            if not echarts_match:
                elements.append(cl.Text(
                    name="text",
                    content=text.info.strip(),
                    display = "inline"
                ))
            return elements

        def _convert_content_to_elements(content: Content) -> list:
            """把AB ComponentOutput.Content转换为chainlit的elements"""
            elements = []
            type = content.type
            text = content.text
            if type == "text" or type == "oral_text":
                elements.extend(_convert_text(text))
            elif type == "image":
                elements.append(cl.Image(
                    name="image",
                    display="inline",
                    size="large",
                    url=text.url,
                ))
            elif type == "files":
                if text.url:
                    elements.append(cl.File(
                        name=text.filename,
                        url=text.url,
                        display="inline",
                    ))
            elif type == "audio":
                elements.append(cl.Audio(
                    name="audio",
                    display="inline",
                    size="medium",
                    url=text.url
                ))
            elif type == "chart":
                json_data = json.loads(text.data)
                fig = _echart_to_plotly(json_data)
                elements.append(cl.Plotly(
                    name="chart",
                    figure=fig,
                    display="inline"
                ))
            elif type == "code":
                elements.append(_convert_code(
                    "code", text.code
                ))
            elif type == "references":
                json_data = text.model_dump_json(indent=4)
                elements.append(cl.Text(
                    name="reference",
                    content=json_data,
                    display="inline",
                    language="json"
                ))
            elif type == "json":
                data = json.loads(text.data)
                data_str = json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=4
                )
                elements.append(cl.Text(
                    name="json",
                    content=data_str,
                    display="inline",
                ))
            elif type == "urls":
                elements.append(cl.Text(
                    name="url", 
                    content="下载链接："+text.url
                ))
            else:
                logging.info(f"invalid type: {type}")
                raise ValueError("invalid type")
            
            return elements

        def _convert_componentoutput_to_msg(result):
            """把ComponentOutput转换为cl.Message"""
            elements = []
            for iter in result:
                content = iter.content[0]
                elements = _convert_content_to_elements(content)
                tool_name = component.manifests[0]["name"]
                msg = cl.Message(content=tool_name, elements=elements)
                yield msg
        
        @cl.on_message  # this function will be called every time a user inputs a message in the UI
        async def main(message: cl.Message):
            logging.info(f"message: {message.content}")
            stream_message = _chat(message)
            for msg in stream_message:
                logging.info(f"msg {msg}")
                await msg.send()

            await msg.update()

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
        try:
            import chainlit as cl
            import chainlit.cli
        except ImportError:
            raise ImportError("chainlit module is not installed. Please install it using 'pip install "
                                "chainlit'.")
        if not isinstance(self.component, appbuilder.AppBuilderClient):
            raise ValueError(
                "chainlit_agent require component must be an instance of AppBuilderClient")

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

        if os.getenv('APPBUILDER_RUN_CHAINLIT') == '1':
            pass
        else:
            os.environ['APPBUILDER_RUN_CHAINLIT'] = '1'
            target = sys.argv[0]
            runner = CliRunner()
            runner.invoke(
                chainlit.cli.chainlit_run, [target, '--watch', "--port", port, "--host", host])
            

if __name__ == "__main__":
    from appbuilder.core.components.v2 import Text2Image
    component = Text2Image()
    agent = ChainlitRuntime(
        component=component,
    )
    agent.chainlit_component_debug(port=8092, tool_eval_args={},
        query_name = "query")
