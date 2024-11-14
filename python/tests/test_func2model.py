import unittest
import appbuilder
import os
from typing import Any, Dict, List, Optional

#@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_SERIAL", "")
class TestAgentRuntime(unittest.TestCase):
    def setUp(self):
        """
        设置环境变量。

        Args:
            无参数，默认值为空。

        Returns:
            无返回值，方法中执行了环境变量的赋值操作。
        """
        os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-DKaql4wY9ojwp2uMe8IEj/7ae1190aff0684153de365381d9b06beab3064c5"
        self.app_id = "7cc4c21f-0e25-4a76-baf7-01a2b923a1a7"

    def test_google_style(self):
    # Generated by vscode plugin
    # https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring
        def google_style(
            name: str,
            val: str = None,
            val_obj: Optional[Any] = None,
            val_list: List[str] = None,
            data: Dict[str, int] = None,
        ) -> str:
            """Google style docstring.

            Args:
                name (str): Name of object.
                val (str, optional): Value of obj. Defaults to None.
                val_obj (Optional[Any], optional): Real object reference. Defaults to None.
                val_list (List[str], optional): List of items with object. Defaults to None.
                data (Dict[str, int], optional): Data along with object. Defaults to None.

            Returns:
                str: Styled string.
            """
            return ""
        function_model = appbuilder.function_to_model(google_style)

        # 断言顶层的结构
        assert function_model.type == "function", "Type does not match 'function'"
        assert function_model.function["name"] == "google_style", "Function name does not match 'google_style'"
        assert function_model.function["description"] == """Google style docstring.

            Args:
                name (str): Name of object.
                val (str, optional): Value of obj. Defaults to None.
                val_obj (Optional[Any], optional): Real object reference. Defaults to None.
                val_list (List[str], optional): List of items with object. Defaults to None.
                data (Dict[str, int], optional): Data along with object. Defaults to None.

            Returns:
                str: Styled string.
            """, "Description does not match"

        # 断言参数结构
        parameters = function_model.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言各个参数的类型和描述
        properties = parameters["properties"]

        # name 参数
        assert "name" in properties, "'name' parameter missing"
        assert properties["name"]["type"] == "string", "'name' type does not match 'string'"
        assert properties["name"]["description"] == "Name of object.", "'name' description does not match"

        # val 参数
        assert "val" in properties, "'val' parameter missing"
        assert properties["val"]["type"] == "string", "'val' type does not match 'string'"
        assert properties["val"]["description"] == "Value of obj. Defaults to None.", "'val' description does not match"

        # val_obj 参数
        assert "val_obj" in properties, "'val_obj' parameter missing"
        assert properties["val_obj"]["type"] == "Optional[Any]", "'val_obj' type does not match 'object'"
        assert properties["val_obj"]["description"] == "Real object reference. Defaults to None.", "'val_obj' description does not match"

        # val_list 参数
        assert "val_list" in properties, "'val_list' parameter missing"
        assert properties["val_list"]["type"] == "List[str]", "'val_list' type does not match 'array'"
        assert properties["val_list"]["description"] == "List of items with object. Defaults to None.", "'val_list' description does not match"

        # data 参数
        assert "data" in properties, "'data' parameter missing"
        assert properties["data"]["type"] == "Dict[str, int]", "'data' type does not match 'object'"
        assert properties["data"]["description"] == "Data along with object. Defaults to None.", "'data' description does not match"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert parameters["required"] == ["name"], "'required' does not match ['name']"

    def test_google_style_bad_args_return_dict(self):
        def func(
            bad_param: str,
            bad_generic_param: List[str],
            bad_format: int,
            val: str = None,
        ) -> Dict[str, str]:
            """Google style docstring.

            Args:
                bad param (str): Bad parameter, name contains whitespace.
                bad_generic_param (List<str>): Bad generic parameter, use <> instead of []
                bad_format (int) Bad arg doc format, lost :.
                val (str    ,      optional): Value of obj. Defaults to None.

            Returns:
                Dict[str, str]: Returns a dict.
            """
            return ""
        function_model = appbuilder.function_to_model(func)
        # 断言顶层的结构
        assert function_model.type == "function", "Type does not match 'function'"
        assert function_model.function["name"] == "func", "Function name does not match 'func'"
        assert function_model.function["description"] == """Google style docstring.

            Args:
                bad param (str): Bad parameter, name contains whitespace.
                bad_generic_param (List<str>): Bad generic parameter, use <> instead of []
                bad_format (int) Bad arg doc format, lost :.
                val (str    ,      optional): Value of obj. Defaults to None.

            Returns:
                Dict[str, str]: Returns a dict.
            """, "Description does not match"

        # 断言参数结构
        parameters = function_model.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言各个参数的类型和描述
        properties = parameters["properties"]

        # bad_param 参数
        assert "bad_param" in properties, "'bad_param' parameter missing"
        assert properties["bad_param"]["type"] == "string", "'bad_param' type does not match 'string'"
        assert properties["bad_param"]["description"] == None, "'bad_param' description should be empty due to incorrect format"

        # bad_format 参数
        assert "bad_format" in properties, "'bad_format' parameter missing"
        assert properties["bad_format"]["type"] == "integer", "'bad_format' type does not match 'integer'"
        assert properties["bad_format"]["description"] == None, "'bad_format' description does not match"

        # val 参数
        assert "val" in properties, "'val' parameter missing"
        assert properties["val"]["type"] == "string", "'val' type does not match 'string'"
        assert properties["val"]["description"] == "Value of obj. Defaults to None.", "'val' description does not match"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert parameters["required"] == ["bad_param", "bad_generic_param", "bad_format"], "'required' does not match expected required parameters"

        # 断言没有多余参数
        assert len(properties) == 4, "Unexpected number of parameters in properties"


    def test_google_style_no_return(self):
        def func(
            name: str,
        ):
            """Google style docstring.

            Args:
                name (str): Name of object.

            """
            return ""
        
        function_model = appbuilder.function_to_model(func)
        # 断言顶层的结构
        assert function_model.type == "function", "Type does not match 'function'"
        assert function_model.function["name"] == "func", "Function name does not match 'func'"
        assert function_model.function["description"] == """Google style docstring.

            Args:
                name (str): Name of object.

            """, "Description does not match"

        # 断言参数结构
        parameters = function_model.function["parameters"]
        assert parameters["type"] == "object", "Parameters type does not match 'object'"
        assert "properties" in parameters, "Properties not found in parameters"

        # 断言参数类型和描述
        properties = parameters["properties"]

        # name 参数
        assert "name" in properties, "'name' parameter missing"
        assert properties["name"]["type"] == "string", "'name' type does not match 'string'"
        assert properties["name"]["description"] == "Name of object.", "'name' description does not match"

        # 断言必需参数
        assert "required" in parameters, "'required' field missing in parameters"
        assert parameters["required"] == ["name"], "'required' does not match ['name']"

        #断言没有["parameters"][1]的参数了
        assert not ("parameters" in function_model.function and len(function_model.function["parameters"]) == 1)


    def test_google_style_no_args_no_return(self):
        def func(
            name: str,
            /,
            *args,
            val: str = None,
            val_obj: Optional[Any] = None,
            data: Dict[str, int] = None,
            **kwargs,
        ) -> str:
            """Google style docstring."""
            return ""

        #断言这里会抛出参数类型缺失导致的ValueError异常
        try:
            function_model = appbuilder.function_to_model(func)
        except ValueError as e:
            print(e)
            assert str(e) == "参数 'args' 缺少类型信息，请在函数签名或注释中指定类型。"

    def test_no_doc(self):
        def func(
            name: str,
            /,
            *args,
            val: str = None,
            val_obj: Optional[Any] = None,
            data: Dict[str, int] = None,
            **kwargs,
        ) -> str:
            return ""

        # 断言这里会抛出缺少文档字符串的 ValueError 异常
        try:
            function_model = appbuilder.function_to_model(func)
        except ValueError as e:
            assert str(e) == "函数 func 缺少文档字符串", "未抛出预期的 ValueError 或信息不匹配"

    def test_priority(self):
        def get_current_weather(location: str, unit: int) -> str:
            """获取指定中国城市的当前天气信息。

            仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。

            Args:
                location (str): 城市名，例如："北京"。
                unit (str): 温度单位，支持 "celsius" 或 "fahrenheit"。

            Returns:
                str: 天气情况描述
            """
            return ""
        function_model = appbuilder.function_to_model(get_current_weather)
        parameters = function_model.function["parameters"]
        properties = parameters["properties"]
        assert "unit" in properties, "'unit' parameter missing"
        # 描述和函数签名不一致的时候，以函数签名为准
        assert properties["unit"]["type"] == 'integer', "'unit' type does not match 'integer'"
        
        def get_current_weather(location: str, unit: str) -> str:
            """获取指定中国城市的当前天气信息。

            仅支持中国城市的天气查询。参数 `location` 为中国城市名称，其他国家城市不支持天气查询。

            Args:
                location (str): 城市名，例如："北京"。
                unit (int): 温度单位，支持 "celsius" 或 "fahrenheit"。

            Returns:
                str: 天气情况描述
            """
            return ""
        function_model = appbuilder.function_to_model(get_current_weather)
        parameters = function_model.function["parameters"]
        properties = parameters["properties"]
        assert "unit" in properties, "'unit' parameter missing"
        # 描述和函数签名不一致的时候，以函数签名为准
        assert properties["unit"]["type"] == 'string', "'unit' type does not match 'string'"

  
if __name__ == '__main__':
    unittest.main()