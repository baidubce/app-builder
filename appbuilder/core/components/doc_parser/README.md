# 文档解析（DocParser）

## 简介
文档解析组件（DocParser）可以用于文档内容解析，支持PDF、JPG、DOC、TXT、XLS、PPT等16种文档格式的内容解析。

### 功能介绍
文档解析组件（DocParser）支持从文档中解析出文档字符内容、版式信息、位置坐标、表格结构、阅读顺序、标题段落层级树等内容

### 特色优势
DocParser支持解析以下几种类型的文档：
* 版式文档：「pdf」、「jpg」、「jpeg」、「png」、「bmp」、「tif」、「tiff」、「ofd」
* 流式文档：「doc」、「docx」、「txt」、「xls」、「xlsx」、「wps」、「ppt」、「pptx」

支持解析的文档内容包括：
* 文档的版式分析，识别文档中的标题、正文、页眉页脚、表格等
* 文档内的文字内容、位置坐标
* 表格结构和内容
* 构建文档标题段落层级树
* 构建文档阅读顺序
* 支持以上类型文档转成pdf格式

### 应用场景
* 文档内容解析
* 文档版式解析
* 文档格式转化

## 基本用法

以下是使用DocParser快速开始的一个示例：

```python
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.message import Message
import os
import requests

# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."

# 进行文档内容解析
file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/test.pdf?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-01-25T12%3A56%3A15Z/-1/host/b54178fea9be115eafa2a8589aeadfcfaeba20d726f434f871741d4a6cb0c70d"
file_data = requests.get(file_url).content
file_path = "./test.pdf"  # 待解析的文件路径
with open(file_path, "wb") as f:
    f.write(file_data)
msg = Message(file_path)
parser = DocParser()
parse_result = parser(msg)
print(parse_result.content)
```

## 参数说明

### 鉴权说明
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```
### 初始化参数
无

### 调用参数
| 参数名称       |参数类型 |是否必须 | 描述          | 示例值  |
|------------|--------|--------|-------------|------|
| message    |String  |是 | 需要解析的文档的存储路径 | "./test.pdf" |
| return_raw |bool|否 | 指定是否返回原始的解析结果结构，默认为 False。 | True |

### 响应参数
| 参数名称        |参数类型 | 描述   | 示例值                     |
|-------------|--------|------|-------------------------|
| parseResult |Message  | 解析结果 | ParseResult对象，包含文档解析的内容 |
### 响应示例
```python
class ParseResult(BaseModel):
    """
    解析结果整体结构
    """
    para_node_tree: Optional[List[ParaNode]] = []  # 标题段落层级树，当ParserConfig.return_para_node_tree为True时有内容
    page_contents: Optional[List[PageContent]] = []  # 页面的解析内容，详细内容参考base.py中的PageContent类
    pdf_data: Optional[str] = "" # pdf格式数据, 当ParserConfig.convert_file_to_pdf为True时有内容
    raw: Optional[Dict] = {} # 云端服务的原始解析结果
```

## 高级用法
DocParser支持自定义文档解析的配置和对解析结果进行二次处理，以下是一个示例：

```python
from appbuilder.core.components.doc_parser.doc_parser import DocParser
from appbuilder.core.message import Message
import os
import requests

# 设置环境变量
os.environ["APPBUILDER_TOKEN"] = "..."

# 先进行文档内容解析
file_url = "https://agi-dev-platform-bos.bj.bcebos.com/ut_appbuilder/test.pdf?authorization=bce-auth-v1/e464e6f951124fdbb2410c590ef9ed2f/2024-01-25T12%3A56%3A15Z/-1/host/b54178fea9be115eafa2a8589aeadfcfaeba20d726f434f871741d4a6cb0c70d"
file_data = requests.get(file_url).content
file_path = "./test.pdf"  # 待解析的文件路径
with open(file_path, "wb") as f:
    f.write(file_data)
msg = Message(file_path)

parser = DocParser()
config = parser.config
config.convert_file_to_pdf = True  # 指定将当前文件转换成pdf格式
config.page_filter = [0, 2]  # 只解析第1页和第3页，注意：页码从0开始

parse_result = parser(msg)
file_content = parse_result.content
pdf_data = file_content.pdf_data  # 获取原始文件转化成pdf之后的数据
page_content = file_content.page_content[1]  # 获取第3页的解析结果
page_table = page_content.tables[0]  # 第3页中第一个表格的解析结果（如有），表格的解析内容的结构详见上一章详细说明部分关于表格结果的说明
cells = page_table.cells  # 表格的单元格信息
cell_text = cells[0]  # 表格第一个单元格的文本内容
matrix = page_table.cell_matrix  # 表格的单元格矩阵，用来描述单元格的空间位置信息
...
自定义处理表格内容
...
```
### 高级用法参数详细说明

在base.py中定义了DocParser配置和结果结构，下面做一些详细的说明和解释：
### DocParser配置
```python
class ParserConfig(BaseModel):
    """
    DocParser解析配置
    """
    convert_file_to_pdf: bool = Field(alias="need_pdffile_data", default=False) #  是否需要将当前文件转换成pdf格式
    page_filter: List[int] = Field(alias="page_filter", default=None) #  指定解析的页码，默认传None，代表全部解析
    return_para_node_tree: bool = Field(alias="return_para_nodes", default=True) #  是否需要返回标题段落层级树
    erase_watermark: bool = Field(alias="erase_watermark", default=False) #  解析的过程中是否需要去除水印的干扰
```
### DocParser解析结果
```python
class ParseResult(BaseModel):
    """
    解析结果整体结构
    """
    para_node_tree: Optional[List[ParaNode]] = []  # 标题段落层级树，当ParserConfig.return_para_node_tree为True时有内容
    page_contents: Optional[List[PageContent]] = []  # 页面的解析内容，详细内容参考base.py中的PageContent类
    pdf_data: Optional[str] = "" # pdf格式数据, 当ParserConfig.convert_file_to_pdf为True时有内容
    raw: Optional[Dict] = {} # 云端服务的原始解析结果

class ParaNode(BaseModel):
    """
    文档内容层级树结构
    """
    node_id: int # 标题段落层级树的节点id
    text: str # 节点文本
    para_type: str # 节点类型，包括：title、text、table
    parent: Optional[int] # 父节点id，文本的父节点是标题，标题的父节点是更高一级的标题
    children: List[int] # 子节点id列表，标题节点才会有子节点
    position: List[Position] # 节点位置信息，包括：页码和在对应页面的位置坐标
    table: Optional[Table] = None # 节点类型为table时，包含表格解析结果

class PageContent(BaseModel):
    """
    单页文档内容结构
    """
    page_num: int # 页码
    page_width: int # 页面宽度
    page_height: int # 页面高度
    page_angle: int # 页面旋转角度
    page_type: str # 页面类型
    page_layouts: List[Layout] # 页面版式信息
    titles: Optional[List[Layout]] = [] # 页面标题信息
    tables: Optional[List[Table]] = [] # 页面表格信息

class Layout(BaseModel):
    """
    layout结构
    """
    type: str # 布局类型
    text: str # 布局文本
    box: List[int] # 布局位置信息，包括：左上角x、y坐标和宽高
    node_id: int # 布局在标题层级树中的节点id

class Table(BaseModel):
    """
    表格结构
    """
    box: List[int] # 表格位置信息，包括：左上角x、y坐标和宽高
    cells: List[Layout] = Field(alias="children") # 表格单元格信息，列表形式
    matrix: List[List[int]] # 表格单元格矩阵，用来描述单元格的空间位置信息
    node_id: int # 表格在标题层级树中的节点id
```
表格解析结构说明, 以下图为例：

![表格](https://bj.bcebos.com/v1/appbuilder-sdk-components/table.png?authorization=bce-auth-v1%2FALTAKGa8m4qCUasgoljdEDAzLm%2F2024-05-30T03%3A09%3A32Z%2F-1%2Fhost%2Fb36695708e047713b5fe17b49733228aecdaf46322a5cec8d4e7bd0989032197)

```python
# cells中一共有26个元素，matrix中的每一个元素代表单元格在cells中的索引
cells = [{"box": [90, 376, 21, 10], "type": "cell", "text": "序号", "node_id": 1}, ...]
matrix = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15],
        [16, 17, 18, 19],
        [20, 21, 22, 23],
        [24, 24, 25, 26]
    ]
```


## 更新记录和贡献
* 文档解析能力 (2023-12)