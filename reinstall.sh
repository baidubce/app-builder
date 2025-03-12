#! /bin/bash
pip3 uninstall -y appbuilder-sdk
python3 setup.py bdist_wheel
pip3 install dist/appbuilder_sdk-1.0.3-py3-none-any.whl