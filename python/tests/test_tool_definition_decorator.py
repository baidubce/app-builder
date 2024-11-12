from appbuilder import FunctionView, function, function_parameter, function_return


def test_disable_docstring():
    @function(description="anotated function", disable_docstring=True)
    @function_parameter(name="param", description="a parameter", type="str", default_value="default_val")
    @function_return(description="a result", default_value="default_result")
    def func(param: str) -> str:
        return param

    view = func.__pf_function__

    assert isinstance(view, FunctionView)
    assert view.name == "func"
    assert view.description == "anotated function"
    assert view.is_async is False
    assert view.is_stream is False

    assert view.parameters[0].name == "param"
    assert view.parameters[0].description == "a parameter"
    assert view.parameters[0].default_value == "default_val"
    assert view.parameters[0].type_ == "str"
    assert view.parameters[0].required is True
    assert view.parameters[0].example is None

    assert view.returns[0].name == "return"
    assert view.returns[0].description == "a result"
    assert view.returns[0].default_value == "default_result"
    assert view.returns[0].type_ == "str"
    assert view.returns[0].required is True
    assert view.returns[0].example is None


def test_combine():
    @function()
    @function_parameter(name="param", example="[1,2,3]")
    @function_return(description="Sum of param as list of number without odds.", example="6")
    def func(param: str = "[]") -> int:
        """An example function.

        Args:
            param (str): A list of numbers.

        Returns:
            int: The sum of parameter.
        """
        return param

    view = func.__pf_function__

    assert isinstance(view, FunctionView)
    assert view.name == "func"
    assert view.description == "An example function."
    assert view.is_async is False
    assert view.is_stream is False

    assert view.parameters[0].name == "param"
    assert view.parameters[0].description == "A list of numbers."
    assert view.parameters[0].default_value == "[]"
    assert view.parameters[0].type_ == "str"
    assert view.parameters[0].required is False
    assert view.parameters[0].example == "[1,2,3]"

    assert view.returns[0].name == "return"
    assert view.returns[0].description == "Sum of param as list of number without odds."
    assert view.returns[0].default_value is None
    assert view.returns[0].type_ == "int"
    assert view.returns[0].required is True
    assert view.returns[0].example == "6"


def test_reversed_decorators():
    @function_parameter(name="param", example="[1,2,3]", description="DECORATOR A list of numbers.")
    @function_return(description="DECORATOR The sum of parameter.", example="6")
    @function()
    def func(param: str = "[]") -> int:
        """An example function.

        Args:
            param (str): A list of numbers.

        Returns:
            int: The sum of parameter.
        """
        return param

    view = func.__pf_function__

    assert isinstance(view, FunctionView)
    assert view.name == "func"
    assert view.description == "An example function."
    assert view.is_async is False
    assert view.is_stream is False

    assert view.parameters[0].name == "param"
    assert view.parameters[0].description == "DECORATOR A list of numbers."
    assert view.parameters[0].default_value == "[]"
    assert view.parameters[0].type_ == "str"
    assert view.parameters[0].required is False
    assert view.parameters[0].example == "[1,2,3]"

    assert view.returns[0].name == "return"
    assert view.returns[0].description == "DECORATOR The sum of parameter."
    assert view.returns[0].default_value is None
    assert view.returns[0].type_ == "int"
    assert view.returns[0].required is True
    assert view.returns[0].example == "6"


def test_only_function_decorator():
    @function()
    def func(param: str = "[]") -> int:
        return param

    view = func.__pf_function__

    assert isinstance(view, FunctionView)
    assert view.name == "func"
    assert view.description is None
    assert view.is_async is False
    assert view.is_stream is False

    assert view.parameters[0].name == "param"
    assert view.parameters[0].description is None
    assert view.parameters[0].default_value == "[]"
    assert view.parameters[0].type_ == "str"
    assert view.parameters[0].required is False
    assert view.parameters[0].example is None

    assert view.returns[0].name == "return"
    assert view.returns[0].description is None
    assert view.returns[0].default_value is None
    assert view.returns[0].type_ == "int"
    assert view.returns[0].required is True
    assert view.returns[0].example is None
