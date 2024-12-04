import unittest
import os
import appbuilder
from appbuilder.core.components.text_to_image.model import (Text2ImageSubmitRequest, Text2ImageSubmitResponse,
                                                            Text2ImageQueryRequest, Text2ImageQueryResponse, SubTaskResult)

from appbuilder.core._exception import RiskInputException 
from appbuilder.core.component import ComponentOutput

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestText2ImageComponent(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.text2Image = appbuilder.Text2Image()
        
    def test_run(self):
        """
        使用原始文本进行单测

        Args:
            None

        Returns:
            None

        """
        inp = appbuilder.Message(content={"prompt": "上海的经典风景"})
        out = self.text2Image.run(inp)
        print(out)
        self.assertIsNotNone(out)
        self.assertIsInstance(out, appbuilder.Message)

    def test_queryText2ImageData(self):
        """
        queryText2ImageData方法单测

        Args:
            None

        Returns:
            None

        """
        request = Text2ImageQueryRequest(
            task_id = "123456",
        )
        response = self.text2Image.queryText2ImageData(request)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, Text2ImageQueryResponse)

    def test_extract_img_urls(self):
        """
        extract_img_urls方法单测

        Args:
            None

        Returns:
            None

        """
        response = Text2ImageQueryResponse()
        response.data.task_progress = 1.0
        response.data.task_progress_detail = 0.5
        response.data.sub_task_result_list = [SubTaskResult(**{'sub_task_progress_detail':0.8, 'final_image_list': [{'img_url': 'http://example.com'}]})]
        img_urls = self.text2Image.extract_img_urls(response)
        self.assertEqual(img_urls, ['http://example.com'])

    def test_check_service_error(self):
        """
        check_service_error方法单测

        Args:
            None

        Returns:
            None

        """
        data = {"error_code": "ERROR", "error_msg": "Error message"}
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.text2Image.check_service_error("", data)

    def test_tool_eval(self):
        """
        测试 tool_eval 方法的正确性。
        
        Args:
            self: 测试类的实例。
        
        Returns:
            无返回值。
        
        Raises:
            无异常抛出。
        
        """
        result = self.text2Image.tool_eval(query = "上海的经典风景")
        for res in result:
            self.assertIsInstance(res, ComponentOutput)
            print(res)

if __name__ == '__main__':
    unittest.main()
