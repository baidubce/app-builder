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