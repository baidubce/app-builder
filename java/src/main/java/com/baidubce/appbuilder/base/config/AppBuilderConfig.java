package com.baidubce.appbuilder.base.config;

public class AppBuilderConfig {
    public static final String APPBUILDER_TOKEN = "APPBUILDER_TOKEN";
    public static final String APPBUILDER_GATEWAY_URL = "GATEWAY_URL";
    public static final String APPBUILDER_GATEWAY_URL_V2 = "GATEWAY_URL_V2";
    public static final String APPBUILDER_CONSOLE_OPENAPI_VERSION = "CONSOLE_OPENAPI_VERSION";
    public static final String APPBUILDER_CONSOLE_OPENAPI_PREFIX = "CONSOLE_OPENAPI_PREFIX";
    public static final String APPBUIDLER_SECRET_KEY_PREFIX = "SECRET_KEY_PREFIX";

    public static final String APPBUILDER_REQUEST_ID = "X-Appbuilder-Request-Id";
    public static final String APPBUILDER_DEFAULT_GATEWAY = "https://appbuilder.baidu.com";
    public static final String APPBUILDER_DEFAULT_GATEWAY_V2 = "https://qianfan.baidubce.com";
    public static final String APPBUILDER_DEFAULT_CONSOLE_OPENAPI_VERSION = "/v2";
    public static final String APPBUILDER_DEFAULT_CONSOLE_OPENAPI_PREFIX = "";
    public static final String APPBUILDER_DEFAULT_SECRET_KEY_PREFIX = "Bearer";

    public static final String APPBUILDER_LOGLEVEL = "APPBUILDER_LOGLEVEL";
    public static final String APPBUILDER_LOGFILE = "APPBUILDER_LOGFILE";

    // http client请求超时时间，秒
    public static final int HTTP_CLIENT_CONNECTION_TIMEOUT = 300;

    // appbuilderclient
    // 应用列表
    public static final String APP_LIST_URL = "/apps";
    public static final String APPS_DESCRIBE_URL = "/app?Action=DescribeApps";
    // 应用详情
    public static final String APP_DESCRIBE_URL = "/app?Action=DescribeApp";
    // 创建会话
    public static final String CREATE_CONVERSATION_URL = "/app/conversation";
    // 上传文件
    public static final String UPLOAD_FILE_URL = "/app/conversation/file/upload";
    // 运行appbuilder
    public static final String AGENTBUILDER_RUN_URL = "/app/conversation/runs";
    // 点踩点赞
    public static final String FEEDBACK_URL = "/app/conversation/feedback";

    // knowledgebase
    // 上传文件
    public static final String KNOWLEDGEBASE_UPLOAD_FILE_URL = "/file";
    // 新增知识库文档
    public static final String KNOWLEDGEBASE_ADD_DOCUMENT_URL = "/knowledge_base/document";
    // 获取知识库文档列表
    public static final String KNOWLEDGEBASE_DOCUMENT_LIST_URL = "/knowledge_base/documents";
    public static final String DESCRIBE_DOCUMENTS_URL = "/knowledgeBase?Action=DescribeDocuments";
    // 删除知识库文档
    public static final String KNOWLEDGEBASE_DELETE_DOCUMENT_URL = "/knowledge_base/document";
    // 创建知识库
    public static final String KNOWLEDGEBASE_CREATE_URL =
            "/knowledgeBase?Action=CreateKnowledgeBase";
    // 获取知识库详情
    public static final String KNOWLEDGEBASE_DETAIL_URL =
            "/knowledgeBase?Action=DescribeKnowledgeBase";
    // 删除知识库
    public static final String KNOWLEDGEBASE_DELETE_URL =
            "/knowledgeBase?Action=DeleteKnowledgeBase";
    // 获取知识库列表
    public static final String KNOWLEDGEBASE_LIST_URL =
            "/knowledgeBase?Action=DescribeKnowledgeBases";
    // 更新知识库
    public static final String KNOWLEDGEBASE_MODIFY_URL =
            "/knowledgeBase?Action=ModifyKnowledgeBase";
    // 导入知识库
    public static final String KNOWLEDGEBASE_CREATE_DOCUMENTS_URL =
            "/knowledgeBase?Action=CreateDocuments";
    // 上传文件到知识库
    public static final String KNOWLEDGEBASE_UPLOAD_DOCUMENTS_URL =
            "/knowledgeBase?Action=UploadDocuments";
    // 创建切片
    public static final String CHUNK_CREATE_URL = "/knowledgeBase?Action=CreateChunk";
    // 修改切片
    public static final String CHUNK_MODIFY_URL = "/knowledgeBase?Action=ModifyChunk";
    // 获取切片详情
    public static final String CHUNK_DESCRIBE_URL = "/knowledgeBase?Action=DescribeChunk";
    // 获取切片列表
    public static final String CHUNKS_DESCRIBE_URL = "/knowledgeBase?Action=DescribeChunks";
    // 删除切片
    public static final String CHUNK_DELETE_URL = "/knowledgeBase?Action=DeleteChunk";
    // 知识库检索
    public static final String QUERY_KNOWLEDGEBASE_URL = "/knowledgebases/query";

    // 组件调用
    public static final String COMPONENT_RUN_URL = "/components";

    // AI搜索、基础搜索
    public static final String AI_SEARCH_URL = "/ai_search/chat/completions";

    // 运行rag
    public static final String RAG_RUN_URL =
            "/api/v1/ai_engine/agi_platform/v1/instance/integrated";

    // dataset
    // 创建数据集
    public static final String DATASET_CREATE_URL =
            "/api/v1/ai_engine/agi_platform/v1/datasets/create";
    // 新增文档
    public static final String DATASET_ADD_FILE_URL =
            "/api/v1/ai_engine/agi_platform/v1/datasets/documents";
    // 获取文档列表
    public static final String DATASET_GET_FILE_LIST_URL =
            "/api/v1/ai_engine/agi_platform/v1/datasets/documents/list_page";
    // 删除文档
    public static final String DATASET_DELETE_FILE_URL =
            "/api/v1/ai_engine/agi_platform/v1/datasets/document/delete";
    // 上传文件
    public static final String DATASET_UPLOAD_FILE_URL =
            "/api/v1/ai_engine/agi_platform/v1/datasets/files/upload";

    private AppBuilderConfig() {}
}
