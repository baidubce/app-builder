# 幻觉检测（Hallucination Detection）

## 简介
幻觉检测（Hallucination Detection）针对问答场景，检测答案中是否存在幻觉。

### 功能介绍
幻觉检测（Hallucination Detection）针对问答场景，检测答案中是否存在幻觉。

### 特色优势
无。

### 应用场景
问答场景，比如RAG问答。

## 基本用法

下面是幻觉检测的代码示例：

```python
import os
import appbuilder
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ['APPBUILDER_TOKEN'] = '...'

hallucination_detection = appbuilder.HallucinationDetection()

query = '澳门新麻蒲烤肉店每天开门吗？'
context = \
'''澳门美食： 澳门新麻蒲韩国烤肉店
在澳门一年四季之中除了火锅，烤肉也相当受欢迎。提到韩烧，有一间令我印象最深刻，就是号称韩国第一的烤肉店－新麻蒲韩国烤肉店，光是韩国的分店便多达四百多间，海外分店更是遍布世界各地，2016年便落户澳门筷子基区，在原本已经食肆林立的地方一起百花齐放！店内的装修跟韩国分店还完度几乎没差，让食客彷如置身于韩国的感觉，还要大赞其抽风系统不俗，离开时身上都不会沾上烤肉味耶！
时间：周一至周日 下午5:00 - 上午3:00
电话：＋853 2823 4012
地址：澳门筷子基船澳街海擎天第三座地下O号铺96号
必食推介:
护心肉二人套餐
来新麻蒲必试的有两样东西，现在差不多每间烤肉店都有炉边烤蛋，但大家知道吗？原来新麻蒲就是炉边烤蛋的开创者，既然是始祖，这已经是个非吃不可的理由！还有一款必试的就是护心肉，即是猪的横隔膜与肝中间的部分，每头猪也只有200克这种肉，非常珍贵，其味道吃起来有种独特的肉香味，跟牛护心肉一样精彩！
秘制猪皮
很多怕胖的女生看到猪皮就怕怕，但其实猪皮含有大量胶原蛋白，营养价值很高呢！这里红通通的猪皮还经过韩国秘制酱汁处理过，会有一点点辣味。烤猪皮的时候也需特别注意火侯，这样吃起来才会有外脆内Q的口感！'''
answer = '澳门新麻蒲烤肉店并不是每天开门，周日休息。'

inputs = {'query': query, 'context': context, 'answer': answer}
msg = appbuilder.Message(inputs)
result = hallucination_detection.run(msg)

print(result)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

### 初始化参数
| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `model` | str | 否 | 模型名称，用于指定要使用的千帆模型。 | ERNIE Speed-AppBuilder |
| `secret_key` | str | 否 | 用户鉴权token，默认从环境变量中获取: `os.getenv("APPBUILDER_TOKEN", "")` |  |
| `gateway` | str | 否 | 后端网关服务地址，默认从环境变量中获取: `os.getenv("GATEWAY_URL", "")` |  |
| `lazy_certification` | bool | 否 | 延迟认证，为True时在第一次运行时认证。默认为False。 | False |

### 调用参数 （以表格形式展示）
| 参数名称 | 参数类型 | 是否必须 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- | -------- |
| `message` | obj | 是 | 输入信息，用于传入用户查询query、根据query得到的检索结果context和基于context生成的query的答案answer。 | Message(content={'query': '...', 'context': '...', 'answer': '...'}) |
| `stream` | bool | 否 | 指定是否以流式形式返回响应。默认为 False。 | False |
| `temperature` | float | 否 | 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。 | 0.1 |
| `top_p` | float | 否 | 影响输出文本的多样性，取值越大，生成文本的多样性越强。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 0。 | 0.0 |

### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
| ------- | ------- | -------- | -------- |
| `result` | obj | 模型运行后的输出结果（可通过result.content获取结果核心内容） | Message(content='...') |

### 响应示例
```
```

### 错误码
|错误码|描述|
| ------ | ------ |

## 高级用法
可用于RAG问答的答案检测。

## 更新记录和贡献
### 2024.5.22
#### [Added]
- 增加幻觉检测组件。
- 增加幻觉检测组件单元测试。