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

## `setLogConfig`功能

Appbuilder-SDK新增滚动日志功能

主要参数:
- console_output: 数据类型bool，默认值True，LOG日志是否在控制台输出
- loglevel: 数据类型str，默认值"DEBUG"，LOG日志级别
- log_path: 数据类型str，默认值"/tmp"，默认日志存放路径。
- file_name: 数据类型str，默认值为进程id，日志名前缀
- rotate_frequency: 数据类型str，默认值"MIDNIGHT"，LOG日志滚动更新时间单位
    - "S": 以秒为单位
    - "M": 以分钟为单位
    - "H": 以小时为单位
    - "D": 以天为时间单位
    - "MIDNIGHT": 每日凌晨更新
- rotate_interval: 数据类型int，默认值1，LOG日志按时间滚动的参数，默认值为1，与when参数联合使用
- max_file_size: 数据类型Optional[int]，默认值None，传入`None`或负数会自动更新为系统最大整数`sys.maxsize`，单个滚动的LOG日志文件的最大大小，例：10M即为10\*1024\*1024 即需要传入 # 以B为单位
- total_log_size: 数据类型Optional[int]，默认值None，传入`None`或负数会自动更新为系统最大整数`sys.maxsize`，当前目录下可储存的LOG日志文件的最大大小，例：10M即为10\*1024\*1024 # 以B为单位
- max_log_files: 数据类型Optional[int]，默认值None，传入`None`或负数会自动更新为系统最大整数`sys.maxsize`，当前目录下可储存的LOG日志文件的最大数量

**注意:`setLogConfig`会自动生成error.file_name日志与file_name日志文件分别储存`error`级别日志和`loglevel`级别的日志,且两种日志文件的滚动逻辑是独立的，不相互影响。**
```python
# python
appbuilder.logger.setLogConfig(
    console_output = False,
    loglevel="DEBUG"
    log_path="/tmp",, 
    rotate_frequency="MIDNIGHT", # 每日凌晨更新 
    rotate_interval=1,
    max_file_size=100 * 1024 *1024, # 最大日志大小为100MB
    total_log_size=1024 * 1024 *1024, # 最大储存1GB的日志
    max_log_files=10, # 当前目录储存的最大LOG日志数 
    )
```