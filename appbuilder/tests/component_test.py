import requests
import types
import re 
import inspect

from typing import TypeVar, Generic, Union, Type
from appbuilder.core._exception import *
from unittest.mock  import Mock
from appbuilder.core import components
from appbuilder.core._session import InnerSession


Data_Type = {
    'string': str,
    'integer': int,
    'object': int,
    'array': list,
    'boolean': bool,
    'null': None,
}

class AppbuilderTestToolEval: 
    """
    功能:Components组件模拟post本地运行。

    使用方法：

    ```python
    # 实例化一个
    image_understand = appbuilder.ImageUnderstand()
    
    # 设计一个符合规范的tool_eval input(dict数据类型)
    tool_eval_input = {
            'streaming': True,
            'traceid': 'traceid',
            'name':"image_understand", 
            'img_url':'img_url_str', 
            'origin_query':""
        }
    
    # 设计一个组件API接口预期的response
    mock_response_data = {
            'result': {'task_id': '1821485837570181996'},
            'log_id': 1821485837570181996,
        }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'application/json'}
    def mock_json():
        return mock_response_data
    mock_response.json = mock_json
    
    # 实例化一个AppbuilderTestToolEval对象,实现组件本地的自动化测试
    appbuilder.AppbuilderTestToolEval(appbuilder_components=image_understand,
                                      tool_eval_input=tool_eval_input,
                                      response=mock_response)
    ```
    """
    def __init__(self, appbuilder_components:components, tool_eval_input:dict, response:requests.Response): 
        """
        初始化函数。
        
        Args:
            appbuilder_components (components): 应用构建器组件对象。
            tool_eval_input (dict): tool_eval的传入参数。
            response (dict): api预期的response返回值。
        
        Returns:
            None
        """
        self.component = appbuilder_components
        self.tool_eval_input = tool_eval_input
        self.response = response
        self.test_manifests()
        self.test_tool_eval_input()
        self.test_tool_eval_generator()
        if hasattr(self.component, '__module__'):
            module_name = self.component.__module__
            if re.match(r'appbuilder\.', module_name):
                self.test_tool_eval_reponse_raise()
                self.test_tool_eval_text_str()

    def test_manifests(self):
        """
        校验组件成员变量manifests是否符合规范。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        Raises:
            AppbuilderBuildexException: 校验不通过时抛出异常。
        """
        manifests = self.component.manifests
        try:
            assert isinstance(manifests, list)
            assert len(manifests) > 0
            assert isinstance(manifests[0],dict)
            assert isinstance(manifests[0]['name'], str)
            assert isinstance(manifests[0]['description'], str)
            assert isinstance(manifests[0]['parameters'], dict)
        except Exception as e:
            raise AppbuilderBuildexException(f'请检查{self.component}组件是否存在成员变量manifests或manifests成员变量定义规范, 错误信息：{e}')

    def test_tool_eval_input(self):
        """
        校验tool_eval的传入参数是否合法。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            AppbuilderBuildexException: 校验不通过时抛出异常。
        
        """
        if not self.tool_eval_input.get('streaming',None):
            raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的传入参数是否定义streaming')
        if hasattr(self.component, '__module__'):
            module_name = self.component.__module__
            if re.match(r'appbuilder\.', module_name):
                if not self.tool_eval_input.get('traceid',None):
                    raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的传入参数是否有traceid')
        try:
            manifests = self.component.manifests[0]
            parameters = manifests['parameters']
            properties = parameters['properties']
        except:
            raise AppbuilderBuildexException(f'请检查{self.component}组件是否存在成员变量manifests或manifests成员变量定义规范')
        anyOf = parameters.get('anyOf',None)
        if anyOf:
            anyOf_test = False
            for anyOf_requried_dict in anyOf:
                anyOf_requried = anyOf_requried_dict.get('required',None)
                if anyOf_requried:
                    success_number = 0
                    for anyOf_requried_data in anyOf_requried:
                        try:
                            input_data = self.tool_eval_input[anyOf_requried_data]
                            input_data_type = Data_Type[properties[anyOf_requried_data]['type']]
                            if anyOf_requried_data in self.tool_eval_input and isinstance(input_data, input_data_type):
                                success_number += 1
                        except:
                            pass  
                    if success_number == len(anyOf_requried):
                        anyOf_test = True
            if not anyOf_test:
                raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的传入参数是否正确或manifests的参数定义是否正确')
                            
        if not anyOf:
            un_anyOf_test = False
            requried = parameters.get('required',None)
            if requried:
                success_number = 0
                for requried_data in requried:
                    try:
                        input_data = self.tool_eval_input[requried_data]
                        input_data_type = Data_Type[properties[requried_data]['type']]
                        if requried_data in self.tool_eval_input and isinstance(input_data, input_data_type):
                            success_number += 1
                    except:
                        pass 
                if success_number == len(requried):
                    un_anyOf_test = True
            if not un_anyOf_test:
                raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的传入参数是否正确或manifests的参数定义是否正确')
           
    def test_tool_eval_reponse_raise(self):
        """
        Args:
            无参数
        
        Returns:
            无返回值
        
        Raises:
            AppbuilderBuildexException: 如果响应头状态码对应的异常类型与捕获到的异常类型不一致，则抛出此异常。
        
        功能：测试tool_eval方法在不同响应头状态码下的异常抛出情况。
        
        首先，设置响应头状态码为bad_request，并模拟InnerSession.post方法的返回值。
        然后，定义一个状态码与异常类型的映射字典test_status_code_dict，用于测试不同状态码下抛出的异常类型是否正确。
        接着，遍历test_status_code_dict字典，将状态码和异常类型分别赋值给self.response.status_code和error变量，并重新模拟InnerSession.post方法的返回值。
        在每次循环中，调用self.component.tool_eval方法，并捕获可能抛出的异常。
        如果捕获到的异常类型与test_status_code_dict字典中对应状态码的异常类型一致，则继续下一次循环；
        否则，抛出AppbuilderBuildexException异常，提示用户检查self.component组件tool_eval方法的response返回值是否添加了check_response_header检测。
        """
        # test_response_head_status
        self.response.status_code = requests.codes.bad_request
        InnerSession.post = Mock(return_value=self.response)
        test_status_code_dict = {
            requests.codes.bad_request: BadRequestException, 
            requests.codes.forbidden: ForbiddenException, 
            requests.codes.not_found: ForbiddenException, 
            requests.codes.precondition_required: PreconditionFailedException, 
            requests.codes.internal_server_error: InternalServerErrorException
                                 }
        for status_code,error in test_status_code_dict.items():
            self.response.status_code = status_code
            InnerSession.post = Mock(return_value=self.response)
            try:
                self.component.tool_eval(**self.tool_eval_input)
            except Exception as e:
                if isinstance(e,error):
                    raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的response返回值是否添加check_response_header检测')
    
    def test_tool_eval_generator(self):
        """
        测试组件tool_eval方法返回是否为生成器
        
        Args:
            无
        
        Returns:
            无
        
        Raises:
            AppbuilderBuildexException: 如果组件tool_eval的返回值不为生成器时抛出异常
        """
        self.response.status_code = requests.codes.ok
        InnerSession.post = Mock(return_value=self.response)
        result_generator = self.component.tool_eval(**self.tool_eval_input)
        if not result_generator:
            raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的返回值是否为生成器')
        if not isinstance(result_generator, types.GeneratorType):
            raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的返回值是否为生成器')
        
    def test_tool_eval_text_str(self):
        """
        测试tool_eval方法返回值的文本是否为字符串类型
        
        Args:
            无
        
        Returns:
            无返回值，该函数主要进行断言测试
        
        Raises:
            AppbuilderBuildexException: 当tool_eval方法返回的文本不是字符串类型时抛出异常
        """
        self.response.status_code = requests.codes.ok
        InnerSession.post = Mock(return_value=self.response)
        result_generator = self.component.tool_eval(**self.tool_eval_input)
        for res in result_generator:
            if not isinstance(res.get("text",""),str):
                raise AppbuilderBuildexException(f'请检查{self.component}组件tool_eval的返回值是否为字符串')

class AutomaticTestToolEval:
    def __init__(self, appbuilder_components:components):
        self.components = appbuilder_components
        self.test_input()

    def test_input(self):
        manifest = self.components.manifests[0]
        properties = manifest['parameters']['properties']
        required_params = []
        anyOf = manifest['parameters'].get('anyOf', None)
        if anyOf:
            for anyOf_dict in anyOf:
                required_params += anyOf_dict['required']
        if not anyOf:
            required_params += manifest['parameters']['required']
        required_param_dict = {
            'name':str,
            'streaming':bool
        }

        for param in required_params:
            required_param_dict[param] = Data_Type[properties[param]['type']]
        required_params = []
        for param in required_param_dict.keys():
            required_params.append(param)

        # 交互检查
        tool_eval_input_params = []
        signature = inspect.signature(self.components.tool_eval)
        for param_name, param in signature.parameters.items():
            if param_name == 'kwargs':
                continue
            if param_name in required_params:
                if required_param_dict[param_name] == param.annotation:
                    tool_eval_input_params.append(param_name)
                else:
                    raise AppbuilderBuildexException(f'请检查tool_eval的传入参数{param_name}是否符合成员变量manifest的参数类型要求')
            else:
                raise AppbuilderBuildexException(f'请检查tool_eval的传入参数{param_name}是否在成员变量manifest要求内')

        for required_param in required_params:
            if required_param not in tool_eval_input_params:
                raise AppbuilderBuildexException(f'请检查成员变量manifest要求的tool_eval的传入参数{required_param}是否在其中')
            
    
        