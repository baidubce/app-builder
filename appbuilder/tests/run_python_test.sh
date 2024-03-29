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
# 若单测失败，则退出
if [ $? -ne 0 ]; then exit 1; fi

# 6、基于coverage 测试结果计算全量单测覆盖率
coverage combine ./appbuilder/tests/
coverage xml -o coverage.xml 
coverage html -d coverage_html

# 7、计算增量代码的单测覆盖率
# 首先需要将coverage.xml里的文件路径替换
# 规则是：从python lib的安装目录，替换为git clone的目录，举例：
# 替换前 /Users/chengmo/Library/Python/3.9/lib/python/site-packages/
# 替换后 /Users/chengmo/workspace/baidu_code/app-builder/
# 首先获取appbuilder-sdk的python lib的安装目录
python_lib=$(python3 -m pip show appbuilder-sdk | grep Location | awk '{print $2}')
# 再获取git clone的目录
git_dir=$(pwd)
# 批量替换coverage.xml文件中的python_lib为git_dir，并将源文件备份一个orignal.xml后缀
python3 -u appbuilder/tests/sed_str.py coverage.xml $python_lib $git_dir
# 最后进行增量代码覆盖率测试
diff-cover coverage.xml --compare-branch=origin/master   --html-report coverage_diff.html
