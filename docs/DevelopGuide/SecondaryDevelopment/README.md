# 开发指引

该文档目录包含以下内容：

- [二次开发基本介绍](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/SecondaryDevelopment/README.md)
- [AppBuilder SDK 运行环境超参配置说明](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/EnvironmentalParameters/env.md)


## 二次开发
当前已集成Python版本AppBuilder-SDK 0.9.4及相关依赖，方便开发者融入个人已有的大模型应用程序。此部分仍在不断建设中。
二次开发可以采用官方提供的开发镜像，便于快速安装各种依赖库。也可在镜像中使用已安装的`appbuilder_trace_server`、`appbuilder_bce_deploy`工具。
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.9.8
```