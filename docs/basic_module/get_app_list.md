# 获取AppBuilder已发布的应用列表

## 简介
该接口可获取用户在 AppBuilder已发布的应用列表，包括模型名称、模型描述、模型的ID

## Python基本用法

### 获取app_list接口 `appbuilder.get_app_list()`

#### 鉴权配置
使用组件之前，请首先申请并设置鉴权参数，可参考[组件使用流程](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5)。
```python
# 设置环境中的TOKEN，以下示例略
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

#### 初始化参数

| 参数名称       | 参数类型   | 描述      | 示例值        |
|------------|--------|---------|------------|
| limit | int | 返回结果的最大数量，默认值为10, 最大值为100 | 10 |
| after | str | 分页游标，返回结果中第一个应用的游标值，接口会返回该应用及之后的应用，用于分页查询。默认值为空字符串。 | app_id |
| before | str | 返回结果中最后一个应用的游标值，与after原理一致，用于分页查询。默认值为空字符串。 | app_id |

#### 返回参数

`get_app_list`方法返回类型为 `list[AppOverview]`,其中 `AppOverview` 结构如下：

```python
class AppOverview(BaseModel):
    id: str = Field("", description="应用ID")
    name: str = Field("", description="应用名称")
    description: str = Field("", description="应用简介")
```


#### 代码示例
下面是模型列表获取功能的代码示例：

```python
import os
import appbuilder
# 设置环境变量和初始化
# 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
os.environ["APPBUILDER_TOKEN"] = "..."
app_list = appbuilder.get_app_list()
print(app_list)
```

返回值为

```shell
[AppOverview(id='e97865e7-e1be-45d3-ab8a-ea84ca6e0b9a', name='二次元风格图片生成助手', description='生成二次元风格图片，一键生成你的专属动漫风格作品'), AppOverview(id='982aaa98-60d4-4120-b4ab-3404a95a61e1', name='智能客服机器人', description='智能回答文字问题，解析程序报错并给出建议'), AppOverview(id='c59cb95b-8c42-4102-8582-df07bde8d4cc', name='招聘海报大师', description='一键生成招聘海报，高效宣传职位需求'), AppOverview(id='42eb211a-14b9-43d2-9fae-193c8760ef26', name='地理小达人', description='提供地理知识解答，如地名由来、地形地貌等。')]
```

## Java基本用法

#### 接口参数及返回值
与 `python appbuilder.get_app_list()`设计一致

#### 代码示例

```java
public void GetAppsTest() throws IOException, AppBuilderServerException {
    AppList builder = new AppList();
    AppListRequest request = new AppListRequest();
    request.setLimit(10);
    assertNotNull(builder.getAppList(request)[0].getId());
}
```

## Go基本用法

#### 接口参数及返回值
与 `python appbuilder.get_app_list()`设计一致

#### 代码示例

```go
package appbuilder

apps, err := GetAppList(GetAppListRequest{
    Limit: 10,
}, config)
if err != nil {
    t.Fatalf("get apps failed: %v", err)
}
fmt.Println(len(apps))
```

## 高级用法

目前该模块提供获取AppBuilder已发布应用的功能，获取的应用ID，可以配合`AppBuilderClient` SDK进行应用调用。


## 更新记录和贡献
* 千帆模型列表获取能力 (2024-7)