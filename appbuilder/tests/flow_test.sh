# 1、配置环境变量
export APPBUILDER_TOKEN='bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd'
export APPBUILDER_TOKEN_V2='bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4'
export BAIDU_VDB_API_KEY='apaasTest1'
export INSTANCE_ID='vdb-bj-vuzmppgqrnhv'
export DATASET_ID='c4652b26-3f2b-4cd1-9ca2-98cd26adc36f'
export APPBUILDER_TOKEN_DOC_FORMAT='bce-v3/ALTAK-bcKsgHd39g0Aaq3nCYUUQ/b06384229df1462c6fb011383d09230346a20ac4'
 
# 2、更新当前环境的python库
pwd
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
python3 -m pip install wheel
python3 -m pip install chainlit~=1.0.200 flask~=2.3.2 flask-restful==0.3.9

cd ../.. 
python3 setup.py bdist_wheel
python3 -m pip uninstall -y appbuilder-sdk
python3 -m pip install --force-reinstall dist/*.whl # 这里需要更换为appbuilder-sdk的whl包路径
unzip -d . /*.whl # 这里需要更换为appbuilder-sdk的whl包路径
cd appbuilder/tests/

 
# 3、执行parallel_ut_run.py，运行python单元测试
python3 parallel_ut_run.py
 
run_result=$?

 
# 若单测失败，则退出
if [ $run_result -ne 0 ]; then  
    echo "单测运行失败，请检查错误日志，修复单测后重试"  
    exit 1  # 退出并返回错误码1  
else  
    echo "单测运行成功"  
fi