import json
from appbuilder.core._client import HTTPClient
from appbuilder.core.component import Message, Component
from appbuilder.core.console.base import ConsoleCompletionResponse


class RAG(Component):
    """
    console RAG组件，利用console端RAG应用进行问答，即将上线

    Examples:
    
    .. code-block:: python
    
            import appbuilder
            import os

            os.environ["APPBUILDER_TOKEN"] = '...'
            conversation_id = '...'
            app_id = '...' # 线上知识库ID
            conversation_id = '...' # 会话ID，可选参数，不传默认新建会话
            rag_app = appbuilder.console.RAG(app_id)
            query = "中国的首都在哪里"
            answer = rag_app.run(appbuilder.Message(query)) # 新建会话
            print(answer)
            conversation_id = answer.conversation_id # 获取会话ID，可用于下次会话
            print(conversation_id)
            query = "它有哪些旅游景点"
            answer = rag_app.run(appbuilder.Message(query), conversation_id) # 接上次会话
            print(answer.content)
            print(answer.extra)  # 获取结果来源
    """
    name = "rag"
    integrated_url: str = "/v1/ai_engine/agi_platform/v1/instance/integrated"
    # debug_url: str = "/debug"

    def __init__(self, app_id: str = ""):
        super().__init__()
        self.app_id = app_id
        self._http_client = None

    @property
    def http_client(self):
        """
        获取HTTP客户端对象。
        
        Args:
            无参数
        
        Returns:
            HTTPClient: 返回HTTPClient对象，如果尚未创建则创建新对象。
        
        """
        if self._http_client is None:
            self._http_client = HTTPClient()
        return self._http_client

    def run(self, query: Message, conversation_id: str = "", stream: bool = False):
        """
        RAG问答
        
        Args:
            query (Message): 用户输入的文本
            conversation_id (str, optional): 会话ID，默认为空字符串，表示新建对话。
            stream (bool, optional): 是否开启流式模式，默认为False。
        
        Returns:
            Message: RAG问答的答案
        
        """
        response_mode = "streaming" if stream else "blocking"
        payload = json.dumps({"query": query.content, "app_id": self.app_id,
                              "response_mode": response_mode, "conversation_id": conversation_id})
        headers = self.http_client.auth_header()
        headers["Content-Type"] = "application/json"
        response = self.http_client.session.post(url=self.http_client.service_url(self.integrated_url),
                                                 headers=headers, data=payload, stream=True)
        response = ConsoleCompletionResponse(response, stream)
        return response.to_message()

    def debug(self, query: Message):
        """
        调试函数(RAG暂时无DEBUG服务)

        Args:
            query (Message): 待调试的消息对象
        
        Returns:
            None
        
        说明:
            这是一个用于调试的函数，接收一个消息对象作为参数，但并不返回任何值。
            你可以在这里添加任何用于调试的代码，比如打印日志或输出消息内容等。
        """
        pass
