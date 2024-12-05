import os
import unittest
import appbuilder
import time
from appbuilder.core.component import ComponentOutput
from appbuilder.core.components.v2 import PPTGenerationFromInstruction


@unittest.skip(reason="暂时跳过")
class TestV2PPTGenerationFromInstruction(unittest.TestCase):
    def setUp(self) -> None:
        self.comp = PPTGenerationFromInstruction()
        self.text = "生成一个介绍迪士尼的PPT"
        
    def _test_non_stream_tool_eval(self):
        time.sleep(2)
        result = self.comp.non_stream_tool_eval(text=self.text)
        print(result)
        self.assertIsInstance(result, ComponentOutput)

    def test_run_with_default_params(self):
        """测试 run 方法使用默认参数
        """
        time.sleep(2)
        msg = appbuilder.Message({"text": self.text})
        result = self.comp(msg)
        print(result)
        self.assertIsNotNone(result)
        print(f'\n[result]\n{result.content}\n')



if __name__ == '__main__':
    unittest.main()