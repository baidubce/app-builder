# 描述生成PPT（PPTGeneration）

## 简介
描述生成PPT组件（PPTGeneration）可以基于对PPT的描述或者自定义信息生成PPT。

### 功能介绍
基于对PPT的描述或者自定义信息生成PPT。

### 特色优势
- 可生成高质量PPT。
- 支持传入自定义信息生成PPT。
- 生成PPT复杂度可控。

### 应用场景
PPT生成。

## 基本用法
### 快速开始
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'


ppt_generator = appbuilder.PPTGeneration()

user_input = {
    'text': '生成一个介绍北京的PPT。',
    'custom_data': {},
    'complex': 1,
    'user_name': '百度千帆AppBuilder'
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
| `text` | str | 是 | 请求生成PPT的query。可为空字符串""，与custom_data有一个参数不为空即可。 | 请你生成一个介绍北京的PPT。 |
| `custom_data` | obj | 是 | 自定义参数，可指定标题、副标题、作者、结构等信息。可为空字典{}，与text有一个参数不为空即可。 | `{"title": "标题", "sub_title": "副标题", "author": "作者", "catalogs": [{"catalog": "一级大纲1", "sub_catalog": ["一级大纲1-二级大纲1"]}, {"catalog": "一级大纲2", "sub_catalog": ["一级大纲2-二级大纲1"]}], "contents": [{"catalog_index": 0, "sub_catalog_index": 0, "content": ["一级大纲1-二级大纲1-内容1", "一级大纲1-二级大纲1-内容2"]}, {"catalog_index": 1, "sub_catalog_index": 0, "content": [{"key": "一级大纲2-二级大纲1-小标题1", "value": "一级大纲2-二级大纲1-子内容1"}, {"key": "一级大纲2-二级大纲1-小标题2", "value": "一级大纲2-二级大纲1-子内容2"}, {"key": "一级大纲2-二级大纲1-小标题3", "value": "一级大纲2-二级大纲1-子内容3"}], "picture": ["https://image.yoojober.com/chatppt_business/2024-02/000114cd07b809cb8c6bb22674e814da.png"]}]}` |
| `complex` | integer | 否 | PPT复杂度，可选：1、2、3，其中1最简单、3最复杂。 | 1 |
| `font_name` | str | 否 | PPT字体，可选：黑体、宋体、仿宋、幼圆、楷体、隶书。 | 黑体 |
| `user_name` | str | 否 | 作者名。 | 百度千帆AppBuilder |


### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果，包含PPT下载链接。 | Message(content='...') |

### 响应示例
```
https://download.yoojober.com/chatppt_business/2024-07/bf2af50285e52261507abdd7385e02c4.pptx?e=1721964536&token=8_2qFlGEVQZPpFvHdGR6gg2t9A9QZfWT9wwTl92s:nikgRM9RbPxzClBvmKrweeKd9Ck=
```

## 高级用法

## 更新记录和贡献
### 2024.7.25
#### [Added]
- 增加描述生成PPT组件。
- 增加描述生成PPT组件单元测试。