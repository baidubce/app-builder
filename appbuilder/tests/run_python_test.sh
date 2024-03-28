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
# See the License for the specific language governing permissions and
# limitations under the License.

# 该脚本执行以下功能
# 1、克隆git仓库: 
# 2、基于环境变量，checkout到指定commit
# 3、执行setup.sh，生产whl包，并更新当前环境的python库
# 4、执行parallel_ut_run.py，运行python单元测试
# 5、基于测试结果计算单测覆盖率


# 1、克隆git仓库
git clone https://github.com/baidubce/app-builder.git
cd app-builder


# 2、checkout到制定commit
# 环境变量形如：AGILE_REVISION=2352a2574bdfcfff22f0ba7413d9318781a85b3d
export AGILE_REVISION=2352a2574bdfcfff22f0ba7413d9318781a85b3d
commit_id=$AGILE_REVISION
# checkout 到指定commit
git checkout $commit_id

# 3、执行setup.py，生产whl包，并更新当前环境的python库
python3 -m pip install wheel
python3 setup.py bdist_wheel
pip install -U dist/*.whl

# 4、单测环境的涉密准备
# 4.1、首先是各个单测所需的token、appid、secret等信息，会保存在仅在百度内网可以下载的环境中



# 5、执行parallel_ut_run.py，运行python单元测试
python3 appbuilder/tests/parallel_ut_run.py


