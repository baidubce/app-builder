# 手写文字识别 （HandwriteOCR）

## 简介
手写文字识别 （HandwriteOCR），图片中的手写中文、手写数字进行检测和识别，针对不规则的手写字体进行专项优化，识别准确率可达90%以上。


### 功能介绍
检测识别图片中的手写中文、手写数字，针对不规则的手写字体进行专项优化


### 特色优势
识别准确率可达90%以上

### 应用场景
手写文字识别


## 基本用法

下面是手写文字识别的代码示例：
```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."
image_url="https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"

# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行手写文字识别
handwrite_ocr = appbuilder.HandwriteOCR()
out = handwrite_ocr.run(inp)
# 打印识别结果
print(out.content) 

```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数 
| 参数名称       | 参数类型   | 是否必须 | 描述                          |示例值|
|------------|--------|------|-----------------------------|---|
| message    | String | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数 ||
| +content   | Dict   | 是    | 消息内容                        ||
| +raw_image | String | 否    | 原始图片字节流                     ||
| +url       | String   | 否    | 图片下载链接地址                    ||
|timeout| Float   | 否    | HTTP超时时间,单位：秒               |1||
|retry|Integer| 否    | HTTP重试次数                    |3||

   
### 响应参数
| 参数名称      | 参数类型     | 描述 | 示例值                                                             |
|-----------|----------|--|-----------------------------------------------------------------|
| contents  | List     | 文本内容块 | |
| +text     | String   | 文本字符串 | |
| +Position | Dict     | 文本位置信息 | |
| ++left    | Interger | 表示定位位置的长方形左上顶点的水平坐标 | |
| ++top      | Interger |  表示定位位置的长方形左上顶点的垂直坐标| |
| ++width   | Interger | 表示定位位置的长方形的宽度 | |
| ++height  | Interger | 表示定位位置的长方形的高度 | |
| direction | Interger | 图像旋转角度 | 图像旋转角度，0（正向），- 1（逆时针90度），- 2（逆时针180度），- 3（逆时针270度）|

### 响应示例
```json
{
	"contents": [{
			"text": "我们家住的小区里有很多银杏树。",
			"position": {
				"left": 390,
				"top": 46,
				"width": 1801,
				"height": 161
			}
		},
		{
			"text": "它们笔直笔直的,就像一位正在站岗的",
			"position": {
				"left": 131,
				"top": 263,
				"width": 2083,
				"height": 170
			}
		},
		{
			"text": "卫兵。它枝繁叶茂,长的非常好,它的叶子",
			"position": {
				"left": 154,
				"top": 483,
				"width": 2023,
				"height": 161
			}
		},
		{
			"text": "有些小的像一把把小扇子,大的也像扇子。",
			"position": {
				"left": 151,
				"top": 699,
				"width": 2167,
				"height": 168
			}
		},
		{
			"text": "但是中间有一个缺口,就像被淘汽的小",
			"position": {
				"left": 148,
				"top": 929,
				"width": 2123,
				"height": 177
			}
		},
		{
			"text": "朋友用剪刀剪掉了一样。",
			"position": {
				"left": 161,
				"top": 1165,
				"width": 1340,
				"height": 217
			}
		}
	],
	"direction": 0
}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的手写体识别。


## 更新记录和贡献
* 手写文字识别 (2024-01)
* 手写文字识别 (2024-02)
