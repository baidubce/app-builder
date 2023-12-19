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
import datetime
import uuid
import json
import os
import logging
from typing import Union, List, Dict
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from appbuilder.core.message import Message


_db = declarative_base()


class SessionMessage(_db):
    """
    会话数据模型
    """
    __tablename__ = 'appbuilder_session_messages'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    session_id = Column(String(36), nullable=False)
    query_message = Column(JSON, nullable=False)
    answer_message = Column(JSON, nullable=False)
    extra = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    def as_dict(self):
        """
        将模型转换为 dict 类型

        Args:
            None
        
        Returns:
            dict
        """
        fields = ["id", "query_message", "answer_message", "extra", "created_at", "updated_at"]
        return {field: getattr(self, field) for field in fields}


class UserSession(object):
    """
    会话数据管理工具。提供保存对话数据与获取历史对话数据的方法
  
    Examples:

        .. code-block:: python

            import os
            import sys
            import appbuilder import UserSession, Message
            
            user_session_config = "sqlite:///foo.db"
            user_session = UserSession(user_session_config)
            session_id = "634432be-9241-47ab-a055-266e89785352"
            query = Message({"query": "你好"})
            answer = Message("answer": "你好，我是文心一言。"})
            
            user_session.save_session_message(session_id, query, answer)
            print(user_session.get_session_messages(session_id)) 
    """

    def __init__(self, user_session_config: Union[sqlalchemy.engine.URL, str, None] = None):
        """
        初始化 UserSession
        
        Args:
            user_session_config (str|None): Session 配置字符串，遵循 sqlalchemy 后端定义，参考文档
              https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
        
        Returns:
            None
        """
        if user_session_config is None:
            user_session_config = "sqlite:///user_session.db"
        if not isinstance(user_session_config, (sqlalchemy.engine.URL, str)):
            raise ValueError("user_session_config must be sqlalchemy.URL or str")
        engine = create_engine(user_session_config)
        _db.metadata.create_all(engine) # 创建表
        Session = sessionmaker(engine)
        self.db_session = Session()

    def get_session_messages(self, session_id: str, limit: int=10) -> List[Message]:
        """
        获取对话历史数据
        
        Args:
            session_id (str): Session ID
            limit (int): 获取最近的几条 session 数据
        
        Returns:
            List[Message]
        """
        session_messages = self.db_session.query(SessionMessage).filter(
            SessionMessage.session_id == session_id,
            SessionMessage.deleted == False).order_by(
                SessionMessage.updated_at.desc()).limit(limit).all()
        return [Message(content=item.as_dict()) for item in session_messages][::-1]

    def save_session_message(
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
        if not isinstance(query_message, Message):
            raise ValueError("query_message must be Message")
        if not isinstance(answer_message, Message):
            raise ValueError("answer_message must be Message")
        try:
            message = SessionMessage(
                query_message=json.loads(query_message.json(exclude_none=True)),
                answer_message=json.loads(answer_message.json(exclude_none=True)),
                extra=extra,
                session_id=session_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now())
            self.db_session.add(message)
            self.db_session.commit()
        except Exception as e:
            logging.error(e)
            self.db_session.rollback()
            raise e