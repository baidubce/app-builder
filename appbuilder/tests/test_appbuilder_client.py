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
        agent_builder = appbuilder.AgentBuilder(self.app_id)

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
        # with tempfile.NamedTemporaryFile(suffix=".png") as fp:
        #     # 上传植物图片
        #     img_url = ("https://bj.bcebos.com/v1/appbuilder/test_agent_builder_tr"
        #                "ee.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzL"
        #                "m%2F2024-03-20T08%3A03%3A16Z%2F-1%2Fhost%2F8227f2bb97928b1957a9a6"
        #                "c14c4e307ef195d18ec68b22764158690cecbd9fc7")
        #     raw_image = requests.get(img_url).content
        #     fp.write(raw_image)
        #     file_id = agent_builder.upload_local_file(conversation_id, fp.name)
        #     msg = agent_builder.run(conversation_id, "请识别图中的植物类别", file_ids=[file_id])
        #     print("助理回答内容：", msg.content.answer)
        #     fp.close()


if __name__ == '__main__':
    unittest.main()
