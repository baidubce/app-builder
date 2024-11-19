#1、清除生成文档环境
cd ../../..
rm -rf java/doc
rm -rf docs/API-Reference/Java/*

# 2、生成Java API文档
cd java
javadoc -d doc -sourcepath src/main/java -subpackages com.baidubce.appbuilder -exclude com.baidubce.appbuilder.base -encoding UTF-8 -charset UTF-8

# 3、迁移文档到docs目录，并删除java/doc目录
cd ..
cp -r java/doc/* docs/API-Reference/Java
rm -rf java/doc

# 4、辅助Java API文档目录文档到docs目录
cp docs/Tools/JavaAPI/JavaAPI.md docs/API-Reference/Java