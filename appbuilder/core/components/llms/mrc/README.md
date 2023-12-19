# 阅读理解问答（MRC）

## 简介
阅读理解问答（MRC）组件是基于生成式大模型的阅读理解问答系统。该组件支持拒答、澄清、重点强调、友好性提升、溯源等多种功能，可用于回答用户提出的问题。

## 基本用法

### 快速开启

```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建MRC对象
mrc_component = appbuilder.MRC()

#初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)
context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）""",
                    """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心"""])

# 模拟运行MRC基本组件
result = mrc_component.run(msg, context_list)

# 输出运行结果
print(result)
```

## 参数说明

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数

- `msg (obj:Message)`: 输入消息，包含用户提出的问题。这是一个必需的参数。
- `context_list (obj:Message)`: 用户输入的问题对应的段落文本列表。这是一个必需的参数。
- `reject (bool, 可选)`: 拒绝开关，如果为 True，则启用拒绝能力。默认为 False。
- `clarify (bool, 可选)`: 澄清开关，如果为 True，则启用澄清能力。默认为 False。
- `highlight (bool, 可选)`: 重点强调开关，如果为 True，则启用重点强调能力。默认为 False。
- `friendly (bool, 可选)`: 友好性提升开关，如果为 True，则启用友好性提升能力。默认为 False。
- `cite (bool, 可选)`: 溯源开关，如果为 True，则启用溯源能力。默认为 False。
- `stream (bool, 可选)`: 指定是否以流式形式返回响应。默认为 False。
- `temperature (float, 可选)`: 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。

### 返回值
- 返回一个 `Message` 对象，包含模型运行后的输出消息。


## 高级用法
该组件的高级用法包括定制化的输入处理、输出处理，以及更复杂的调用场景。用户可以根据具体需求扩展组件功能，实现个性化的问答系统。
包括如下功能：
1、拒答
2、澄清反问
3、重点强调
4、友好度提升
5、溯源


### 代码样例
```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建MRC对象
mrc_component = appbuilder.MRC()

#初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)
context_list = appbuilder.Message(["""如何办理残疾人通行证一、残疾人通行证办理条件：
1、持有中华人民共和国残疾人证，下肢残疾或者听力残疾；
2、持有准驾车型为C1（听力残疾）、C2（左下肢残疾、听力残疾）""",
                    """3、本人拥有本市登记核发的非营运小型载客汽车，车辆须在检验有效期内，并有有效交强险凭证，
C5车辆加装操纵辅助装置后已办理变更手续。二、办理地点：北京市朝阳区左家庄北里35号：
北京市无障碍环境建设促进中心"""])

# 模拟运行MRC组件，开启拒答、澄清追问、重点强调、友好性提升和溯源能力五个功能
result = mrc_component.run(msg, context_list, reject=True,
                           clarify=True, highlight=True, friendly=True, cite=True)

# 输出运行结果
print(result)
```