from appbuilder.core.manifest.models import Manifest, ParametersModel, PropertyModel
from appbuilder.core.manifest.manifest_signature import get_signature
from appbuilder.core.manifest.manifest_decorator import ManifestView

def function_to_manifest(func) -> Manifest:
    """
    利用 manifest_signature.py 提供的 get_signature 方法解析函数的签名和参数信息，
    并生成一个 Manifest 实例。

    Args:
        func: 要转换的函数。

    Returns:
        Manifest: 包含函数元信息的模型。
    """
    if func.__doc__ is None:
        raise ValueError(f"函数 {func.__name__} 缺少文档字符串")

    # 使用 manifest_signature 提取函数签名信息
    sig_params, sig_returns = get_signature(func)

    # 构造参数模型
    properties = {}
    required = []

    for param in sig_params:
        param_info = {
            "type": param.get("type_", None),  # 类型
            "description": param.get("description", None),  # 描述
        }

        # 验证类型字段是否有有效值
        if not param_info["type"]:
            raise ValueError(f"参数 '{param['name']}' 缺少类型信息，请在函数签名中指定类型。")

        # 构造 PropertyModel
        properties[param["name"]] = PropertyModel(**param_info)

        # 记录必需参数
        if param.get("required", False):
            required.append(param["name"])

    # 构造返回值描述
    return_info = {
        "type": sig_returns.get("type_", None),
        "description": sig_returns.get("description", None),
    }

    # 构造 ParametersModel
    parameters_model = ParametersModel(
        type="object",
        properties=properties,
        required=required,
    )

    # 构造 Manifest 对象
    function_manifest = Manifest(
        type="function",
        function={
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": parameters_model.model_dump(),
            "returns": return_info,
        },
    )

    return function_manifest

def decorator_to_manifest(manifest_view:ManifestView) -> Manifest:
    """
    将经过装饰器函数处理后带有函数元信息的 BaseModel 对象转换为 Manifest对象。
    
    Args:
        manifest_view (ManifestView): 装饰器处理后得到的ManifestView类型数据
    
    Returns:
        Manifest: 函数模型对象。
    
    Raises:
        ValueError: 如果函数视图的参数缺少类型信息或函数缺少描述，则引发 ValueError 异常。
    
    """
    # 提取参数信息
    parameters = {}
    required_fields = []

    for param in manifest_view.parameters:
        # 验证类型字段是否有有效值
        if not param.type_:
            raise ValueError(f"参数 '{param.name}' 缺少类型信息，请在函数签名中指定类型。")

        # 定义每个参数的属性模型
        parameters[param.name] = PropertyModel(
            type=param.type_,
            description=param.description
        )
        # 检查参数是否是必填项
        if param.required:
            required_fields.append(param.name)

    # 创建 ParametersModel
    parameters_model = ParametersModel(
        type="object",
        properties=parameters,
        required=required_fields
    )
    if not manifest_view.description:
        raise ValueError(f"函数 {manifest_view.name} 缺少描述")
    
    # 构建 Manifest 对象
    function_manifest = Manifest(
        type="function",
        function={
            "name": manifest_view.name,
            "description": manifest_view.description,
            "parameters": parameters_model.dict(),  # 转换为字典格式
            "returns": {
                "type": manifest_view.returns[0].type_,
                "description": manifest_view.returns[0].description
            }
        }
    )

    return function_manifest
