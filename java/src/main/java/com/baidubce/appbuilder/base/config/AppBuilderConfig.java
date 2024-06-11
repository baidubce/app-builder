package com.baidubce.appbuilder.base.config;

public class AppBuilderConfig {
    public static final String APPBUILDER_TOKEN = "APPBUILDER_TOKEN";
    public static final String APPBUILDER_GATEWAY_URL = "GATEWAY_URL";
    public static final String APPBUILDER_GATEWAY_URL_V2 = "GATEWAY_URL_V2";
    public static final String APPBUILDER_REQUEST_ID = "X-Appbuilder-Request-Id";
    public static final String APPBUILDER_DEFAULT_GATEWAY = "https://appbuilder.baidu.com";
    public static final String APPBUILDER_DEFAULT_GATEWAY_V2 = "https://qianfan.baidubce.com";
    public static final String APPBUILDER_LOGLEVEL = "APPBUILDER_LOGLEVEL";
    public static final String APPBUILDER_LOGFILE = "APPBUILDER_LOGFILE";

    // http client请求超时时间，秒
    public static final int HTTP_CLIENT_CONNECTION_TIMEOUT = 300;
    
    // agentbuilder
    // 创建会话
    public static final String CREATE_CONVERSATION_URL = "/v2/app/conversation";
    // 上传文件
    public static final String UPLOAD_FILE_URL = "/v2/app/conversation/file/upload";
    // 运行appbuilder
    public static final String AGENTBUILDER_RUN_URL = "/v2/app/conversation/runs";

    // 运行rag
    public static final String RAG_RUN_URL = "/api/v1/ai_engine/agi_platform/v1/instance/integrated";

    // dataset
    // 创建数据集
    public static final String DATASET_CREATE_URL = "/api/v1/ai_engine/agi_platform/v1/datasets/create";
    // 新增文档
    public static final String DATASET_ADD_FILE_URL = "/api/v1/ai_engine/agi_platform/v1/datasets/documents";
    // 获取文档列表
    public static final String DATASET_GET_FILE_LIST_URL = "/api/v1/ai_engine/agi_platform/v1/datasets/documents/list_page";
    // 删除文档
    public static final String DATASET_DELETE_FILE_URL = "/api/v1/ai_engine/agi_platform/v1/datasets/document/delete";
    // 上传文件
    public static final String DATASET_UPLOAD_FILE_URL = "/api/v1/ai_engine/agi_platform/v1/datasets/files/upload";

    private AppBuilderConfig() {
    }
}
