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
import unittest
import os
import uuid
import sqlite3

from appbuilder.core.user_session import UserSession
from appbuilder.core.session_message import SessionMessage
from appbuilder.core.context import init_context,_LOCAL_KEY,get_context,context_var
from appbuilder.core.message import Message 


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestCoreUserSession(unittest.TestCase):      
    def test_usersession_init(self):
        UserSession._instance = None 
        UserSession._initialized = False 
        with self.assertRaises(ValueError):
            user_session=UserSession(user_session_config=1234)
        UserSession._instance = None 
        UserSession._initialized = False  
    
    def test_get_context(self):
        get_context() 
          
    def test_not_startswith_LOCAL_KEY(self): 
        user_session = UserSession()
        init_context(
            session_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4())
        )
        key = "test_key"
        message_dict = {key: Message(content={"key": "value"})}
        # if key not in ctx.session_vars_dict
        user_session.append(message_dict)
        history = user_session.get_history(key)
        self.assertEqual(len(history), 0)
        # if not isinstance(message, Message)
        with self.assertRaises(ValueError):
            user_session.append({key: "test"})
        # 测试if key in ctx.session_vars_dict
        with self.assertRaises(KeyError):
            user_session.append(message_dict)       
        # 测试_post_append(self)的try
        user_session._post_append()

    def test_startswith_LOCAL_KEY(self):
        user_session = UserSession()
        init_context(
            session_id=_LOCAL_KEY+str(uuid.uuid4()),
            request_id=_LOCAL_KEY+str(uuid.uuid4())               
        )
        key = "test_key"
        message_dict = {key: Message(content={"key": "value"})}
        # if key not in ctx.session_vars_dict
        user_session.append(message_dict)
        history = user_session.get_history("test")
        self.assertEqual(len(history), 0) 
        history = user_session.get_history(key)
        self.assertEqual(len(history), 1)
        # if not isinstance(message, Message)
        with self.assertRaises(ValueError):
            user_session.append({key: "test"})
        # 测试_post_append(self)的异常 
        with self.assertRaises(Exception):
            user_session._post_append()  

        # 验证user_session.db文件是否创建,并验证文件内容
        user_session_path = 'user_session.db' 
        conn = sqlite3.connect(user_session_path)  
        cursor = conn.cursor()  

        # 执行一条 SQL 语句，列出所有表  
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
        sql = cursor.fetchall()
        print('sql:{}'.format(sql))  
        assert sql[0][0] == 'appbuilder_session_messages'  
        # 执行一条 SQL 语句，列出表所有列  
        cursor.execute("PRAGMA table_info(appbuilder_session_messages);")  
        
        columns_info = cursor.fetchall()  

        column_names = [info[1] for info in columns_info]  # info[1]是列名的位置  
        for column_name in column_names:  
            print(column_name)
        assert 'id' in column_names   
        
          
if __name__ == '__main__':
    unittest.main()