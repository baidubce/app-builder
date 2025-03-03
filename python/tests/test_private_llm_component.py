import os
import unittest
from appbuilder.core.components.llms.base import CompletionBaseComponent, ModelArgsConfig

class MockLLMComponent(CompletionBaseComponent):

    def __init__(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        print("Success")


class TestComponentInit(unittest.TestCase):
    def setUp(self):
        '''
        return mrc class
        '''
        # 设置环境变量和初始化TestMRCComponent实例
        self.model_name = "ERNIE-3.5-8K"
        self.component = MockLLMComponent(model=self.model_name)

    def test_private_llm_component_init(self):
        os.environ["PRIVATE_AB"] = "true"
        self.component.set_model_info("test_model_name", "test_model_url")
        os.environ["APPBUILDER_TOKEN"] = "abc"
        self.component.set_secret_key_and_gateway()
        model_config_inputs = ModelArgsConfig(**{"stream": True, "temperature": 0.01, "top_p": 1})
        self.component.get_model_config(model_config_inputs)
        self.component.run()


if __name__ == '__main__':
    unittest.main()
