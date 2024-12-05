import os
import unittest
import time
import appbuilder
from appbuilder.core.component import ComponentOutput
from appbuilder.core.components.v2 import PPTGenerationFromFile


@unittest.skip(reason="暂时跳过")
class TestCarExpert(unittest.TestCase):
    def setUp(self):
        """
        初始化。

        Args:
            None.
        Returns:
            None.
        """
        self.ppt_generator = PPTGenerationFromFile()
        self.test_data = {
            '_sys_file_urls': {'test_file': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672a92c87e6f.doc'}
        }

    def _test_ppt_generation_from_file_non_stream(self):
        """测试non_stream_tool_eval
        """
        time.sleep(2)
        result = self.ppt_generator.non_stream_tool_eval(**self.test_data)
        self.assertIsInstance(result, ComponentOutput)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数
        """
        time.sleep(2)
        msg = appbuilder.Message({'file_url': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672a92c87e6f.doc'})
        result = self.ppt_generator(msg)
        # print(result)
        self.assertIsNotNone(result)
        print(f'\n[result]\n{result.content}\n')



if __name__ == '__main__':
    unittest.main()