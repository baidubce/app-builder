import unittest
import appbuilder
import requests
import tempfile
import os

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL","")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        self.app_id = "aa8af334-df27-4855-b3d1-0d249c61fc08"

    def test_agent_builder_client(self):
        agent_builder = appbuilder.AppBuilderClient(self.app_id)

    def test_agent_builder_run(self):
        # 如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
        """
        如果app_id为空，则跳过单测执行, 避免单测因配置无效而失败
    
        Args:
            self (unittest.TestCase): unittest的TestCase对象
    
        Raises:
            None: 如果app_id不为空，则不会引发任何异常
            unittest.SkipTest (optional): 如果app_id为空，则跳过单测执行
        """
        if len(self.app_id) == 0:
            self.skipTest("self.app_id is empty")
    
        builder = appbuilder.AppBuilderClient(self.app_id)
        conversation_id = builder.create_conversation()
        msg = builder.run(conversation_id, "你可以做什么？")
        print(msg)
        respid = builder.upload_local_file(conversation_id, "./data/qa_appbuilder_client_demo.pdf")
        print(respid)
        
    def test_upload_local_file_raise(self):
        builder = appbuilder.AppBuilderClient(self.app_id)
        with self.assertRaises(ValueError):
            builder.upload_local_file(conversation_id='', local_file_path='')
            
        with self.assertRaises(ValueError):
            builder.run(conversation_id='', query='')


if __name__ == '__main__':
    unittest.main()
