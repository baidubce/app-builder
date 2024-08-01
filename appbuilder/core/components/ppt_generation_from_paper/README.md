# 论文生成PPT（PPTGenerationFromPaper）

## 简介
论文生成PPT组件（PPTGenerationFromPaper）可以根据上传的论文（支持**中英文**）生成PPT。

### 功能介绍
根据上传的论文（支持**中英文**）生成PPT。

### 特色优势
可根据论文（支持**中英文**）生成高质量PPT。

### 应用场景
PPT生成。

## 基本用法
### 快速开始
```python
import os
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'


ppt_generator = appbuilder.PPTGenerationFromPaper()

user_input = {
    'file_key': 'http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx',
    'style': '科技',
    'color': '蓝色',
    'title': '',
    'pleader': '百度千帆AppBuilder',
    'advisor': '百度千帆AppBuilder',
    'school': '北京大学',
    'school_logo': '',
    'school_picture': ''
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
| `file_key` | str | 是 | 论文链接。 | http://image.yoojober.com/users/chatppt/temp/2024-06/6672aa839a9da.docx |
| `style` | str | 否 | PPT风格，可选：科技、商务、小清新、可爱卡通、中国风、极简、党政。 | 科技 |
| `color` | str | 否 | PPT主色调。可选：紫色、红色、橙色、黄色、绿色、青色、蓝色、粉色。 | 紫色 |
| `title` | str | 否 | 自定义标题。优先使用自定义标题，如果为空则使用解析结果中的标题。 | 论文分享 |
| `pleader` | str | 否 | 汇报人。 | 百度千帆AppBuilder |
| `advisor` | str | 否 | 指导教师。 | 百度千帆AppBuilder |
| `school` | str | 否 | 学校名称。 | 北京大学 |
| `school_logo` | str | 否 | 学校logo链接。 |  |
| `school_picture` | str | 否 | 学校图片链接。 |  |


### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果，包含PPT下载链接。 | Message(content='...') |

### 响应示例
```
https://download.yoojober.com/chatppt_business/2024-07/6f472b65ee324d2da7849b6003a896e3.pptx?e=1721964794&token=8_2qFlGEVQZPpFvHdGR6gg2t9A9QZfWT9wwTl92s:nG-hbPN51uPP8FOeTY2jdQcT51w=
```

## 高级用法

## 更新记录和贡献
### 2024.8.1
#### [Added]
- 增加论文生成PPT组件。
- 增加论文生成PPT组件单元测试。