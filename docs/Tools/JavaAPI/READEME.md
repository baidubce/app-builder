# Appbuilder-SDK Java 自动文档生成

## 操作流程

- 完成SDK代码开发
- 依照google规范编写注释--仅需要对类和非私有方法进行注释
- 进入根目录的docs/Tools/JavaAPI目录下执行java_api_update.sh脚本

## 脚本功能

- 依据注释自动生成文档，并将文档迁移到docs/API-Reference/Java目录下

## 代码注释规范

### 基本格式

Javadoc注释是用/**开始，用\*/结束的，位于类、方法或字段之前。例如

```java
/**
 * 这是一个用于演示的类。
 */
public class Demo {
}
```

### 类和接口注释

对于类和接口，Javadoc注释应该解释其整体功能和用途，以及如何与其他类或接口交互

```java
/**
 * 这是一个计算工具类，提供静态方法来进行数学计算。
 */
public class MathUtils {
    // ...
}
```

### 方法注释

每个公共和受保护的方法应该有Javadoc注释，说明方法的作用、参数、返回值以及可能抛出的异常。

- `@param` 用来描述参数
- `@return` 描述返回值（如果方法不返回任何内容，则不需要此标签）
- `@throws` 或 `@exception` 描述可能抛出的异常

```java
/**
 * 计算两个整数的和。
 *
 * @param a 第一个整数
 * @param b 第二个整数
 * @return 两个整数的和
 */
public static int add(int a, int b) {
    return a + b;
}
```

### 字段注释

公共字段应有简短的注释说明其作用。如果字段的用途不是显而易见的，应该提供详细的描述。

```java
/**
 * 默认的错误消息。
 */
public static final String DEFAULT_ERROR_MESSAGE = "An error occurred.";
```

### 通用标签

除了上述特定标签外，Javadoc还支持以下一些通用标签：

- `@see` 参考其他相关类、方法或文档
- `@since` 指明从哪个版本开始添加的
- `@version` 标明当前代码的版本
- `@deprecated` 指明方法或类不再推荐使用

```java
/**
 * @deprecated 由于安全问题，此方法从版本1.5开始不推荐使用。
 */
@Deprecated
public void oldMethod() {
    // ...
}
```

