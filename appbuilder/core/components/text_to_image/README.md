# AI作画-高级版 (Text2Image)

## 简介
AI作画-高级版（Text2Image）基于文心大模型，可以根据用户输入的文本，自动创作不限定风格的图，为内容创作者提供灵感和高质量配图。

## 基本用法

下面是AI作画的代码示例: 

```python
import os
import appbuilder
# 设置环境变量和初始化
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

text2Image = appbuilder.Text2Image()
content_data = {"prompt": "上海的经典风景", "width": 1024, "height": 1024, "image_num": 1}
msg = appbuilder.Message(content_data)
out = text2Image.run(msg)
print(out.content)
```

## 参数说明
### 初始化参数

无

### 调用参数
- `run`函数中包含以下参数：
   - `message`: 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"prompt": "上海的经典风景"})
   - `width`: 图片宽度，支持：512x512、640x360、360x640、1024x1024、1280x720、720x1280、2048x2048、2560x1440、1440x2560。
   - `height`: 图片高度，支持：512x512、640x360、360x640、1024x1024、1280x720、720x1280、2048x2048、2560x1440、1440x2560。
   - `image_num`: 生成图片数量，默认一张，支持生成 1-8 张。
   - `timeout`: HTTP超时时间
   - `retry`: HTTP重试次数

返回值示例：eg: {"img_urls": ["xxx"]}

## 高级用法

目前该模块仅提供基础的AI作画功能。
## 更新记录和贡献
* AI作画能力 (2023-12)