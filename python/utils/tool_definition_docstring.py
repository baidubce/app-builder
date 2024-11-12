# -*- coding: UTF-8 -*-
"""FunctionView classes."""

import re
from enum import Enum
from textwrap import dedent
from typing import Tuple

# TODO: support using docstring for function & parameter description
# https://github.com/ju-bezdek/langchain-decorators/blob/main/src/langchain_decorators/function_decorator.py

NoneType = type(None)

# Validation regexes
FUNCTION_NAME_REGEX = r"^[0-9A-Za-z_]*$"
FUNCTION_PARAM_NAME_REGEX = r"^[0-9A-Za-z_]*$"


class DocstringsFormat(Enum):
    """Python docstring format."""

    AUTO = "auto"
    GOOGLE = "google"
    # https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
    SPHINX = "sphinx"
    NUMPY = "numpy"


def _get_function_docs(func: callable) -> Tuple:
    if not func.__doc__:
        return None

    return _parse_function_doc(func.__doc__)


def get_docstring_view(func, format, disable_docstring):
    """Extract function metadata from docstring."""

    docstring = _get_function_docs(func)
    if docstring is None or disable_docstring:
        doc_params = {}
        doc_returns = {}
    else:
        doc_params, doc_returns = _find_and_parse_params_from_docstrings(docstring, format)

    return doc_params, doc_returns


def _parse_function_doc(docstring: str) -> Tuple:
    fist_line, rest = docstring.split("\n", 1) if "\n" in docstring else (docstring, "")
    # we dedent the first line separately,because its common that it often starts right after """
    fist_line = fist_line.strip()
    if fist_line:
        fist_line += "\n"
    docs = fist_line + dedent(rest)
    return docs


def _parse_function_description_from_docstrings(docstring: str) -> str:
    # we will return first text until first empty line
    if docstring is None:
        return None

    lines = docstring.splitlines()
    description = []
    for line in lines:
        line = line.strip()
        if line:
            description.append(line)
        elif description:
            # if we have already some description, we stop at first empty line ... else continue
            break
    return "\n".join(description)


def _find_and_parse_params_from_docstrings(docstring: str, format: DocstringsFormat) -> str:
    """
    Find Args section in docstring.
    """

    if format == DocstringsFormat.AUTO or format == DocstringsFormat.GOOGLE:
        # auto here means more more free format than google
        args_section_start_regex_pattern = r"(^|\n)(Args|Arguments|Parameters)\s*:?\s*\n"
        args_section_end_regex_pattern = r"(^|\n)([A-Z][a-z]+)\s*:?\s*\n"
        returns_section_start_pattern = r"(^|\n)(Returns|Ret)\s*:?\s*\n"
        return_param_start_parser_regex = r"(^|\n)\s+(?P<type>[^\)]*)\s*:\s*(?=[^\n]+)"
        if format == DocstringsFormat.GOOGLE:
            param_start_parser_regex = (
                r"(^|\n)\s+(?P<name>[\*]{0,2}[a-zA-Z_][a-zA-Z0-9_]*)\s*(\((?P<type>[^\)]*)\))?\s*:\s*(?=[^\n]+)"
            )
        else:
            param_start_parser_regex = (
                r"(^|\n)\s+(?P<name>[\*]{0,2}[a-zA-Z_][a-zA-Z0-9_]*)\s*(\((?P<type>[^\)]*)\))?\s*(-|:)\s*(?=[^\n]+)"
            )
    elif format == DocstringsFormat.NUMPY:
        args_section_start_regex_pattern = r"(^|\n)(Args|Arguments|Parameters)\s*\n\s*---+\s*\n"
        args_section_end_regex_pattern = r"(^|\n)([A-Z][a-z]+)\s*\n\s*---+\s*\n"
        param_start_parser_regex = (
            r"(^|\n)\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)(\s*:\s*(?P<type>[^\)]*)\s*)?\n\s+(?=[^\n]+)"
        )
    elif format == DocstringsFormat.SPHINX:
        args_section_start_regex_pattern = None  # we will look for :param everywhere
        args_section_end_regex_pattern = r"(\n)\s*:[a-z]"
        param_start_parser_regex = (
            r"(^|\n)\s*:param\s+(?P<type>[^\)]*)\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(?=[^\n]+)"
        )

    params = _parse_params(
        docstring,
        args_section_start_regex_pattern,
        args_section_end_regex_pattern,
        param_start_parser_regex,
        has_name=True,
    )

    returns_param_name = "default"
    returns = _parse_params(
        docstring,
        returns_section_start_pattern,
        args_section_end_regex_pattern,
        return_param_start_parser_regex,
        has_name=False,
        param_name=returns_param_name,
    )

    if not params and format == DocstringsFormat.AUTO:
        # try other options
        options = [DocstringsFormat.NUMPY, DocstringsFormat.SPHINX]
        for option in options:
            params, returns = _find_and_parse_params_from_docstrings(docstring, option)
            if params:
                return params, returns[returns_param_name] if returns_param_name in returns else {}
    else:
        return params, returns[returns_param_name] if returns_param_name in returns else {}


def _parse_params(
    docstring,
    args_section_start_regex_pattern,
    args_section_end_regex_pattern,
    param_start_parser_regex,
    has_name=True,
    param_name="default",
):
    optional_pattern = r",\s+optional\s*"
    args_section = None
    args_section_start = 0
    args_section_end = None

    if args_section_start_regex_pattern:
        match = re.search(args_section_start_regex_pattern, docstring)
        if match:
            args_section_start = match.end()
            if args_section_end_regex_pattern:
                match = re.search(args_section_end_regex_pattern, docstring[args_section_start:])
                if match:
                    args_section_end = match.start() + args_section_start
            if not args_section_end:
                args_section_end = len(docstring)
            args_section = docstring[args_section_start:args_section_end]
        else:
            args_section = None
    else:
        args_section = docstring

    params = {}
    if args_section:
        last_param = None
        last_param_end = None
        for param_start_match in re.finditer(param_start_parser_regex, args_section):
            if last_param_end is not None:
                last_param["description"] = args_section[last_param_end : param_start_match.start()].strip()

            param_name = param_start_match.group("name") if has_name else param_name
            param_name = param_name.lstrip("*")

            param_type = param_start_match.group("type")
            param_required = True
            if param_type and re.search(optional_pattern, param_type):
                param_required = False
                param_type = re.sub(optional_pattern, "", param_type).strip()
            last_param = {"type": param_type or "", "description": None, "required": param_required}
            last_param_end = param_start_match.end()
            params[param_name] = last_param

        if last_param_end is not None:
            section_end = None
            if args_section_start_regex_pattern is None and args_section_end_regex_pattern:
                # this is handling SPHINX, we didnt parse the start so we cant parse the end until all the params are consumed... now we can parse the end after the last param
                section_end_match = re.search(args_section_end_regex_pattern, docstring[last_param_end:])
                if section_end_match:
                    section_end = last_param_end + section_end_match.start()
            if not section_end:
                section_end = len(docstring)
            last_param["description"] = args_section[last_param_end:section_end].strip()
    return params
