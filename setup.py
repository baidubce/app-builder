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

setup(
    name='appbuilder-sdk',
    version='0.6.0',
    author='dongdaxiang',
    author_email='dongdaxiang@baidu.com',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    extras_require={
        'serve': ['chainlit~=1.0.200', 'flask~=2.3.2', 'flask-restful==0.3.9']
    }
)

