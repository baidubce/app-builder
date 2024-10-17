echo "========================开始更新文档========================"

# 1、注释@HTTPClient\.check_param装饰器
echo "================注释@HTTPClient.check_param装饰器==============="
echo "当前路径:"
pwd
cd ../..
find . -name "*.py" -exec sed -i '' 's/@HTTPClient\.check_param/# @HTTPClient.check_param/g' {} \;
cd docs/sphinx_doc
echo "===============注释@HTTPClient.check_param装饰器完成=============="

# 2、安装依赖
echo "=========================安装依赖========================="
echo "当前路径:"
pwd
python3 -m pip install -r requirements.txt

echo "安装当前目录的Appbuilder-SDK:"
cd ../..
python3 -m pip uninstall appbuilder-sdk -y
rm -rf dist
python3 -u setup.py bdist_wheel
python3 -m pip install dist/*.whl
# 更新builde目录
rm -rf build
cd docs/sphinx_doc
echo "=========================安装依赖========================="


# 3、删除 doc/build 下的所有文件夹
echo "================删除 doc/build 下的所有文件夹================"
echo "当前路径:"
pwd
echo "删除  build 下的所有文件夹及文件:"
rm -r build/*
echo "删除  build 下的所有文件夹及文件完成"
echo "==============删除 doc/build  下的所有文件夹完成=============="


# 4、删除  doc/source 下除index.rst的所有.rst文件
echo "==========删除doc/source下除index.rst的所有.rst文件=========="
echo "当前路径:"
pwd
echo "删除  source 下除index.rst的所有.rst文件:"
cd source
find . -maxdepth 1 -type f -name '*.rst' ! -name 'index.rst' -exec rm {} \;|| { echo "删除  doc/source 下除index.rst的所有.rst文件失败"; exit 1; }
cd ..
echo "删除  source 下除index.rst的所有.rst文件完成"
echo "=========删除doc/source下除index.rst的所有.rst文件完成========="


# 5、删除原有的 docs/sphinx_md 文件夹及其文件
echo "============删除原有的 docs/sphinx_md 文件夹及其文件============"
echo "当前路径:"
pwd
rm -rf ../docs/sphinx_md/*
echo "===========删除原有的 docs/sphinx_md 文件夹及其文件完成==========="


# 6、在doc目录下下执行命令   sphinx-apidoc -o source ../appbuilder/
echo "=======执行命令 sphinx-apidoc -o source ../appbuilder/======="
echo "当前路径:"
pwd
sphinx-apidoc -o source ../../appbuilder/
# 删除test目录内容
rm ./source/appbuilder.tests.*
rm ./source/appbuilder.utils.*
rm ./source/appbuilder.core.assistant.type.rst

cp update_rst.py source/
cd source
python3 update_rst.py
rm -rf update_rst.py
cd ..
echo "======执行命令 sphinx-apidoc -o source ../appbuilder/完成======"


# 7、在doc目录下执行命令 make markdown
echo "==============在doc目录下执行命令 make markdown================"
echo "当前路径:"
pwd

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

DOC_DIR="$SCRIPT_DIR"
cd "$DOC_DIR" || { echo "无法切换到 $DOC_DIR 目录"; exit 1; }

echo "当前路径: $(pwd)"

export PATH=/path/to/your/python:$PATH
# 执行 make markdown
make markdown || { echo "make markdown 命令失败"; exit 1; }
echo "=============在doc目录下执行命令 make markdown 完成=============="


# 8、恢复装饰器
echo "========================恢复装饰器========================"
cd ../..
echo "当前路径:"
pwd
find . -name "*.py" -exec sed -i '' 's/# @HTTPClient\.check_param/@HTTPClient.check_param/g' {} \; || { echo "恢复装饰器失败"; exit 1; }
cd docs/sphinx_doc
echo "========================恢复装饰器完成========================"


# 9、清理多余文件
echo "========================清理多余文件========================"
echo "当前路径:"
pwd
cd source
find . -maxdepth 1 -type f -name '*.rst' ! -name 'index.rst' -exec rm {} \;|| { echo "删除  doc/source 下除index.rst的所有.rst文件失败"; exit 1; }
cd ..
echo "删除  doc/source 下除index.rst的所有.rst文件完成"
rm -rf /build/doctrees/*
echo "======================清理多余文件完成======================"


echo "========================更新文档完成========================"
