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

db = None

def get_db_base_class():
    try:
        from sqlalchemy.orm import declarative_base
    except ImportError as e:
        raise ImportError("Please install SQLAlchemy first: python3 -m pip install SQLAlchemy==2.0.31")
    
    global db

    if not db:
        db = declarative_base()

    return db

class SessionMessage(get_db_base_class()):
        """
        会话 Message 数据模型，用于在数据库中存储和管理会话消息。

        以下是每个字段的注释：
        __tablename__：数据库表名为 appbuilder_session_messages，这是该类对应的数据库表名。
        id：主键字段，使用UUID作为默认值，确保每条记录的唯一性。
        session_id：会话ID字段，不允许为空，用于标识会话。
        request_id：请求ID字段，不允许为空，用于标识请求。
        message_key：Message 键字段，不允许为空，用于标识 Message 的关键字。
        message_value：Message 值字段，不允许为空，用于存储 Message 的具体内容，使用JSON格式存储。
        created_at：创建时间字段，使用当前时间作为默认值，不允许为空。
        updated_at：更新时间字段，使用当前时间作为默认值，不允许为空。
        deleted：删除标记字段，使用False作为默认值，不允许为空。当该字段为True时，表示该条记录已被删除。
        """
        from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
        __tablename__ = 'appbuilder_session_messages'

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
        session_id = Column(String(36), nullable=False)
        request_id = Column(String(36), nullable=False)
        message_key = Column(String(128), nullable=False)
        message_value = Column(JSON, nullable=False)
        created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
        updated_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
        deleted = Column(Boolean, default=False, nullable=False)