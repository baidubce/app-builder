# RAG With BaiduSearch

## 简介
RAG with BaiduSearch是基于生成式大模型的问答组件，使用百度搜索引擎检索候选文本进行检索增强。

## 基本用法

### 快速开启

```python
import appbuilder
import os
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch对象
rag_with_baidusearch_component = appbuilder.RAGWithBaiduSearch(model="eb-turbo-appbuilder")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)

# 模拟运行rag_with_baidusearch基本组件
result = rag_with_baidusearch_component.run(msg)

# 获取reference
references = result.extra

# 输出运行结果
print(result)
```




## 参数说明

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数

- `msg (obj:Message)`: 输入消息，包含用户提出的问题。这是一个必需的参数。
- `instruction (obj:Message, 可选)`: 可设定人设，如：你是问答助手，在回答问题前需要加上“很高兴为您解答：”
- `reject (bool, 可选)`: 拒绝开关，如果为 True，则启用该能力。默认为 False。当输入的问题在搜索结果中没有找到答案时，开关开启时，模型会用特定话术("当前文档库找不到对应的答案，我可以尝试用我的常识来回答你。")做回复的开头，并后接自有知识做回复内容。
- `clarify (bool, 可选)`: 澄清开关，如果为 True，则启用该能力。默认为 False。 当输入的问题比较模糊、或者主体指代不清晰，且context_list中包含有可以回答该模糊问题的多种潜在备选答案时，开启该开关，大模型会以特定的话术做澄清反问，引导用户继续补充问题发问。举例子，query:发电机的续航时间？ Answer: 根据搜索结果得到了xx和xx两种型号的发电机，您的问题具体涉及到哪一个？请补充关键信息，作为完整的问题重新发问。
- `highlight (bool, 可选)`: 重点强调开关，如果为 True，则启用该能力。默认为 False。开启该功能时，回复结果中会高亮显示关键部分的内容。
- `friendly (bool, 可选)`: 友好性提升开关，如果为 True，则启用该能力。默认为 False。开关开启时，部分回复的开头会加礼貌用语。且如果回答涉及到大段的信息，会倾向于以<总-分>或者<总-分-总>的形式做分点论述，使得答案的格式更规整，可读性更强。
- `cite (bool, 可选)`: 溯源开关，如果为 True，则启用该能力。默认为 False。开关开启时，回复内容后会使用引用标记来标注回答内容参考的搜索结果序号，如^[1]^ (引用单个搜索结果）,^[1][2]^（引用多个搜索结果）。例如：按照当地公安机关出入境管理部门规定的其他材料办理^[2]^。
- `stream (bool, 可选)`: 指定是否以流式形式返回响应。默认为 False。
- `temperature (float, 可选)`: 模型配置的温度参数，用于调整模型的生成概率。取值范围为 0.0 到 1.0，其中较低的值使生成更确定性，较高的值使生成更多样性。默认值为 1e-10。
- `top_p (float, 可选)`: 模型配置的top_p参数，top_p值越高输出文本越多样，top_p值越低输出文本越稳定。取值范围为 0.0 到 1.0，默认值为 1e-10。
- 
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
6、人设


### 代码样例

```python
import appbuilder
import os

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建rag_with_baidusearch对象
rag_with_baidusearch_component = appbuilder.RAGWithBaiduSearch(model="eb-turbo-appbuilder")

# 初始化参数
msg = "残疾人怎么办相关证件"
msg = appbuilder.Message(msg)

# 模拟运行rag_with_baidusearch组件，开启拒答、澄清追问、重点强调、友好性提升、溯源能力、人设六个功能
instruction = "你是问答助手，在回答问题前需要加上“很高兴为您解答："
instruction = appbuilder.Message(instruction)
result = rag_with_baidusearch_component.run(msg, reject=True, clarify=True, highlight=True,
                                            friendly=True, cite=True, temperature=0.5, stream=False,
                                            instruction=instruction)

# 输出运行结果
print(result)
```

### 返回参数说明

extra字段：

| 字段      | 字段说明   |
|---------|--------|
| content | 网页内容摘要 |
| id      | 网页链接   |
| mock_id | 序号     |
| title   | 标题     |


### 典型返回样例
Message(name=msg, content=你好，根据搜索结果得到了**办理残疾人证**^[1]^和**申请智力、精神类残疾人证和未成年人申请残疾人
证须知**^[2]^两个相关内容。 您的问题具体涉及到哪一个？请补充关键信息，作为完整的问题重新发问。, mtype=dict, 
extra={'search_baidu': [{'content': '一、如何办理残疾人证? (一)残疾人的定义 根据全国人大常委会关于1990年12月28日通过的
《中华人民共和国残疾人保障法》第二条的规定:残疾人是指在心理、生理、人体结构上,某种组织、功能丧失或者不正常,
全部或者部分丧失以正常方式从事某种活动能力的人。 残疾人包括视力残疾、听力残疾、言语残疾、肢体残疾、智力残疾、精神残疾、
多重残疾和其他残疾的人。 (二)如何办理残疾人证 第二代残疾人证件号为20位数字,前18位为身份证号,后2位编号则为残疾类型+等级,
具体如下:视力残疾为1,听力残疾为2,言语残疾为3,肢体残疾为4,智力残疾为5,精神残疾为6,多重残疾:存在2项或2项以上残疾,编号为7;
结尾等级分为1,2,3,4级。例如:视力2级,则残疾证号为:X12,(X代表某人18位身份证号) 现场办理残疾人证需要提供四份材料:(1)申请人提出申请,
在县残联办证窗口领取办理残疾证的申请表;(2)身份证或户口簿复印件;(3)相关的病历材料;(4)二寸近期彩照4张。 
申请后县残联组织医疗鉴定机构(医院)进行鉴定,县残联办证窗口医疗鉴定机构进行残疾人现场评残鉴定的时间是每周二。
县残联办证窗口位于县政务服务中心一楼(户籍大厅旁)。 残疾证补办需向县残联申请补发。 视力类残疾人证是红色证件,其余为绿色证件。 
二、残疾人类别等级评定标准 一、视力残疾标准 (一)视力残疾的定义 视力残疾,是指由于各种原因导致双眼视力低下并且不能矫正或视野缩小,
以致影响其日常生活和社会参与。 视力残疾包括盲及低视力。 (二)视力残疾的分级 类别 级别 最佳矫正视力 盲 一级 无光感～<0.02;
或视野半径<5度 二级0.02～<0.05;或视野半径<10度 低视力 三级 0.05～<0.1 四级0.1～<0.3 〔注〕 
1.盲或低视力均指双眼而言,若双眼视力不同,则以视力较好的一眼为准。如仅有单眼为盲或低视力,而另一眼的视力达到或优于0.3,则不属于视力残疾范畴。 
2.最佳矫正视力是指以适当镜片矫正所能达到的最好视力,或针孔视力。 3.以注视点为中心,视野半径<10度者,不论其视力如何均属于盲。', 
'doc_id': 'https://www.linquan.gov.cn/xxgk/detail/5af2e3f14daee31b7679c579.html', 
'id': 'https://www.linquan.gov.cn/xxgk/detail/5af2e3f14daee31b7679c579.html', 'mock_id': '1', 
'title': '解读如何办理残疾人证及残疾评定标准-临泉县人民政府', 'type': 'web'}, 
{'content': '申请智力、精神类残疾人证和未成年人申请残疾人证须同时提供法定监护人的证明材料。有条件的地方可开展网上办理申请。', 
'doc_id': 'https://mp.weixin.qq.com/s?__biz=MzIxOTQ2MTc4Mg==&mid=2247496262&idx=5&sn=
9e91ef70653bb166afc3ab134e93669e&chksm=97d853bfa0afdaa9456aa28c549729085093f51138e9ae57399aaf99c1f7855ad63e2cc58b71
&scene=27', 'id': 'https://mp.weixin.qq.com/s?__biz=MzIxOTQ2MTc4Mg==&mid=2247496262&idx=5&sn=
9e91ef70653bb166afc3ab134e93669e&chksm=97d853bfa0afdaa9456aa28c549729085093f51138e9ae57399aaf99c1f7855ad63e2cc58b71
&scene=27', 'mock_id': '2', 'title': '残疾人证怎么办理?流程来了,请转给需要的人!', 'type': 'web'}]})



