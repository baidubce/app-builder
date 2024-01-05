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
from typing import Union, List, Dict, Optional
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from appbuilder.core.message import Message
from appbuilder.core.context import get_context


_db = declarative_base()


class SessionMessage(_db):
    """
    会话数据模型
    """
    __tablename__ = 'appbuilder_session_messages'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    session_id = Column(String(36), nullable=False)
    request_id = Column(String(36), nullable=False)
    message_key = Column(String(128), nullable=False)
    message_value = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)


class UserSession(object):
    """
    会话数据管理工具，实例化后将是一个全局变量。
    提供保存对话数据与获取历史数据的方法，**必须**在 AgentBase 启动的服务中使用。
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, user_session_config: Optional[Union[sqlalchemy.engine.URL, str]] = None):
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
        self._db_session = Session()

    def get_history(self, key: str, limit: int=10) -> List[Message]:
        """
        获取同个 session 中名为 key 的历史变量
        
        Args:
            key (str): 变量名
            limit (int): 获取最近的几条 session 数据
        
        Returns:
            List[Message]
        """
        ctx = get_context()
        session_messages = self._db_session.query(SessionMessage).filter(
            SessionMessage.session_id == ctx.session_id,
            SessionMessage.message_key == key,
            SessionMessage.deleted == False).order_by(
                SessionMessage.updated_at.desc()).limit(limit).all()
        return [Message(content=item.message_value) for item in session_messages][::-1]

    def set(self, key: str, message: Message) -> None:
        """
        保存一个变量到 session 中，变量名为 key 值为 message
        
        Args:
            key (str): 变量名
            message (Message): 想要保存的 message
        
        Returns:
            None
        """
        ctx = get_context()
        if not isinstance(message, Message):
            raise ValueError("message must be Message type")
        if key in ctx.session_vars_dict:
            raise keyError(f"key {key} has already been set")
        ctx.session_vars_dict[key] = message

    def _post_set(self) -> None:
        """
        后置保存。流式数据不能直接保存到数据库，需要通过该方法后置保存。
        
        Args:
            None
        
        Returns:
            None
        """
        ctx = get_context()
        try:
            for key, message_value in ctx.session_vars_dict.items():
                message = SessionMessage(
                    session_id=ctx.session_id,
                    request_id=ctx.request_id,
                    message_key=key,
                    message_value=json.loads(message_value.json(exclude_none=True)),
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now())
                self._db_session.add(message)
                self._db_session.commit()
        except Exception as e:
            logging.error(e)
            self._db_session.rollback()
            raise e