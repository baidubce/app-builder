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


"""
Setup script.

Authors: dongdaxiang(dongdaxiang@baidu.com)
Date:    2023/12/01 11:19:24
"""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = find_packages()
package_data = {}
for package in packages:
    if package.startswith('appbuilder.utils'):
        package_data[package] = ["*.md"]

setup(
    name="appbuilder-sdk",
    # NOTE(chengmo): 修改此版本号时，请注意同时修改 __init__.py 中的 __version__
    version="0.9.0",
    author="dongdaxiang",
    author_email="dongdaxiang@baidu.com",
    packages=packages,
    package_data=package_data,
    install_requires=requirements,
    python_requires=">=3.9",
    extras_require={
        "asr": ["pydub"],
        "serve": ["chainlit~=1.0.200", "flask~=2.3.2", "flask-restful==0.3.9", "arize-phoenix==4.5.0"]
    },
    entry_points={
        "console_scripts": [
            "appbuilder_bce_deploy=appbuilder.utils.bce_deploy:deploy",
            "appbuilder_trace_server=appbuilder.utils.trace.phoenix_wrapper:runtime_main"
        ]
    },
    description="百度智能云千帆AppBuilder-SDK",
    long_description="百度智能云千帆AppBuilder, 开箱即用的组件与框架, 高效开发你的AI原生应用, 更多信息请登录: https://appbuilder.cloud.baidu.com/",
    url="https://github.com/baidubce/app-builder",
)
