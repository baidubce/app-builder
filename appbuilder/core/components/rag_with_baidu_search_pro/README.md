# 百度搜索RAG_PRO

## 简介
百度搜索RAG_PRO组件旨在解决传统生成模型在生成长文本时可能会受到信息获取不足的问题，核心思想是将百度搜索与LLM相结合，使得生成的文本可以借助检索到的信息进行增强，从而提高生成文本的质量和相关性。

### 功能介绍
基于百度搜索结果进行RAG检索增强问答。
百度搜索RAG_PRO组件支持配置用户指令，temperature，top_p，以及溯源开关等，为用户提供了更灵活的控制选项。
对比旧版百度搜索RAG，新版百度搜索RAG_PRO在支持配置检索个数和检索类型（网页、视频等）方面进行了升级。

### 特色优势
百度搜索RAG_PRO组件的综合优势在于通过结合百度搜索的搜索引擎技术和ERNIE模型的语义理解能力，可以更准确地理解用户的搜索意图，并提供与搜索查询相关性更高的搜索结果。

### 应用场景
通用搜索领域

## 基本用法
以下是一个简单的例子来演示如何开始使用百度搜索RAG_PRO组件：

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch_pro对象
rag_with_baidu_search_pro = appbuilder.RagWithBaiduSearchPro(model="ERNIE Speed-AppBuilder")

# 运行rag_with_baidusearch基本组件
msg = appbuilder.Message("残疾人怎么办相关证件")
result = rag_with_baidu_search_pro.run(msg)

# 获取reference
references = result.extra

# 输出运行结果
print(result)
```

## 参数说明
### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
import os 

os.environ["APPBUILDER_TOKEN"] = "..."
```

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。
- `instruction (obj:Message, 可选)`: 可设定人设，如：你是问答助手，在回答问题前需要加上“很高兴为您解答：”


### 调用参数
调用参数中的 instruction 会覆盖初始化时的参数。

- `msg (obj:Message)`: 输入消息，包含用户提出的问题。这是一个必需的参数。
- `instruction (obj:Message, 可选)`: 可设定人设，如：你是问答助手，在回答问题前需要加上“很高兴为您解答：”
- `stream (bool, 可选)`: 指定是否以流式形式返回响应。默认为 False。
- `temperature (float, 可选)`: 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
- `top_p (float, 可选)`: 模型配置的top_p参数，top_p值越高输出文本越多样，top_p值越低输出文本越稳定。取值范围为 0.0 到 1.0，默认值为 1e-10。
- `search_top_k (int, 可选)`: 指定百度搜索返回的检索个数，最多10，默认为4。
- `hide_corner_markers (bool, 可选)`: 溯源开关，默认开。


### 返回值
- 返回一个 `Message` 对象，包含模型运行后的输出消息。


## 高级用法
该组件的高级用法包括定制化的输入处理、输出处理，以及更复杂的调用场景。用户可以根据具体需求扩展组件功能，实现个性化的问答系统。
包括如下功能：
1、人设
2、溯源
3、百度搜索检索个数


### 代码样例

```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch对象, 并初始化人设指令
rag_with_baidusearch_pro = appbuilder.RagWithBaiduSearchPro(
        model="ERNIE Speed-AppBuilder", 
        instruction=appbuilder.Message("你是问答助手，在回答问题前需要加上: 很高兴为您解答"))


# 运行rag_with_baidusearch组件，开启拒答、澄清追问、重点强调、友好性提升、溯源能力功能
msg = appbuilder.Message("残疾人怎么办相关证件")
result = rag_with_baidusearch_pro.run(
        msg, temperature=0.5, stream=False)

# 输出运行结果
print(result)
```

### 返回参数说明

返回的message中具体字段说明如下：

| 字段            | 字段说明   |
|---------------|--------|
| name          | 名称     | 
| mtype         | 类型     | 
| content       | 内容     |  
| extra         | 引用     | 
| +search_baidu | 百度搜索结果 |
| ++content     | 网页内容摘要 |
| ++url         | 网页链接   |
| ++ref_id      | 序号     |
| ++title       | 标题     |
| ++icon        | 网站图标   |
| ++site_name   | 网站名    |


### 典型返回样例
```
Message(name=msg, content=您好，请问您是想询问关于残疾人办理什么证件的问题吗？如果是，我可以为您提供一些信息。

首先，如果您是首次申请办理残疾人证，需要携带身份证、户口簿和三张两寸近期免冠白底彩色照片到县残联办证窗口提出申请。如果您因身体原因无法亲自前往，可以联系村（社区）工作人员代办申请。

其次，如果您是指残疾类型等级证明，您需要携带相关材料到指定医院或医生进行评级，并由医生签名盖章。

最后，如果您是指残疾人享受低保或残疾人贫困证的一级肢体、视力、智力、精神、多重及60周岁以上的一级听力、语言的重度残疾人可以享受重度残疾人生活补助，那么您需要携带身份证、户口本和残疾证申请表到县、市、区级残联进行办理。

希望这些信息对您有所帮助。如果您还有其他问题，欢迎随时提问。^[2]^, mtype=dict, extra={'search_baidu': [{'content': '(一)3张两寸近期免冠白底彩色照片。 (二)身份证、户口簿原件及复印件。 (三)申请智力、精神类残疾人证和未成年人申请残疾人证需同时提供法定监护人的身份证、户口本原件及复印件和监护人的证明材料。监护人证明材料为以下三项中任意一项: (1)能体现双方直系血缘亲属关系的户口簿。 (2)申请人所在村(社区)出具的说明双方关系的证明材料。 (3)其他能够证明其双方关系的合法证件。(法院判决书、结婚证、出生证明等) (四)经常居住地的有效居住证(户籍地不在本市申请人需提供此证件,本市户籍申请人无需提供此证件)。 (五)经常居住地残联要求的其他材料。 残疾证办理事项及流程', 'icon': 'https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1505232404,3530227258&fm=195&app=88&f=JPEG?w=200&h=200', 'url': 'https://www.jingzhou.gov.cn/ztfwnew/shjz/cjrbl/index.shtml', 'ref_id': '1', 'site_name': '荆州市人民政府', 'title': '残疾人证办理服务'}, {'content': '{#}申请{@}. 首次申请办理残疾人证人员,需持申请人居民身份证,户口簿和3张两寸近期免冠白底彩照,到县残联办证窗口(县政务服务中心一楼1号窗口)提出办证申请,填写《中华人民共和国残疾人证申请表》.如因身体原因个人无法出行办证,可联系村(社区)工作人员代办申请.', 'icon': None, 'url': 'https://mp.weixin.qq.com/s?__biz=MzIxMzM5ODY5OQ==&mid=2247485042&idx=1&sn=26a4cad0122d24971d3f5ce598af3564&chksm=97b623b6a0c1aaa02f776c19f567e0b3fabdef3d9f5c957e1f260f286fe5356101fd1ac4e675&scene=27', 'ref_id': '2', 'site_name': '微信公众平台', 'title': '残疾人证如何办理?到哪里评定?你想知道的都在这里'}, {'content': '一、残疾人如何办残疾证 1、户口所在地的县、市、区级残联领取《残疾人证申请表》和《残疾评定表》; 2、身份证或户口本复印件一张; 3、两寸彩色相片2-6张(多带不碍事,各地标准不一); 4、残疾类型等级证明。残疾很明显的可以直接到残联进行评级(像肢体类)审核办理,不明显的必须到指定医院、指定医生进行评级签名并盖章。 一切手续完备,就到县、市、区级残联进行办理,快的话立等可取,慢的话7-15天也差不多了。 二、残疾证有什么用? 1、持有残疾证的残疾人可享受低保或持残疾人贫困证的一级肢体、视力、智力、精神、多重及60周岁以上的一级听力、语言的重度残疾人,可享受重度残疾人生活补助。 2、残疾人托(安)养方面,一级重度残疾人(不含听力、语言、视力残疾)或18至60周岁二级重度残疾人(不含听力、语言、视力残疾),集中托养:低保户、贫困户的对象补助每年补助现金按各地政策规定金额发放。', 'icon': 'https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=215799447,688541359&fm=195&app=88&f=JPEG?w=200&h=200', 'url': 'https://mip.66law.cn/laws/1060751.aspx', 'ref_id': '3', 'site_name': '华律网', 'title': '残疾人如何办残疾证-证件办理|华律办事直通车'}]})
```
