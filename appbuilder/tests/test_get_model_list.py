import unittest

import appbuilder
from appbuilder.utils.model_util import GetModelListRequest, Models, GetModelListResponse


class TestModels(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            None

        Returns:
            None.
        """
        self.model = Models()

    def get_model_list(self):
        """
        get_model_list方法单测

        Args:
            None

        Returns:
            None

        """
        response = appbuilder.get_model_list(apiTypefilter=["chat"])
        self.assertIsNotNone(response)

    def test_list(self):
        """
        list方法单测

        Args:
            None

        Returns:
            None

        """

        request = GetModelListRequest()
        response = self.model.list(request)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, GetModelListResponse)

    def test_check_service_error(self):
        """
        check_service_error方法单测

        Args:
            None

        Returns:
            None

        """
        data = {'error_msg': 'Error', 'error_code': 1}
        request_id = "request_id"
        with self.assertRaises(appbuilder.AppBuilderServerException):
            self.model._check_service_error(request_id, data)
        data = {'error_msg': 'No Error', 'error_code': 0}
        self.assertIsNone(self.model._check_service_error(request_id, data))


if __name__ == '__main__':
    unittest.main()
