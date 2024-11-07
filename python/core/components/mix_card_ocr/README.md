# 身份证混贴识别（MixCardOCR）

## 简介
身份证混贴识别（MixCardOCR），身份证混贴识别支持自动检测与识别身份证正反面在同一张图片上的场景，一次识别图片中身份证正反面所有字段。


### 功能介绍
支持对二代居民身份证正反面所有8个字段进行结构化识别，包括姓名、性别、民族、出生日期、住址、身份证号、签发机关、有效期限，识别准确率超过99%；同时支持身份证正面头像检测，并返回头像切片的base64编码及位置信息。

### 特色优势
同时，支持对用户上传的身份证图片进行图像风险和质量检测，可识别图片是否为复印件或临时身份证，是否被翻拍或编辑，是否存在正反颠倒、模糊、欠曝、过曝等质量问题。



### 应用场景
身份证混贴识别支持自动检测与识别身份证正反面在同一张图片上的场景，一次识别图片中身份证正反面所有字段。


## 基本用法

下面是身份证混贴识别的代码示例：

示例图片为：![示例图片](https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18296bd29598)

```python
import os
import requests
import appbuilder

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

image_url= "https://bj.bcebos.com/v1/appbuilder/test_mix_card_ocr.jpeg?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-01-24T06%3A18%3A11Z%2F-1%2Fhost%2F695b8041c1ded194b9e80dbe1865e4393da5a3515e90d72d81ef18296bd29598"


# 从BOS存储读取样例文件
raw_image = requests.get(image_url).content
inp = appbuilder.Message(content={"raw_image": raw_image})
# inp = Message(content={"url": image_url})

# 运行身份证混贴识别OCR
mix_card_ocr = appbuilder.MixCardOCR()
out = mix_card_ocr.run(inp)
# 打印识别结果
print(out.content) 

# {'front': {'fields': [{'key': '出生', 'value': '19920225', 'position': {'left': 620, 'top': 218, 'width': 239, 'height': 30}}, {'key': '性别', 'value': '女', 'position': {'left': 616, 'top': 164, 'width': 25, 'height': 30}}, {'key': '民族', 'value': '汉', 'position': {'left': 766, 'top': 164, 'width': 29, 'height': 30}}, {'key': '姓名', 'value': '姚佳', 'position': {'left': 621, 'top': 102, 'width': 84, 'height': 35}}, {'key': '公民身份号码', 'value': '110103199202250229', 'position': {'left': 733, 'top': 417, 'width': 399, 'height': 36}}, {'key': '住址', 'value': '北京市海淀区仙秀园555号', 'position': {'left': 618, 'top': 277, 'width': 253, 'height': 67}}], 'position': {'left': 483, 'top': 42, 'width': 737, 'height': 464}}, 'back': {'fields': [{'key': '签发日期', 'value': '20150413', 'position': {'left': 789, 'top': 946, 'width': 139, 'height': 34}}, {'key': '签发机关', 'value': '北京市公安局海淀分局', 'position': {'left': 787, 'top': 883, 'width': 275, 'height': 35}}, {'key': '失效日期', 'value': '20350413', 'position': {'left': 946, 'top': 945, 'width': 144, 'height': 34}}], 'position': {'left': 473, 'top': 537, 'width': 749, 'height': 480}}, 'direction': 0}
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

| 参数名称       | 参数类型   | 描述                  | 示例值                                                |
|------------|--------|---------------------|----------------------------------------------------|
| front      | object | 身份证正面信息             |                                                    |
| +fields    | list   | 字段信息                |                                                    |
| ++key      | str    | 字段名                 |                                                    |
| ++value    | str    | 字段值                 |                                                    |
| ++position | object | 字段坐标,结构同下position           |                                                    |
| +position  | object | 身份证正面坐标             |                                                    |
| ++left     | int | 表示定位位置的长方形左上顶点的水平坐标 |                                                    |
| ++top        | int | 表示定位位置的长方形左上顶点的垂直坐标 |                                                    |
| ++width    | int | 表示定位位置的长方形的宽度       |                                                    |
| ++height   | int | 表示定位位置的长方形的高度       |                                                    |
| back       | object | 身份证反面信息，结构同front    |                                            |
| direction  | int    | 图像旋转角度              | 图像旋转角度，0（正向），- 1（逆时针90度），- 2（逆时针180度），- 3（逆时针270度） |

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

## 更新记录和贡献
* 身份证混贴识别 (2024-01)