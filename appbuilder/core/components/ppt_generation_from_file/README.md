# 文件生成PPT（PPTGenerationFromFile）

## 简介
文件生成PPT组件（PPTGenerationFromFile）可以根据上传的**中文**文件生成PPT。

### 功能介绍
根据上传的**中文**文件生成PPT。

### 特色优势
可根据**中文**文件生成高质量PPT。

### 应用场景
PPT生成。

## 基本用法
### 快速开始
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'


ppt_generator = appbuilder.PPTGenerationFromFile()

user_input = {
    'file_url':'http://image.yoojober.com/users/chatppt/temp/2024-06/6672a92c87e6f.doc',
    'user_name':'百度千帆AppBuilder'
}
result = ppt_generator(appbuilder.Message(user_input))
print(result.content)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ['APPBUILDER_TOKEN'] = 'bce-YOURTOKEN'
```

### 初始化参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `secret_key` | str | 否 | 用户鉴权token，默认从环境变量中获取: `os.getenv("APPBUILDER_TOKEN", "")` | bce-v3/XXX |
| `gateway` | str | 否 | 后端网关服务地址，默认从环境变量中获取: `os.getenv("GATEWAY_URL", "")` | https://appbuilder.baidu.com |
| `lazy_certification` | bool | 否 | 延迟认证，为True时在第一次运行时认证。默认为False。 | False |

### 调用参数

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `message` | obj | 是 | 输入消息，用于模型的主要输入内容。 | Message(content=input_data) |
| `poll_request_times` | int | 否 | 轮询请求结果次数。默认为60。 | 60 |
| `poll_request_interval` | int | 否 | 轮询请求的间隔时间（秒）。默认为5。 | 5 |

其中message包含的input_data包括以下参数：

| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `file_url` | str | 是 | 文件链接。 | http://image.yoojober.com/users/chatppt/temp/2024-06/6672a92c87e6f.doc |
| `user_name` | str | 否 | 作者名。 | 百度千帆AppBuilder |


### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果，包含PPT下载链接。 | Message(content='...') |

### 响应示例
```
https://download.yoojober.com/chatppt_business/2024-07/d1a1ab518ebcfbba7908a6734fa11d13.pptx?e=1721964933&token=8_2qFlGEVQZPpFvHdGR6gg2t9A9QZfWT9wwTl92s:9bs8LWV1SQLJNJoJgtd-sLF-CTw=
```

## 高级用法

## 更新记录和贡献
### 2024.7.25
#### [Added]
- 增加文件生成PPT组件。
- 增加文件生成PPT组件单元测试。