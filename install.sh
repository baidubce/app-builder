# linux系统快捷安装包shell脚本
python3 -m pip uninstall appbuilder-sdk -y
rm -rf dist
python3 -u setup.py bdist_wheel
python3 -m pip install dist/*.whl
