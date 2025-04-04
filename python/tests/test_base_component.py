import os
import unittest
from appbuilder.core.component import Component
from appbuilder.core.component import ComponentOutput, Urls, Chart

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestBaseComponent(unittest.TestCase):
    def setUp(self) -> None:
        self.component = Component()


    def test_valid_output_with_str(self):
        out1 = self.component.create_output(type="text", text="test")
        out2 = self.component.create_output(type="code", text="import appbuilder")
        out3 = self.component.create_output(type="urls", text="http://www.baidu.com")
        out4 = self.component.create_output(type="oral_text", text="你是哪个")
        out5 = self.component.create_output(type="json", text="{'key':'value'}")
        self.assertIsInstance(out1, ComponentOutput)
        self.assertIsInstance(out2, ComponentOutput)
        self.assertIsInstance(out3, ComponentOutput)
        self.assertIsInstance(out4, ComponentOutput)
        self.assertIsInstance(out5, ComponentOutput)

    def test_valid_output_with_dict(self):
        output1 = self.component.create_output(type="text", text={"info": "1"})
        output2 = self.component.create_output(type="code", text={"code": "1"})
        output3 = self.component.create_output(type="urls", text={"url": "http://www.baidu.com"})
        output4 = self.component.create_output(type="oral_text", text={"info": "你好"})
        output5 = self.component.create_output(type="files", text={"filename": "file.txt", "url": "http://www.baidu.com"})
        output6 = self.component.create_output(type="image", text={"filename": "file.png", "url": "http://www.baidu.com"})
        output7 = self.component.create_output(type="chart", text={"type": "chart", "data": '{"key": "value"}'})
        output8 = self.component.create_output(type="audio", text={"filename": "file.mp3", "url": "http://www.baidu.com"})
        output9 = self.component.create_output(type="plan", text={"detail": "hello", "steps":[{"name": "1", "arguments": {"query": "a", "chat_history": "world"}}]})
        output10 = self.component.create_output(type="function_call", text={"thought": "hello", "name": "AppBuilder", "arguments": {"query": "a", "chat_history": "world"}})
        output11 = self.component.create_output(type="references", text={"type": "engine", "doc_id": "1", "content": "hello, world", "title": "Have a nice day", "source": "bing", "extra": {"key": "value"}})
        output12 = self.component.create_output(type="json", text={"data": "value"})
        output13 = self.component.create_output(type="screenshot", text={"browser_url": "http://www.baidu.com"})
        self.assertIsInstance(output1, ComponentOutput)
        self.assertIsInstance(output2, ComponentOutput)
        self.assertIsInstance(output3, ComponentOutput)
        self.assertIsInstance(output4, ComponentOutput)
        self.assertIsInstance(output5, ComponentOutput)
        self.assertIsInstance(output6, ComponentOutput)
        self.assertIsInstance(output7, ComponentOutput)
        self.assertIsInstance(output8, ComponentOutput)
        self.assertIsInstance(output9, ComponentOutput)
        self.assertIsInstance(output10, ComponentOutput)
        self.assertIsInstance(output11, ComponentOutput)
        self.assertIsInstance(output12, ComponentOutput)
        self.assertIsInstance(output13, ComponentOutput)
        self.assertEqual(output11.content[0].text.extra["key"], "value")

    def test_valid_output_type_with_same_key(self):
        output1 = self.component.create_output(type="urls", text={"url": "http://www.baidu.com"})
        self.assertIsInstance(output1.content[0].text, Urls)
        output2 = self.component.create_output(type="chart", text={"type": "chart_sheet", "data": '{"key": "value"}'})
        self.assertIsInstance(output2.content[0].text, Chart)
        with self.assertRaises(ValueError):
            output = self.component.create_output(type="files", text=["http://www.baidu.com"])
        with self.assertRaises(ValueError):
            output = self.component.create_output(type="test", text={"filename": "file.txt", "url": ["http://www.baidu.com"]})
        
        
        
    def test_invalid_output_type_json(self):
        with self.assertRaises(ValueError):
            output = self.component.create_output(type="test", text="")


if __name__ == '__main__':
    unittest.main()