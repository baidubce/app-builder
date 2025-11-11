# Copyright (c) 2025 Baidu, Inc. All Rights Reserved.
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
import asyncio
import unittest
import os
import appbuilder


@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAppBuilderClientFeedback(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "2313e282-baa6-4db6-92dd-a21e99cfd59e"

    def test_async_appbuilder_parameters(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """

        async def agent_handle():
            if len(self.app_id) == 0:
                self.skipTest("self.app_id is empty")
            appbuilder.logger.setLoglevel("ERROR")
            builder = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await builder.create_conversation()
            msg = await builder.run(conversation_id, "国庆长假", stream=False, parameters={"city": "北京"})
            print(msg.content.answer)
            await builder.http_client.session.close()

        asyncio.run(agent_handle())

    def test_async_appbuilder_parameters_stream(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败

        Args:
            self (unittest.TestCase): unittest的TestCase对象

        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """

        async def agent_handle():
            if len(self.app_id) == 0:
                self.skipTest("self.app_id is empty")
            appbuilder.logger.setLoglevel("ERROR")
            builder = appbuilder.AsyncAppBuilderClient(self.app_id)
            conversation_id = await builder.create_conversation()
            msg = await builder.run(conversation_id, "元旦节", stream=True, parameters={"city": "北京"})

            async for content in msg.content:
                print(content.answer)
            await builder.http_client.session.close()

        asyncio.run(agent_handle())


if __name__ == "__main__":
    unittest.main()
