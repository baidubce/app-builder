# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""include HTTP and backend server exception.
"""

def _check_error_message(message):
    if message.startswith('Traceback ') or message.startswith("\n  File "):
        return True

class BaseRPCException(Exception):
    r"""Base RPC exception.
    """
    pass

class BadRequestException(BaseRPCException):
    """ 
    BadRequestException代表一个HTTP 400 Bad Request错误。
    当服务器因检测到某些客户端错误而无法或不会处理请求时，应抛出此异常。
    这些错误可能包括请求语法格式错误、请求参数无效，或请求中存在其他导致无法成功处理的问题。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"Bad Request"。
        """
        self.message = message
        super().__init__(message)
        
    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息、HTTP状态和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\nHTTP状态码(HTTP Code): 400"
                f"\n解决方案(Solution for error): 请检查您的输入参数是否正确，若问题仍然存在，请联系Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")
    
class ForbiddenException(BaseRPCException):
    """
    ForbiddenException代表一个HTTP 403 Forbidden错误。
    当服务器理解请求但是拒绝执行时，应抛出此异常。
    这通常是因为用户没有足够的权限访问资源，或者尽管请求者的身份验证成功，但是被访问的资源拒绝让他访问。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"No Error Message"。
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息、HTTP状态和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\nHTTP状态码(HTTP Code): 403"
                f"\n解决方案(Solution for error): 请确认您是否有权限访问请求的资源。"
                f"如果您认为这是一个错误，请联系系统管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")


class NotFoundException(BaseRPCException):
    """
    NotFoundException代表一个HTTP 404 Not Found错误。
    当服务器找不到请求的资源时，应抛出此异常。
    这可能是因为请求的资源不存在或不可用，或者URL输入错误。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"No Error Message"。
        
        Returns:
            无
        
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息、HTTP状态和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\nHTTP状态码(HTTP Code): 404"
                f"\n解决方案(Solution for error): 请检查URL是否输入正确，确认资源是否存在或已被移动。尝试更新SDK版本"
                f"若问题仍然存在，请联系网站管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")


class PreconditionFailedException(BaseRPCException):
    """
    PreconditionFailedException代表一个HTTP 412 Precondition Failed错误。
    当服务器未能满足请求中在请求头字段中给定的其中一个前提条件时，应抛出此异常。
    这通常意味着客户端提供的前置条件错误，或者资源的状态与前置条件不符。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"Precondition Failed"。
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息、HTTP状态和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\nHTTP状态码(HTTP Code): 412"
                f"\n解决方案(Solution for error): 请检查请求头中的前提条件是否设置正确，并确保目标资源的状态符合这些条件。"
                f"如果您认为这是一个错误，请联系网站管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")


class InternalServerErrorException(BaseRPCException):
    """
    InternalServerErrorException代表一个HTTP 500 Internal Server Error错误。
    当服务器遇到了一个阻止它完成请求的意外情况时，应抛出此异常。
    这种错误通常意味着服务器端存在代码或配置上的问题。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化方法。
        
        Args:
            message (str, optional): 错误信息。默认为 "No Error Message"。
        
        Returns:
            None
        
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息、HTTP状态和解决方案的格式化字符串。
        """
        if _check_error_message(self.message):
            return self.message
        # 使用分隔线和缩进增加可读性
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\nHTTP状态码(HTTP Code): 500"
                f"\n解决方案(Solution for error): 请检查服务器日志以确定问题原因，可能需要进行代码调试或服务器配置更正。如果问题持续存在，"
                f"请联系网站管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")


class HTTPConnectionException(BaseRPCException):
    """
    HTTPConnectionException代表一个HTTP连接错误。
    当客户端尝试与服务器建立连接时发生错误，应抛出此异常。
    这种错误可能由于网络问题、服务器宕机或配置错误导致。
    """
    def __init__(self, message="No Error Message"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"HTTP Connection Error"。
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息和解决方案的格式化字符串。
        """
        if _check_error_message(self.message):
            return self.message
        # 使用分隔线和缩进增加可读性
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): 请检查网络连接是否正常，确保您可以访问服务器。如果网络无问题，"
                f"请确认服务器状态是否正常运行，以及是否存在配置问题"
                f"{error_separator}")


class ModelNotSupportedException(BaseRPCException):
    """
    ModelNotSupportedException代表尝试使用的模型不被支持。
    当客户端请求一个尚未实现或不兼容的模型时，应抛出此异常。
    这种错误通常意味着客户端需要更新或更换模型。
    """
    def __init__(self, message="Model Not Supported"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"Model Not Supported"。
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): 请检查选择的模型是否符合要求:"
                f"\n- 调用的组件是否支持你选择的模型"
                f"\n- 使用appbuilder.get_model_list()查看当前支持的模型列表"
                f"{error_separator}")


class TypeNotSupportedException(BaseRPCException):
    """
    TypeNotSupportedException代表一个不被支持的类型异常。
    当传递了不在预期范围内的类型参数时，应抛出此异常。
    这种错误通常意味着调用者需要修正参数以匹配支持的类型。
    """
    def __init__(self, message="Type Not Supported"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"Type Not Supported"。
        """
        self.message = message
        self.api_type_set = {"chat", "completions", "embeddings", "text2image"}
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息和解决方案的格式化字符串。
        """
        # 使用分隔线和缩进增加可读性
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): 请检查您提供的类型参数是否正确。"
                f"您应该只使用下列支持的类型：{self.api_type_set}。请修改参数以匹配支持的类型，并再次尝试调用。"
                f"{error_separator}")


class AppBuilderServerException(BaseRPCException):
    r"""AppBuilderServerException represent backend server failed response.
    """
    description: str = "No Error Message"
    code: int = 500

    def __init__(self, request_id="", code="", message="", service_err_code="", service_err_message=""):
        self.description = "request_id={}, code={}, message={}, service_err_code={}, service_err_message={} ".format(
            request_id, code, message, service_err_code, service_err_message)
        self.code = code if code else self.code

    def __str__(self):
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.description}"
                f"\nCode:{self.code}"
                f"\n解决方案(Solution for error): Assistant服务端问题，请联系网站管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")

class AssistantServerException(BaseRPCException):
    r"""AssistantSercerException represent assistant server failed response.
    """
    description: str = "No Error Message"
    code: int = 500

    def __init__(self, request_id= "", code="", message="", type="", params=""):
        """
        初始化方法，用于初始化对象。
        
        Args:
            request_id (str, optional): 请求ID，默认为空字符串。
            code (str, optional): 状态码，默认为空字符串。
            message (str, optional): 消息内容，默认为空字符串。
            type (str, optional): 类型，默认为空字符串。
            params (str, optional): 参数，默认为空字符串。
        
        Returns:
            None
        """
        self.description = "request_id={}, code={}, message={}, type={}, params={} ".format(
            request_id, code, message, type, params)
        self.code = code if code else self.code

    def __str__(self):
        """
        将错误信息格式化为字符串形式返回。
        
        Args:
            无
        
        Returns:
            str: 格式化后的错误信息字符串，包含错误描述、错误代码和解决方案。
        
        """
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.description}"
                f"\nCode:{self.code}"
                f"\n解决方案(Solution for error): Appbuilder-Assistant服务端问题，请联系网站管理员或Appbuilder工作人员，并提供request_id以便我们查看并帮助您解决错误原因"
                f"{error_separator}")


class InvalidRequestArgumentError(BaseRPCException):
    """
    InvalidRequestArgumentError 表示在RPC调用中一个无效的请求参数错误。
    当RPC请求的参数无效、缺失或者不符合预期的格式时，应抛出此异常。
    这种错误通常意味着调用者需要检查并修正提供的参数。
    """
    def __init__(self, message="Invalid request argument"):
        """
        初始化异常类。
        
        Args:
            message (str, optional): 异常信息，默认为"Invalid request argument"。
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        """
        返回该对象的字符串表示形式。
        
        Returns:
            str: 返回包含错误消息和建议解决方案的格式化字符串。
        """
        if _check_error_message(self.message):
            return self.message
        # 使用分隔线和缩进增加可读性
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): 请检查是否未设置文件名或指定文件名对应的URL不存在"
                f"{error_separator}")


class RiskInputException(BaseRPCException):
    r"""RiskInputException
    """
    pass


class AppbuilderBuildexException(BaseRPCException):
    """
    Appbuilder组件规范化检测报错异常，说明组件开发者未按照规范进行开发，导致单元测试流水线检测过程出现错误
    """
    def __init__(self, message="No Error Message"):
        """
        初始化错误类实例。
        
        Args:
            message (str, optional): 错误消息，默认为 "No Error Message"。
        
        """
        self.message = message
        self.components_docs_url = "待更新"
        super().__init__(message)
    
    def __str__(self):
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): 组件开发者未按照规范进行开发，导致单元测试流水线检测过程出现错误，"
                f"请联系Appbuilder团队或查看:{self.components_docs_url},按照规范进行开发"
                f"{error_separator}")


class AppbuilderTraceException(BaseRPCException):
    """
    Appbuilder SDK Trace功能异常
    """
    def __init__(self, message="No Error Message"):
        """
        初始化错误类实例。
        
        Args:
            message (str, optional): 错误消息，默认为 "No Error Message"。
        
        """
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        """
        返回错误信息的字符串表示。
        
        Args:
            无
        
        Returns:
            str: 包含错误信息和解决方案的字符串。
        
        """
        if _check_error_message(self.message):
            return self.message
        error_separator = "\n" + "-" * 100 
        return (f"{error_separator}"
                f"\n错误信息(Error Message): {self.message}"
                f"\n解决方案(Solution for error): Appbuilder SDK Trace功能异常，开发者可控制台输入 export APPBUILDER_TRACE_DEBUG=True 查看Appbuilder SDK Trace功能完整报错链路并调试"
                f"{error_separator}")