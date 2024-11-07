# Appbuilder-SDK 自动文档生成

## 操作流程

- 完成SDK代码开发
- 依照google规范编写注释--仅需要对类和非私有方法进行注释
- 进入根目录的docs/sphinx_doc目录下执行update_doc.sh脚本
- 执行成功后，在docs/sphinx_doc/build/markdown目录下查看生成的文档是否无误
- 迁移所有生成的文档到docs/sphinx_md目录下

## 代码注释规范

- 注释使用google规范

### object类注释

```python
class AppBuilderClient(Component):
    r"""
    AppBuilderClient 组件支持调用在[百度智能云千帆AppBuilder](https://cloud.baidu.com/product/AppBuilder)平台上
    构建并发布的智能体应用，具体包括创建会话、上传文档、运行对话等。
    
    Examples:

    .. code-block:: python

        import appbuilder
        # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
        os.environ["APPBUILDER_TOKEN"] = '...'
        # 可在Console 应用页面获取
        app_id = "app_id"
        client = appbuilder.AppBuilderClient("app_id")
        conversation_id = client.create_conversation()
        file_id = client.upload_local_file(conversation_id, "/path/to/file")
        message = client.run(conversation_id, "今天你好吗？")
        # 打印对话结果
        print(message.content)
        
    """
```
- 注意
    - 注释必须使用 Examples:之后必须存在一行空行，.. code-block:: python之后也必须要有一行空行
    - code-block前为两点（..）之后为两个冒号(::)
    - 方法的示例注释与此规范相同

### 函数注释

- 私有函数如_recognize_w_post_process等无需按照规范注释函数

```python
@components_run_stream_trace
def tool_eval(
    self,
    name: str,
    streaming: bool,
    origin_query: str,
    **kwargs,
) -> Union[Generator[str, None, None], str]:
    """
    执行工具函数，通过调用底层接口进行动物识别。
    
    Args:
        name (str): 工具名
        streaming (bool): 是否流式返回结果，True 表示流式返回，False 表示一次性返回
        origin_query (str): 用户原始查询字符串
        **kwargs: 工具调用的额外关键字参数
    
    Returns:
        Union[Generator[str, None, None], str]: 动物识别结果。如果 streaming 为 True，则返回一个生成器，可以逐个返回识别结果；
                                                如果 streaming 为 False，则返回一个字符串，包含识别出的动物类别和相应的置信度信息。
    
    """
```

### google风格指南与规范示例

- Google详情见 [Google注释风格指南](https://google.github.io/styleguide/pyguide.html)
   

```python
class GoogleStyle:
    '''Google注释风格
    用 ``缩进`` 分隔，
    适用于倾向水平，短而简单的文档
    Attributes:
        dividend (int or float): 被除数
        name (:obj:`str`, optional): 该类的命名
    '''
 
    def __init__(self, dividend, name='GoogleStyle'):
        '''初始化'''
        self.dividend = dividend
        self.name = name
 
    def divide(self, divisor):
        '''除法
        Google注释风格的函数，
        类型主要有Args、Returns、Raises、Examples
        Args:
            divisor (int):除数
        Returns:
            除法结果
        Raises:
            ZeroDivisionError: division by zero
        Examples:
        
        .. code-block:: python
        
            # 实例代码
            
        References:
            除法_百度百科  https://baike.baidu.com/item/%E9%99%A4%E6%B3%95/6280598
        '''
        try:
            return self.dividend / divisor
        except ZeroDivisionError as e:
            return e
```
