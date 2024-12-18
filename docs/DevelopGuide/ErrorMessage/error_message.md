# SDK 错误信息

1、 `BaseRPCException`

- 报错解释: 
    - Base RPC exception，
    - SDK基类异常

2、 `BadRequestException`

- 报错解释: 
    - BadRequestException represent HTTP Code 400
    - BadRequestException 表示请求错误，错误码为400

3、 `ForbiddenException`

- 报错解释: 
    - ForbiddenException represent HTTP Code 403
    - ForbiddenException 表示禁止访问，错误码为403

4、 `NotFoundException`

- 报错解释: 
    - NotFoundException represent HTTP Code 404
    - NotFoundException 表示资源不存在，错误码为404

5、 `PreconditionFailedException`

- 报错解释: 
    - PreconditionFailedException represent HTTP Code 412
    - PreconditionFailedException 表示前置条件失败，错误码为412

6、 `InternalServerErrorException`

- 报错解释: 
    - InternalServerErrorException represent HTTP Code 500
    - InternalServerErrorException 表示内部服务器错误，错误码为500


7、 `HTTPConnectionException`

- 报错解释: 
    - HTTPConnectionException represent HTTP Connection error
    - HTTPConnectionException 表示HTTP连接错误

8、 `ModelNotSupportedException`

- 报错解释: 
    - ModelNotSupportedException represent model is not supported
    - ModelNotSupportedException 表示模型不支持

9、 `TypeNotSupportedException`

- 报错解释: 
    - TypeNotSupportedException represent type is not supported
    - TypeNotSupportedException 表示类型不支持

10、 `AppBuilderServerException`

- 报错解释: 
    - AppBuilderServerException represent backend server failed response
    - AppBuilderServerException 表示后端服务器响应失败

11、 `AssistantServerException`

- 报错解释: 
    - AssistantSercerException represent assistant server failed response.
    - AssistantSercerException 表示助理服务器响应失败

12、 `InvalidRequestArgumentError`

- 报错解释: 
    - InvalidRequestArgumentError invalid request param
    - InvalidRequestArgumentError 表示请求参数无效

13、 `RiskInputException`

- 报错解释: 
    - RiskInputException represent risk input error
    - RiskInputException 表示异常输入错误

14、 `AppbuilderBuildexException`

- 报错解释: 
    - Appbuilder buledex exception
    - AppbuilderBuildexException 表示AppBuilder-SDK构建异常，报错使用与Appbuilder-SDK的构造代码单元检测不符合规范

15、 `AppbuilderTraceException`

- 报错解释: 
    - Appbuilder trace exception
    - AppbuilderTraceException 表示AppBuilder-SDK追踪框架异常，使用`export APPBUILDER_TRACE_DEBUG=TRUE`来开启Appbuilder-SDK的追踪框架的DEBUG模式，展示报错的完整链路并调试