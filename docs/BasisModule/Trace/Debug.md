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


## log高阶配置

`setLogConfig`功能可以设置日志的输出方式、是否滚动日志、滚动日志参数等。

参数说明:
- rolling (bool, optional): 是否启用滚动日志. 默认为True.
- update_interval (int, optional): 更新日志文件的间隔时间. 默认为1.
- update_time (str, optional): 更新日志文件的时间间隔单位. 默认为'midnight'，每日凌晨更新.
    - 可选值:
        - 'S' - Seconds
        - 'M' - Minutes
        - 'H' - Hours
        - 'D' - Days
        - 'W0'-'W6' - Weekday (0=Monday, 6=Sunday)
        - 'midnight' - Roll over at midnight 
- backup_count (int, optional): 备份日志文件的数量. 默认为无穷大.
- filename (str, optional): 日志文件的名称. 默认为空字符串.

需在代码中设置

```python
appbuilder.logger.setLoglevel("DEBUG")
"""
这里设置:
    rolling=Ture - 启用滚动日志(运行此段代码，默认使用滚动日志)
    filename="appbuilder.log" - 此优先级最高会覆盖之前的设置，若未传参则使用之前已经设置的日志文件，若之前未设置则使用默认的"tmp.log"日志文件
    update_interval = 1 - 更新日志文件的间隔数量级
    update_time = 'midnight' - 更新日志文件的间隔单位为秒级，每日凌晨滚动日志
"""
appbuilder.logger.setLogConfig(filename="appbuilder.log",update_interval=1, update_time='midnight')
```

## 新增功能
日志功能会自动开启日志的分离功能，独立创建一个`error.(filename).log'文件，用于存储`WARNING`、`ERROR`级别日志，同时会兼容日志的滚动功能。