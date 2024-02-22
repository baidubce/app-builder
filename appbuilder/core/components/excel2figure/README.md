# Excel2Figure

## 简介
Excel转图表（Excel2Figure）组件通过理解对表格信息的提问，生成对应语义的图表。

### 功能介绍
Excel2Figure 是一个高级的数据可视化工具，它结合了大语言模型的强大语义理解能力，以帮助用户将 Excel 表格数据转换成直观、易理解的图表。用户只需通过自然语言描述他们想要呈现的数据和图表类型，Excel2Figure 会解析这些指令，自动从Excel数据中提取相关信息，生成符合用户需求的图表。

### 特色优势
- 强大的语义理解：利用文心一言大语言模型的先进技术，Excel2Figure能够理解复杂的自然语言指令，包括数据筛选、分析需求和图表类型等。
- 用户友好的交互：用户可以用自己熟悉的语言描述数据可视化需求，无需学习复杂的软件操作或编程语言。
- 支持多样化的图表类型：根据用户的自然语言描述，Excel2Figure能够生成多种类型的图表，包括但不限于柱状图、线形图、饼图、散点图等。
- 快速准确的数据处理：通过语义理解快速定位和处理Excel中的数据，大大减少了数据准备的时间和出错的可能性。

### 应用场景
- 学术研究：研究人员可以简单描述他们需要的图表类型和数据集，Excel2Figure将帮助他们将研究数据可视化，以便在学术论文或演讲中展示。
- 市场趋势分析：市场分析师利用Excel2Figure快速生成展示市场调查结果和消费者行为分析的图表，帮助团队理解市场动态。
- 教育用途：教师可以利用这个工具将复杂的数据集转换为学生更容易理解的图表，提高教学效果和学生的学习兴趣。
- 个人数据管理和展示：个人用户可以使用Excel2Figure来跟踪和展示自己的财务状况、健康数据或任何其他类型的个人记录。


## 基本用法

### 快速开启

```python
import appbuilder
import os

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = '...'

# 创建 component 对象，推荐使用 ERNIE-Bot 4.0 获取更稳定的画图效果
component = appbuilder.Excel2Figure(model="ERNIE-Bot 4.0")

# 准备 excel 文件链接，该链接需要是公网可访问的地址
excel_file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/[测试]超市收入明细表格.xlsx?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T09%3A51%3A14Z/-1/host/1802a9c9142ef328d61e7673db7c1f05842b2af93d18a02ac7ef7aa6f64db54e"

# 针对 excel 文件内容绘制图表
result = component.run(appbuilder.Message({
    "query": "2020年各个月份的利润分别是多少？使用条形图绘制出来",
    "excel_file_url": excel_file_url,
}))

# 输出运行结果
print(result)
# Message(name=msg, content="http://可访问的文件地址...", mtype=str)
```

如果绘图成功，预期结果为一个可访问的文件地址，文件链接**过期时间限制为24小时**；如果绘图失败，预期结果为空字符串，需要调整query。

这里给出上述代码运行得到的图表（每次运行结果可能会发生变化，仅供参考）：
![2020年各个月份利润条形图.png](https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/%5B%E6%B5%8B%E8%AF%95%5D2020%E5%B9%B4%E5%90%84%E4%B8%AA%E6%9C%88%E4%BB%BD%E5%88%A9%E6%B6%A6%E6%9D%A1%E5%BD%A2%E5%9B%BE.png?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T10%3A00%3A16Z/-1/host/b68f35825ad99075caf8bd009e4871ee9eb7b718e550968fdf12695b1502bc78)


## 参数说明

### 初始化参数
- `model`: 模型名称，用于指定要使用的千帆模型。

### 调用参数
| 参数名称 | 参数类型 | 是否必须 |描述 | 示例值 |
|--------|--------|---|----|------------------------------------------|
| msg | Message | 是 | 输入消息，包含用户提出的问题 query 和一个公网可访问的 excel 文件链接 excel_file_url。| Message({"query": "2020年各个月份的利润分别是多少？使用条形图绘制出来", "excel_file_url": "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/[测试]超市收入明细表格.xlsx?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T09%3A51%3A14Z/-1/host/1802a9c9142ef328d61e7673db7c1f05842b2af93d18a02ac7ef7aa6f64db54e"}) |

### 响应参数
| 参数名称 | 参数类型 | 描述 | 示例值 |
|--------|--------|----|------|
| result | Message | 返回结果。如果图表绘制成功，则会返回一个可下载的图片链接，有效期为24小时；如果绘制失败，则会返回空字符串。 | Message(name=msg, content="https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/%5B%E6%B5%8B%E8%AF%95%5D2020%E5%B9%B4%E5%90%84%E4%B8%AA%E6%9C%88%E4%BB%BD%E5%88%A9%E6%B6%A6%E6%9D%A1%E5%BD%A2%E5%9B%BE.png?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T10%3A00%3A16Z/-1/host/b68f35825ad99075caf8bd009e4871ee9eb7b718e550968fdf12695b1502bc78", mtype=str)|

### 响应示例
```shell
Message(name=msg, content="https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/%5B%E6%B5%8B%E8%AF%95%5D2020%E5%B9%B4%E5%90%84%E4%B8%AA%E6%9C%88%E4%BB%BD%E5%88%A9%E6%B6%A6%E6%9D%A1%E5%BD%A2%E5%9B%BE.png?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-02-21T10%3A00%3A16Z/-1/host/b68f35825ad99075caf8bd009e4871ee9eb7b718e550968fdf12695b1502bc78", mtype=str)
```

### 错误码
无

## 更新记录和贡献
* Excel转图表 (2024-02)