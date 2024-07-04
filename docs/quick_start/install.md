# AppBuilder-SDK 安装

### Python
> 执行如下命令，快速安装Python语言的最新版本AppBuilder-SDK（要求Python >= 3.9)。

```shell
pip install --upgrade appbuilder-sdk
```
如果在本地无法跑通appbuilder-sdk包，也可以使用我们的官方镜像来安装和运行，具体方案参考**二次开发**部分。

### Java (仅支持调用端到端应用)
> 使用AppBuilder Java ConsoleSDK要求Java版本>=8
#### Maven
在pom.xml的dependencies中添加依赖
```xml
<dependency>
    <groupId>com.baidubce</groupId>
    <artifactId>appbuilder</artifactId>
    <version>0.9.0</version>
</dependency>
```
#### Gradle
对于Kotlin DSL，在build.gradle.kts的dependencies中添加依赖
```kotlin
implementation("com.baidubce:appbuilder:0.9.0")
```
对于Groovy DSL，在build.gradle的dependencies中添加依赖
```groovy
implementation 'com.baidubce:appbuilder:0.9.0'
```
#### 本地导入
点击[链接](https://repo1.maven.org/maven2/com/baidubce/appbuilder/0.9.0/appbuilder-0.9.0.jar) 下载Jar包，将Jar包导入到项目目录下。

### Go (仅支持调用端到端应用)
> 支持Go 1.18.1以上版本

```shell
go get github.com/baidubce/app-builder/go/appbuilder
````

### Docker (当前仅集成了Python版本AppBuilder-SDK)
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.9.0
```
