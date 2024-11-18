# AppBuilder SDK 运行环境超参配置说明

## 运行超参

- `APPBUILDER_TOKEN`
    - 超参说明：设置当前运行环境的用户Token，用于所有接口的鉴权
    - 默认值： 空字符串
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序

- `SECRET_KEY_PREFIX`
    - 超参说明：设置当前运行环境中AppBuilder组件（Component）的密钥前缀，SDK会自动组装最终的密钥为 `{SECRET_KEY_PREFIX} {APPBUILDER_TOKEN}`的形式，用于发起HTTP请求。常用于私有化部署的场景。
    - 默认值： `Bearer`
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序

- `GATEWAY_URL`
    - 超参说明：设置当前运行环境中AppBuilder组件（Component）网关的URL
    - 默认值： `https://appbuilder.baidu.com` 
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的基础组件调用请求

- `GATEWAY_URL_V2`
    - 超参说明：设置当前运行环境中AppBuilder OpenAPI的URL
    - 默认值： `https://qianfan.baidubce.com`
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的端到端应用 及 OpenAPI能力的调用
    - 注意事项：当前该参数影响以下接口
        - `AppBuilderClient SDK` 所有接口
        - `KnowledgeBase SDK` 所有接口 

- `CONSOLE_OPENAPI_PREFIX`
    - 超参说明：设置当前运行环境中AppBuilder OpenAPI的URL前缀，体现在`https://qianfan.baidubce.com/{custom_prefix}/v2/app/conversation`中的`{custom_prefix}`字段。常用于私有化部署的场景。
    - 默认值： 空字符串
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的端到端应用 及 OpenAPI能力的调用
    - 注意事项：当前该参数影响以下接口
        - `AppBuilderClient SDK` 所有接口
        - `KnowledgeBase SDK` 所有接口 

- `CONSOLE_OPENAPI_VERSION`
    - 超参说明：设置当前运行环境中AppBuilder OpenAPI的版本，体现在`https://qianfan.baidubce.com/{custom_prefix}/v2/app/conversation`中的`/v2`字段。常用于私有化部署的场景。
    - 默认值： `v2`
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的端到端应用 及 OpenAPI能力的调用
    - 注意事项：当前该参数影响以下接口
        - `AppBuilderClient SDK` 所有接口
        - `KnowledgeBase SDK` 所有接口 



### 运行超参使用Tips
- 私有化环境部署时，需要同时设置私有化部署的网关地址：`GATEWAY_URL`和`GATEWAY_URL_V2`，且需要使用在私有化环境中可以鉴权的用户Token：`APPBUILDER_TOKEN`与`SECRET_KEY_PREFIX`


## 调试超参

- `APPBUILDER_LOGLEVEL`
    - 超参说明：设置AppBuilder运行的日志级别，可选值：`DEBUG`, `INFO`, `WARNING`, `ERROR`
    - 默认值： INFO
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序的日志级别
    - 注意事项：`APPBUILDER_LOGLEVEL`生效于`import appbuilder`时，若期望该参数生效，可使用`appbuilder.logger.setLoglevel("DEBUG")`方法设置
    ```python
    import appbuilder # NOQA 
    appbuilder.logger.setLoglevel("DEBUG") # NOQA
    ```


- `APPBUILDER_LOGFILE`
  - 超参说明：设置AppBuilder运行的日志文件路径，最好是绝对路径
  - 默认值；空
  - 注意事项：`APPBUILDER_LOGFILE`生效于`import appbuilder`时，若期望该参数生效，可使用`appbuilder.logger.setLogFile("")`方法设置
  ```python
  import appbuilder # NOQA 
  appbuilder.logger.setFilename("/tmp/appbuilder.log") # NOQA
  ```