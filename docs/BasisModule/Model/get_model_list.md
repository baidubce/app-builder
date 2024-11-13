# 千帆模型列表获取能力

## 简介
该能力可以通过参数控制获取用户可用的不同类型的千帆大模型名称，从而进行大模型组件的调用，该能力获取的模型名称可以直接传参到大模型组件的model字段。

## 基本用法

下面是模型列表获取功能的代码示例：

```python
import os
import appbuilder
# 设置环境变量和初始化
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."
models = appbuilder.get_model_list(api_type_filter=["chat"], is_available=True)
print(models)
```
## 参数说明

### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数

无

### 调用参数
|参数名称 | 参数类型         | 是否必须 |描述 | 示例值  |
|--------|--------------|------|----|------|
|secret_key | String       | 否    |用户鉴权token, 默认从环境变量中获取| bce-YOURTOKEN |
|api_type_filter| List[String] | 否    |根据apiType过滤，["chat", "completions", "embeddings", "text2image"]，不填包括所有的。| chat |
|is_available| Boolean      | 否    |是否返回可用模型列表, 默认返回所有模型。| True |


### 返回示例
['ERNIE-Bot 4.0', 'ERNIE-Bot', 'ERNIE-Bot-turbo']


## 高级用法

目前该模块仅提供获取千帆模型列表功能。


## 更新记录和贡献
* 千帆模型列表获取能力 (2024-1)