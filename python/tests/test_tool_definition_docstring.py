# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
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
import os
import unittest
from typing import Any, Dict, List, Optional, Callable

from appbuilder.utils.tool_definition_docstring import (
    get_docstring_view,
    _parse_function_doc,
    _parse_function_description_from_docstrings,
    _find_and_parse_params_from_docstrings,
    _get_function_docs,
    _parse_params,
    DocstringsFormat
)

@unittest.skipUnless(os.getenv("TEST_CASE", "UNKNOWN") == "CPU_PARALLEL", "")
class TestToolDefinitionDocstring(unittest.TestCase):
    def test_google_style(self):
        # Generated by vscode plugin
        # https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring
        def google_style(
            name: str,
            /,
            *args,
            val: str = None,
            val_obj: Optional[Any] = None,
            val_list: List[str] = None,
            data: Dict[str, int] = None,
            **kwargs,
        ) -> str:
            """Google style docstring.

            Args:
                name (str): Name of object.
                *args: Variable length argument list.
                val (str, optional): Value of obj. Defaults to None.
                val_obj (Optional[Any], optional): Real object reference. Defaults to None.
                val_list (List[str], optional): List of items with object. Defaults to None.
                data (Dict[str, int], optional): Data along with object. Defaults to None.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                str: Styled string.
            """
            return ""

        doc = _get_function_docs(google_style)
        params, returns = _find_and_parse_params_from_docstrings(docstring=doc, format=DocstringsFormat.GOOGLE)

        assert params
        assert params["name"]
        assert params["name"]["type"] == "str"
        assert params["name"]["description"] == "Name of object."
        assert params["name"]["required"] is True
        assert params["args"]
        assert params["args"]["type"] == ""
        assert params["args"]["description"] == "Variable length argument list."
        assert params["args"]["required"] is True
        assert params["val"]
        assert params["val"]["type"] == "str"
        assert params["val"]["description"] == "Value of obj. Defaults to None."
        assert params["val"]["required"] is False
        assert params["val_obj"]
        assert params["val_obj"]["type"] == "Optional[Any]"
        assert params["val_obj"]["description"] == "Real object reference. Defaults to None."
        assert params["val_obj"]["required"] is False
        assert params["val_list"]
        assert params["val_list"]["type"] == "List[str]"
        assert params["val_list"]["description"] == "List of items with object. Defaults to None."
        assert params["val_list"]["required"] is False
        assert params["data"]
        assert params["data"]["type"] == "Dict[str, int]"
        assert params["data"]["description"] == "Data along with object. Defaults to None."
        assert params["data"]["required"] is False
        assert params["kwargs"]
        assert params["kwargs"]["type"] == ""
        assert params["kwargs"]["description"] == "Arbitrary keyword arguments."
        assert params["kwargs"]["required"] is True
        assert returns
        assert returns["type"] == "str"
        assert returns["description"] == "Styled string."
        assert returns["required"] is True


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

        doc = _get_function_docs(func)
        params, returns = _find_and_parse_params_from_docstrings(docstring=doc, format=DocstringsFormat.GOOGLE)

        assert params
        assert params["val"]
        assert params["val"]["type"] == "str"
        assert params["val"]["description"] == "Value of obj. Defaults to None."
        assert params["val"]["required"] is False
        assert returns
        assert returns["type"] == "Dict[str, str]"
        assert returns["description"] == "Returns a dict."
        assert returns["required"] is True


    def test_google_style_no_return(self):
        def func(
            name: str,
        ):
            """Google style docstring.

            Args:
                name (str): Name of object.

            """
            return ""

        doc = _get_function_docs(func)
        params, returns = _find_and_parse_params_from_docstrings(docstring=doc, format=DocstringsFormat.GOOGLE)

        assert params
        assert params["name"]
        assert params["name"]["type"] == "str"
        assert params["name"]["description"] == "Name of object."
        assert params["name"]["required"] is True
        assert returns == {}


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

        doc = _get_function_docs(func)
        params, returns = _find_and_parse_params_from_docstrings(docstring=doc, format=DocstringsFormat.GOOGLE)

        assert params == {}
        assert returns == {}


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

        doc = _get_function_docs(func)

        assert doc is None
        
if __name__ == '__main__':
    unittest.main()