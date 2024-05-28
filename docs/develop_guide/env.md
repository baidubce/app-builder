# AppBuilder SDK 运行环境超参配置说明

## 运行超参

- `APPBUILDER_TOKEN`
    - 超参说明：设置当前运行环境的用户Token，用于所有接口的鉴权
    - 默认值： 空字符串
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序


- `GATEWAY_URL`
    - 超参说明：设置当前运行环境中AppBuilder组件（Component）网关的URL
    - 默认值： `https://appbuilder.baidu.com` 
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的基础组件调用请求

- `GATEWAY_URL_V2`
    - 超参说明：设置当前运行环境中AppBuilder 端到端应用（AppBuilderClient）网关以及OpenAPI的URL
    - 默认值： `https://qianfan.baidubce.com`
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序中的端到端应用 及 OpenAPI能力的调用
    - 注意事项：当前该参数影响以下接口
        - 接口：`AppBuilderClient.create_conversation`
        - 接口：`AppBuilderClient.upload_local_file`
        - 接口：`AppBuilderClient.run`

### 运行超参使用Tips
- 私有化环境部署时，需要同时设置私有化部署的网关地址：`GATEWAY_URL`和`GATEWAY_URL_V2`，且需要使用在私有化环境中可以鉴权的用户Token：`APPBUILDER_TOKEN`


## 调试超参

- `APPBUILDER_LOGLEVEL`
    - 超参说明：设置AppBuilder运行的日志级别，可选值：`DEBUG`, `INFO`, `WARNING`, `ERROR`
    - 默认值： INFO
    - 影响范围：当前终端（Terminal）运行的所有AppBuilder程序的日志级别
    - 注意事项：`APPBUILDER_LOGLEVEL`生效于`import appbuilder`时，若期望该参数生效，需要在`import appbuilder`之前设置
    ```python
    import os # NOQA
    os.environ['APPBUILDER_LOGLEVEL'] = 'DEBUG' # NOQA
    import appbuilder # NOQA 
    ```