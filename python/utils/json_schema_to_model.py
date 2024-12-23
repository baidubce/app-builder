import importlib.util
import json
import re
import sys
import copy
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import ModuleType

from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from pydantic import BaseModel


NON_ALPHANUMERIC = re.compile(r"[^a-zA-Z0-9]+")
STARTS_WITH_NUMBER = re.compile(r'[0-9]+')
UPPER_CAMEL_CASE = re.compile(r"[A-Z][a-zA-Z0-9]+")
LOWER_CAMEL_CASE = re.compile(r"[a-z][a-zA-Z0-9]+")

class BadJsonSchema(Exception):
    pass


def _to_camel_case(name: str) -> str:
    if any(NON_ALPHANUMERIC.finditer(name)):
        return  "".join(term.lower().title() if not STARTS_WITH_NUMBER.match(term) else term.lower() for term in NON_ALPHANUMERIC.split(name))
    if UPPER_CAMEL_CASE.match(name):
        return name
    if LOWER_CAMEL_CASE.match(name):
        return name[0].upper() + name[1:]
    raise BadJsonSchema(f"Unknown case used for {name}")


def _load_module_from_file(file_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        name=file_path.stem, location=str(file_path)
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_path.stem] = module
    spec.loader.exec_module(module)
    return module


@contextmanager
def _delete_file_on_completion(file_path: Path):
    try:
        yield
    finally:
        file_path.unlink(missing_ok=True)

def replace_last_match(text, pattern, repl):
    # 使用正则表达式查找所有匹配的子字符串
    matches = list(re.finditer(pattern, text))
    
    # 如果没有找到匹配的子字符串，直接返回原始文本
    if not matches:
        return text
    
    # 找到最后一个匹配的子字符串的位置和长度
    last_match = matches[-1]
    start, end = last_match.span()
    
    # 替换最后一个匹配的子字符串
    before = text[:start]
    after = text[end:]
    new_text = before + repl + after
    
    return new_text

def sed_pydantic_str(pydantic_models_as_str:str, title: str):
    # 在 "from pydantic import BaseModel, Field" 这行后，添加 "from pydantic import RootModel"
    new_pydantic_models_as_str = re.sub(r'from pydantic import BaseModel, Field',
                                        'from pydantic import BaseModel; from pydantic import Field, RootModel',
                                        pydantic_models_as_str)
    # 判断字符串中是否存在"__root__"
    has_root = "__root__" in new_pydantic_models_as_str
    if has_root:
        # 把最后一个的BaseModel替换为RootModel
        new_pydantic_models_as_str = replace_last_match(new_pydantic_models_as_str, "BaseModel", "RootModel")

        # 替换 __root__ 为 root
        new_pydantic_models_as_str = re.sub(r'\b__root__\b', r'root', new_pydantic_models_as_str)
    return new_pydantic_models_as_str


def json_schema_to_pydantic_model(json_schema: dict, name_override: str) -> BaseModel:
    json_schema_as_str = json.dumps(json_schema)
    pydantic_models_as_str: str = JsonSchemaParser(json_schema_as_str).parse()

    class_title = json_schema["title"]
    pydantic_models_as_str = sed_pydantic_str(pydantic_models_as_str, class_title)
    pydantic_models_as_str = pydantic_models_as_str.replace("unique_items", "Set")
    
    with NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        temp_file_path = Path(temp_file.name).resolve()
        temp_file.write(pydantic_models_as_str.encode())

    with _delete_file_on_completion(file_path=temp_file_path):
        module = _load_module_from_file(file_path=temp_file_path)

    main_model_name = _to_camel_case(name=class_title)
    pydantic_model: BaseModel = module.__dict__[main_model_name]
    # Override the pydantic model/parser name for nicer ValidationError messaging and logging
    pydantic_model.__name__ = name_override
    pydantic_model.parse_obj.__func__.__name__ = name_override
    return pydantic_model

if __name__ == '__main__':
    manifests = [
        {
            "name": "general_ocr",
            "description": "提供更高精度的通用文字识别能力，能够识别图片中的文字，不支持html后缀文件的输入",
            "parameters": {
                "type": "object",
                "properties": {
                    "img_url": {
                        "type": "string",
                        "description": "待识别图片的url,根据该url能够获取图片"
                    },
                    "img_name": {
                        "type": "string",
                        "description": "待识别图片的文件名,用于生成图片url"
                    },
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "uniqueItems": True
                    }
                    
                },
                "anyOf": [
                    {
                        "required": [
                            "img_url"
                        ]
                    },
                    {
                        "required": [
                            "img_name"
                        ]
                    }
                ]
            }
        }
    ]
    schema = copy.deepcopy(manifests[0]['parameters'])
    schema['title'] = "general_ocr"
    model = json_schema_to_pydantic_model(json_schema=schema, name_override="GeneralOcr")
    print(model)
    print(model.schema_json())