# 身份证混贴识别（MixCardOCR）

## 简介
身份证混贴识别（MixCardOCR），身份证混贴识别支持自动检测与识别身份证正反面在同一张图片上的场景，一次识别图片中身份证正反面所有字段。


### 功能介绍


### 特色优势


### 应用场景



## 基本用法

下面是身份证混贴识别的代码示例：
```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["GATEWAY_URL"] = "..."
os.environ["APPBUILDER_TOKEN"] = "..."
image_url="https://bj.bcebos.com/v1/appbuilder/test_handwrite_ocr.jpg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-23T11%3A58%3A09Z%2F-1%2Fhost%2F677f93445fb65157bee11cd492ce213d5c56e7a41827e45ce7e32b083d195c8b"

# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行手写体识别
mix_card_ocr = appbuilder.MixCardOCR()
out = mix_card_ocr.run(inp)
# 打印识别结果
print(out.content) 
 
```


## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数

无

### 调用参数 （以表格形式展示）
|参数名称 |参数类型 | 是否必须 | 描述                                                                    |示例值|
|--------|--------|------|-----------------------------------------------------------------------|------|
|message |String  | 是    | 输入的消息，用于模型的主要输入内容。这是一个必需的参数，例如：Message(content={"raw_image": b"..."}) |eg.示例值|
|timeout|Integer| 否    | HTTP超时时间                                                              |10|
|retry|Integer| 否    | HTTP重试次数                                                              |3|


### 响应参数

| 参数名称       | 参数类型   | 描述                  | 示例值                                                |
|------------|--------|---------------------|----------------------------------------------------|
| front      | object | 身份证正面信息             |                                                    |
| +fields    | list   | 字段信息                |                                                    |
| ++key      | str    | 字段名                 |                                                    |
| ++value    | str    | 字段值                 |                                                    |
| ++position | object | 字段坐标,结构同下position           |                                                    |
| +position | object | 身份证正面坐标             |                                                    |
| ++left | int | 表示定位位置的长方形左上顶点的水平坐标 |                                                    |
| ++right | int | 表示定位位置的长方形左上顶点的垂直坐标 |                                                    |
| ++width | int | 表示定位位置的长方形的宽度       |                                                    |
| ++height | int | 表示定位位置的长方形的高度       |                                                    |
| back      | object | 身份证反面信息，结构同front    |                                            |
| direction | int    | 图像旋转角度              | 图像旋转角度，0（正向），- 1（逆时针90度），- 2（逆时针180度），- 3（逆时针270度） |

### 响应示例
```json
{
	"front": {
		"fields": [{
				"key": "出生",
				"value": "19920225",
				"position": {
					"left": 620,
					"top": 218,
					"width": 239,
					"height": 30
				}
			},
			{
				"key": "性别",
				"value": "女",
				"position": {
					"left": 616,
					"top": 164,
					"width": 25,
					"height": 30
				}
			},
			{
				"key": "民族",
				"value": "汉",
				"position": {
					"left": 766,
					"top": 164,
					"width": 29,
					"height": 30
				}
			},
			{
				"key": "姓名",
				"value": "姚佳",
				"position": {
					"left": 621,
					"top": 102,
					"width": 84,
					"height": 35
				}
			},
			{
				"key": "公民身份号码",
				"value": "110103199202250229",
				"position": {
					"left": 733,
					"top": 417,
					"width": 399,
					"height": 36
				}
			},
			{
				"key": "住址",
				"value": "北京市海淀区仙秀园555号",
				"position": {
					"left": 618,
					"top": 277,
					"width": 253,
					"height": 67
				}
			}
		],
		"position": {
			"left": 483,
			"top": 42,
			"width": 737,
			"height": 464
		}
	},
	"back": {
		"fields": [{
				"key": "签发日期",
				"value": "20150413",
				"position": {
					"left": 789,
					"top": 946,
					"width": 139,
					"height": 34
				}
			},
			{
				"key": "签发机关",
				"value": "北京市公安局海淀分局",
				"position": {
					"left": 787,
					"top": 883,
					"width": 275,
					"height": 35
				}
			},
			{
				"key": "失效日期",
				"value": "20350413",
				"position": {
					"left": 946,
					"top": 945,
					"width": 144,
					"height": 34
				}
			}
		],
		"position": {
			"left": 473,
			"top": 537,
			"width": 749,
			"height": 480
		}
	},
	"direction": 0
}
```

### 错误码
|错误码|描述|
|------|---|

## 高级用法
目前该模块仅提供基础的身份证混贴识别。

