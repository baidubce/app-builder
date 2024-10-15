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


# # 1、克隆git仓库
# git clone https://github.com/baidubce/app-builder.git
# cd app-builder
# 1.1、添加提交者的源
# fork_repo="https://github.com/$AGILE_MODULE_NAME.git"
# git clone $fork_repo
# cd app-builder
# git remote add upstream https://github.com/baidubce/app-builder.git 
# git fetch upstream


# # 2、checkout到制定commit
# # 环境变量形如：AGILE_REVISION=2352a2574bdfcfff22f0ba7413d9318781a85b3d
# export AGILE_REVISION=2352a2574bdfcfff22f0ba7413d9318781a85b3d
# commit_id=$AGILE_REVISION
# # checkout 到指定commit
# git checkout $commit_id
# 代码Pass，保存在流水线配置中，并在流水线环境执行

# 3、单测环境的涉密准备
# 3.1、首先是各个单测所需的token、appid、secret等信息，会保存在仅在百度内网可以下载的环境中
# 代码Pass，保存在流水线配置中，并在流水线环境执行

# 4、执行setup.py，生产whl包，并更新当前环境的python库
python3 -m pip install wheel
python3 -m pip install coverage
python3 -m pip install diff-cover

python3 setup.py bdist_wheel
python3 -m pip install --force-reinstall dist/*.whl
python3 -m pip uninstall numpy -y
python3 -m pip install numpy==1.26.4
echo "重新安装pydantic包，设置版本为2.7.4"
python3 -m pip uninstall -y pydantic
python3 -m pip install pydantic==2.7.4
python3 -m pip install langchain==0.3.0
python3 -m pip install datamodel-code-generator==0.25.8
cd appbuilder/tests/


# 5、执行parallel_ut_run.py，运行python单元测试
python3 parallel_ut_run.py

run_result=$?

# 6、基于coverage 测试结果计算全量单测覆盖率
# coverage combine ./appbuilder/tests/
coverage combine
coverage xml -o coverage.xml 
coverage html -d coverage_html
echo "--------------------------"
echo "全量代码覆盖率为："
coverage report -m
echo "--------------------------"

# 7、计算增量代码的单测覆盖率
# 首先需要将coverage.xml里的文件路径替换
# 规则是：从python lib的安装目录，替换为git clone的目录，举例：
# 替换前 /Users/chengmo/Library/Python/3.9/lib/python/site-packages/
# 替换后 /Users/chengmo/workspace/baidu_code/app-builder/
# 首先获取appbuilder-sdk的python lib的安装目录
python_lib=$(python3 -m pip show appbuilder-sdk | grep Location | awk '{print $2}')
# 再获取git clone的目录, 当前目录为 app-builder/appbuilder/tests, 取 app-builder/目录
git_dir=$(pwd | sed 's/appbuilder\/tests//')
# 批量替换coverage.xml文件中的python_lib为git_dir，并将源文件备份一个orignal.xml后缀
python3 -u sed_str.py coverage.xml $python_lib $git_dir
# 最后进行增量代码覆盖率测试
echo "增量代码覆盖率为："
diff-cover coverage.xml --compare-branch=upstream/master   --html-report coverage_diff.html --fail-under=90
cover_result=$?

echo "--------------------------"
echo "CI 流水线运行结果如下: "
echo "单测运行结果: $run_result"
echo "单测覆盖率结果: $cover_result"
echo "--------------------------"

echo "--------------------------"
echo "Components组件检查规范性检测结果: "
python3 print_components_error_info.py
echo "--------------------------"

# 若单测失败，则退出
if [ $run_result -ne 0 ]; then echo "单测运行失败，请检查错误日志，修复单测后重试" && exit 1; fi

if [ $cover_result -ne 0 ]; then echo "增量代码的单元测试覆盖率低于90%，请完善单元测试后重试" && exit 1; fi


