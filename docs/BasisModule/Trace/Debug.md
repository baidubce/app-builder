# Appbuilder-SDK Debug

## 打印DEBUG日志

开启DEBUG日志，可以打印出更多的日志信息，方便调试，包括且不限于：请求URL、请求头、请求参数等。

```bash
# 可以设置环境变量开启
# 开启DEBUG
export APPBUILDER_LOGLEVEL=DEBUG
# 关闭DEBUG
export APPBUILDER_LOGLEVEL=INFO
```

也可以在代码中设置，优先级高于环境变量。
```python
# python
appbuilder.logger.setLoglevel("DEBUG")
```
```java
// java
System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
```
```golang
// golang
os.Setenv("APPBUILDER_LOGLEVEL", "DEBUG")
```

## 指定日志文件

如果需要将日志输出到指定文件，方便落盘。默认输出为标准输出流。
可以设置环境变量`APPBUILDER_LOGFILE`。

```bash
# 文件名及路径可以根据实际使用修改
export APPBUILDER_LOGFILE=/tmp/appbuilder.log
```

也可以在代码中设置，优先级高于环境变量。

```python
# python
appbuilder.logger.setFilename("/tmp/appbuilder.log")
```

```java
// java
System.setProperty("APPBUILDER_LOGLFILE", "/tmp/appbuilder.log");
```

```golang
// golang
os.Setenv("APPBUILDER_LOGLEVEL", "/tmp/appbuilder.log")
```