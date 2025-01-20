package com.baidubce.appbuilder.console.knowledgebase;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.apache.hc.client5.http.entity.mime.HttpMultipartMode;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.knowledgebase.*;

public class Knowledgebase extends Component {
    private String knowledgeBaseId;

    public Knowledgebase() {
        super();
    }

    public Knowledgebase(String SecretKey) {
        super(SecretKey);
    }

    public Knowledgebase(String knowledgeBaseId, String SecretKey) {
        super(SecretKey);
        this.knowledgeBaseId = knowledgeBaseId;
    }

    /**
     * 上传文档
     *
     * @param filePath 文件路径
     * @return 上传成功后的文档ID
     * @throws IOException               当文件上传失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String uploadFile(String filePath) throws IOException, AppBuilderServerException {
        return innerUploadFile(filePath, java.util.UUID.randomUUID().toString());
    }

    /**
     * 上传文件
     *
     * @param filePath 文件路径
     * @param clientToken 客户端令牌
     * @return 上传文件的结果
     * @throws IOException 如果发生I/O错误
     * @throws AppBuilderServerException 如果应用构建服务器发生错误
     */
    public String uploadFile(String filePath, String clientToken) throws IOException, AppBuilderServerException {
        return innerUploadFile(filePath, clientToken);
    }

    /**
     * 上传文件到指定服务器。
     *
     * @param filePath 文件路径
     * @param clientToken 客户端令牌
     * @return 文件ID
     * @throws IOException 当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当发生应用构建服务器异常时抛出
     */
    private String innerUploadFile(String filePath, String clientToken) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_UPLOAD_FILE_URL;

        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY).setCharset(StandardCharsets.UTF_8);
        builder.addBinaryBody("file", new File(filePath));

        url = url + "?clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, builder.build());
        HttpResponse<FileUploadResponse> response = httpClient.execute(postRequest, FileUploadResponse.class);
        FileUploadResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(),
                    response.getMessage(), respBody.toString());
        }
        return respBody.getId();
    }

    /**
     * 新增知识库文档
     *
     * @param req 请求参数
     * @return documentIds 文档ID
     * 
     * @throws IOException               当文件上传失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String[] addDocument(DocumentAddRequest req)
            throws IOException, AppBuilderServerException {
        return innerAddDocument(req, java.util.UUID.randomUUID().toString());
    }

    /**
     * 向应用程序中添加文档
     *
     * @param req 文档添加请求对象，包含需要添加的文档信息
     * @param clientToken 客户端令牌，用于验证请求来源
     * @return 返回一个字符串数组，包含操作结果
     * @throws IOException 如果发生输入/输出异常，抛出此异常
     * @throws AppBuilderServerException 如果应用程序构建服务器发生异常，抛出此异常
     */
    public String[] addDocument(DocumentAddRequest req, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerAddDocument(req, clientToken);
    }

    /**
     * 向知识库中添加文档
     *
     * @param req 文档添加请求对象
     * @param clientToken 客户端令牌
     * @return 文档ID数组
     * @throws IOException 如果发生I/O异常
     * @throws AppBuilderServerException 如果应用构建服务器异常
     */
    private String[] innerAddDocument(DocumentAddRequest req, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_ADD_DOCUMENT_URL;

        String jsonBody = JsonUtils.serialize(req);
        url = url + "?clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentAddResponse> response = httpClient.execute(postRequest, DocumentAddResponse.class);
        DocumentAddResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(),
                    response.getMessage(), respBody.toString());
        }
        return respBody.getDocumentIds();
    }

    /**
     * 获取文档列表
     *
     * @param request 文档列表请求对象，包含请求参数
     * @return 文档数组
     * @throws IOException 当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当应用构建服务器发生异常时抛出
     */
    public Document[] getDocumentList(DocumentListRequest request)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DOCUMENT_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentListResponse> response = httpClient.execute(getRequest, DocumentListResponse.class);
        DocumentListResponse respBody = response.getBody();
        return respBody.getData();
    }

    /**
     * 删除文档
     *
     * @param request 文档删除请求对象
     * @throws IOException                 如果在删除文档过程中发生I/O异常
     * @throws AppBuilderServerException 如果在删除文档过程中发生AppBuilder服务器异常
     */
    public void deleteDocument(DocumentDeleteRequest request)
            throws IOException, AppBuilderServerException {
        innerDeleteDocument(request, java.util.UUID.randomUUID().toString());
    }

    /**
     * 删除文档
     *
     * @param request       删除文档的请求对象，包含要删除的文档ID等信息
     * @param clientToken   客户端令牌，用于验证请求合法性
     * @throws IOException   如果发生输入输出异常
     * @throws AppBuilderServerException 如果发生应用构建服务器异常
     */
    public void deleteDocument(DocumentDeleteRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        innerDeleteDocument(request, clientToken);
    }

    /**
     * 删除文档
     *
     * @param request 删除文档请求
     * @param clientToken 客户端令牌
     * @throws IOException IO异常
     * @throws AppBuilderServerException 应用构建服务器异常
     */
    private void innerDeleteDocument(DocumentDeleteRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DELETE_DOCUMENT_URL;
        url = url + "?clientToken=" + clientToken;
        ClassicHttpRequest getRequest = httpClient.createDeleteRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentDeleteResponse> response = httpClient.execute(getRequest, DocumentDeleteResponse.class);
        DocumentDeleteResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(),
                    response.getMessage(), respBody.toString());
        }
    }

    /**
     * 创建知识库详情
     *
     * @param request 请求体，包含创建知识库所需的信息
     * @return 创建成功后的知识库详情
     * @throws IOException 当输入输出操作发生错误时抛出
     * @throws AppBuilderServerException 当应用构建服务器发生错误时抛出
     */
    public KnowledgeBaseDetail createKnowledgeBase(KnowledgeBaseDetail request)
            throws IOException, AppBuilderServerException {
        return innerCreateKnowledgeBase(request, java.util.UUID.randomUUID().toString());
    }

    /**
     * 创建知识库详情
     *
     * @param request        包含创建知识库详情所需的参数
     * @param clientToken    客户端令牌，用于身份验证
     * @return 创建成功后的知识库详情对象
     * @throws IOException                 如果发生I/O错误
     * @throws AppBuilderServerException   如果发生应用程序构建服务器异常
     */
    public KnowledgeBaseDetail createKnowledgeBase(KnowledgeBaseDetail request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateKnowledgeBase(request, clientToken);
    }

    /**
     * 创建一个知识库详情
     *
     * @param request 知识库详情请求对象
     * @param clientToken 客户端令牌
     * @return 创建成功后的知识库详情对象
     * @throws IOException IO异常
     * @throws AppBuilderServerException AppBuilder服务器异常
     */
    private KnowledgeBaseDetail innerCreateKnowledgeBase(KnowledgeBaseDetail request, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_CREATE_URL;
        url = url + "&clientToken=" + clientToken;
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<KnowledgeBaseDetail> response = httpClient.execute(postRequest, KnowledgeBaseDetail.class);
        KnowledgeBaseDetail respBody = response.getBody();
        return respBody;
    }

    /**
     * 根据知识库ID获取知识库详情
     *
     * @param knowledgeBaseId 知识库ID
     * @return KnowledgeBaseDetail 知识库详情对象
     * @throws IOException 如果在发送HTTP请求或解析响应时发生IO异常
     * @throws AppBuilderServerException 如果发生AppBuilder服务器异常
     */
    public KnowledgeBaseDetail getKnowledgeBaseDetail(String knowledgeBaseId)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DETAIL_URL;

        KnowledgeBaseDetailRequest request = new KnowledgeBaseDetailRequest();
        request.setKnowledgeBaseId(knowledgeBaseId);
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<KnowledgeBaseDetail> response = httpClient.execute(postRequest, KnowledgeBaseDetail.class);
        KnowledgeBaseDetail respBody = response.getBody();
        return respBody;
    }

    /**
     * 删除知识库
     *
     * @param knowledgeBaseId 知识库ID
     * @throws IOException      当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当应用构建服务器异常时抛出
     */
    public void deleteKnowledgeBase(String knowledgeBaseId)
            throws IOException, AppBuilderServerException {
        innerDeleteKnowledgeBase(knowledgeBaseId, java.util.UUID.randomUUID().toString());
    }

    /**
     * 删除知识库
     *
     * @param knowledgeBaseId 知识库ID
     * @param clientToken     客户端令牌
     * @throws IOException              如果发生输入输出异常
     * @throws AppBuilderServerException 如果发生应用构建服务器异常
     */
    public void deleteKnowledgeBase(String knowledgeBaseId, String clientToken)
            throws IOException, AppBuilderServerException {
        innerDeleteKnowledgeBase(knowledgeBaseId, clientToken);
    }

    /**
     * 删除知识库
     *
     * @param knowledgeBaseId 知识库ID
     * @param clientToken     客户端令牌
     * @throws IOException                 IO异常
     * @throws AppBuilderServerException   AppBuilder服务器异常
     */
    private void innerDeleteKnowledgeBase(String knowledgeBaseId, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DELETE_URL;

        KnowledgeBaseDetailRequest request = new KnowledgeBaseDetailRequest();
        request.setKnowledgeBaseId(knowledgeBaseId);
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, null);
    }

    /**
     * 修改知识库。
     *
     * @param request 知识库修改请求对象
     * @throws IOException 如果在I/O操作过程中发生错误，则抛出此异常
     * @throws AppBuilderServerException 如果应用构建服务器发生错误，则抛出此异常
     */
    public void modifyKnowledgeBase(KnowledgeBaseModifyRequest request)
            throws IOException, AppBuilderServerException {
        modifyKnowledgeBase(request, java.util.UUID.randomUUID().toString());
    }

    /**
     * 修改知识库
     *
     * @param request 修改请求对象，包含需要修改的内容
     * @param clientToken 客户端令牌，用于验证请求来源的合法性
     * @throws IOException 如果发生输入输出异常
     * @throws AppBuilderServerException 如果应用构建服务器发生异常
     */
    public void modifyKnowledgeBase(KnowledgeBaseModifyRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        innerModifyKnowledgeBase(request, clientToken);
    }

    /**
     * 修改知识库
     *
     * @param request  修改知识库的请求对象
     * @param clientToken 客户端令牌
     * @throws IOException                  当请求过程中发生I/O异常时抛出
     * @throws AppBuilderServerException    当请求过程中发生服务器异常时抛出
     */
    private void innerModifyKnowledgeBase(KnowledgeBaseModifyRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_MODIFY_URL;

        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, null);
    }

    /**
     * 获取知识库列表
     *
     * @param request 包含请求参数的知识库列表请求对象
     * @return 知识库列表响应对象
     * @throws IOException 如果发生I/O异常，抛出此异常
     * @throws AppBuilderServerException 如果应用构建服务器发生异常，抛出此异常
     */
    public KnowledgeBaseListResponse getKnowledgeBaseList(KnowledgeBaseListRequest request)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_LIST_URL;

        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<KnowledgeBaseListResponse> response = httpClient.execute(postRequest,
                KnowledgeBaseListResponse.class);
        KnowledgeBaseListResponse respBody = response.getBody();
        return respBody;
    }

    /**
     * 创建文档
     *
     * @param request 文档创建请求
     * @return 创建文档的响应结果
     * @throws IOException          当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当应用构建服务器发生异常时抛出
     */
    public DocumentsCreateResponse createDocuments(DocumentsCreateRequest request)
            throws IOException, AppBuilderServerException {
        return innerCreateDocuments(request, java.util.UUID.randomUUID().toString());
    }

    /**
     * 创建文档
     *
     * @param request 包含创建文档所需信息的请求对象
     * @param clientToken 客户端令牌，用于身份验证
     * @return 包含创建文档结果的响应对象
     * @throws IOException 如果发生输入/输出错误
     * @throws AppBuilderServerException 如果应用程序构建服务器发生错误
     */
    public DocumentsCreateResponse createDocuments(DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateDocuments(request, clientToken);
    }

    /**
     * 创建文档的内部方法
     *
     * @param request    创建文档的请求参数
     * @param clientToken 客户端令牌
     * @return 创建文档的响应结果
     * @throws IOException              如果发生输入输出异常
     * @throws AppBuilderServerException 如果应用构建服务器发生异常
     */
    private DocumentsCreateResponse innerCreateDocuments(DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_CREATE_DOCUMENTS_URL;

        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, null);

        HttpResponse<DocumentsCreateResponse> response = httpClient.execute(postRequest,
                DocumentsCreateResponse.class);
        DocumentsCreateResponse respBody = response.getBody();
        return respBody;
    }

    /**
     * 上传文档
     *
     * @param filePath 文件路径
     * @param request 文档创建请求
     * @return 文档上传响应
     * @throws IOException            如果发生I/O错误，则抛出此异常
     * @throws AppBuilderServerException 如果发生应用程序构建服务器错误，则抛出此异常
     */
    public DocumentsUploadResponse uploadDocuments(String filePath, DocumentsCreateRequest request)
            throws IOException, AppBuilderServerException {
        return innerUploadDocuments(filePath, request, java.util.UUID.randomUUID().toString());
    }

    /**
     * 上传文档
     *
     * @param filePath 文件路径
     * @param request  文档上传请求对象
     * @param clientToken 客户端Token
     * @return 文档上传响应对象
     * @throws IOException 抛出IO异常
     * @throws AppBuilderServerException 抛出应用构建服务器异常
     */
    public DocumentsUploadResponse uploadDocuments(String filePath, DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerUploadDocuments(filePath, request, clientToken);
    }

    /**
     * 上传文档到知识库
     *
     * @param filePath 要上传的文件的路径
     * @param request 文档上传请求对象
     * @param clientToken 客户端令牌
     * @return 上传文档响应对象
     * @throws IOException 如果在IO操作过程中发生错误
     * @throws AppBuilderServerException 如果在应用构建服务器操作过程中发生错误
     */
    private DocumentsUploadResponse innerUploadDocuments(String filePath, DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_UPLOAD_DOCUMENTS_URL;

        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY).setCharset(StandardCharsets.UTF_8);
        builder.addBinaryBody("file", new File(filePath));

        String jsonBody = JsonUtils.serialize(request);
        builder.addTextBody("payload", jsonBody);

        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, builder.build());
        HttpResponse<DocumentsUploadResponse> response = httpClient.execute(postRequest,
                DocumentsUploadResponse.class);
        DocumentsUploadResponse respBody = response.getBody();
        return respBody;
    }

    /**
     * 根据给定的文档ID和内容创建一个块
     *
     * @param documentId 文档ID
     * @param content    块的内容
     * @return 创建的块的字符串表示
     * @throws IOException 如果在文件操作中发生错误
     * @throws AppBuilderServerException 如果在应用程序构建服务器操作中发生错误
     */
    public String createChunk(String documentId, String content)
            throws IOException, AppBuilderServerException {
        return innerCreateChunk(documentId, content, java.util.UUID.randomUUID().toString());
    }

    /**
     * 创建文档块
     *
     * @param documentId 文档ID
     * @param content    文档内容
     * @param clientToken 客户端令牌
     * @return 创建的文档块字符串
     * @throws IOException          如果发生I/O错误
     * @throws AppBuilderServerException 如果应用程序构建服务器异常
     */
    public String createChunk(String documentId, String content, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateChunk(documentId, content, clientToken);
    }

    /**
     * 内部创建文档片段的方法
     *
     * @param documentId 文档ID
     * @param content 文档内容
     * @param clientToken 客户端令牌
     * @return 创建的文档片段ID
     * @throws IOException IO异常
     * @throws AppBuilderServerException 应用构建服务器异常
     */
    private String innerCreateChunk(String documentId, String content, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_CREATE_URL;
        
        ChunkCreateRequest request;
        if(this.knowledgeBaseId.isEmpty()) {
            request = new ChunkCreateRequest(documentId, content);
        } else {
            request = new ChunkCreateRequest(this.knowledgeBaseId, documentId, content);
        }
        
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunkCreateResponse> response = httpClient.execute(postRequest, ChunkCreateResponse.class);
        ChunkCreateResponse respBody = response.getBody();
        return respBody.getChunkId();
    }

    /**
     * 修改指定块的内容
     *
     * @param chunkId 块标识符
     * @param content 要设置的内容
     * @param enable 是否启用块
     * @throws IOException 当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当发生应用构建服务器异常时抛出
     */
    public void modifyChunk(String chunkId, String content, boolean enable)
            throws IOException, AppBuilderServerException {
        innerModifyChunk(chunkId, content, enable, java.util.UUID.randomUUID().toString());
    }

    /**
     * 修改指定区块的内容及其启用状态
     *
     * @param chunkId      区块的ID
     * @param content      需要设置的新内容
     * @param enable       是否启用该区块，true表示启用，false表示禁用
     * @param clientToken  客户端令牌，用于验证客户端身份
     * @throws IOException           如果发生I/O错误
     * @throws AppBuilderServerException 如果发生应用构建服务器错误
     */
    public void modifyChunk(String chunkId, String content, boolean enable, String clientToken)
            throws IOException, AppBuilderServerException {
        innerModifyChunk(chunkId, content, enable, clientToken);
    }

    /**
     * 修改指定的块内容
     *
     * @param chunkId    块的ID
     * @param content    块的新内容
     * @param enable     是否启用块，true 表示启用，false 表示禁用
     * @param clientToken 客户端令牌
     * @throws IOException              如果发生I/O错误
     * @throws AppBuilderServerException 如果应用构建服务器发生错误
     */
    private void innerModifyChunk(String chunkId, String content, boolean enable, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_MODIFY_URL;

        ChunkModifyRequest request;
        if (this.knowledgeBaseId.isEmpty()) {
            request = new ChunkModifyRequest(chunkId, content, enable);
        } else {
            request = new ChunkModifyRequest(this.knowledgeBaseId, chunkId, content, enable);
        }
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, ChunkCreateResponse.class);
    }

    /**
     * 删除指定的文件块。
     *
     * @param chunkId 要删除的文件块的ID
     * @throws IOException 如果发生I/O错误
     * @throws AppBuilderServerException 如果发生应用构建服务器异常
     */
    public void deleteChunk(String chunkId) throws IOException, AppBuilderServerException {
        innderDeleteChunk(chunkId, java.util.UUID.randomUUID().toString());
    }

    /**
     * 删除指定的块。
     *
     * @param chunkId 块标识
     * @param clientToken 客户端令牌
     * @throws IOException 如果发生输入输出异常
     * @throws AppBuilderServerException 如果发生应用程序构建服务器异常
     */
    public void deleteChunk(String chunkId, String clientToken) throws IOException, AppBuilderServerException {
        innderDeleteChunk(chunkId, clientToken);
    }

    /**
     * 删除指定块
     *
     * @param chunkId 块ID
     * @param clientToken 客户端令牌
     * @throws IOException 当I/O操作失败时抛出
     * @throws AppBuilderServerException 当应用构建服务器异常时抛出
     */
    private void innderDeleteChunk(String chunkId, String clientToken) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_DELETE_URL;
        
        ChunkDeleteRequest request = new ChunkDeleteRequest();
        request.setChunkId(chunkId);
        if (!this.knowledgeBaseId.isEmpty()) {
            request.setKnowledgeBaseId(this.knowledgeBaseId);
        }
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, ChunkCreateResponse.class);
    }

    /**
     * 根据块ID描述块
     *
     * @param chunkId 块ID
     * @return 描述块的响应对象
     * @throws IOException 如果发生输入输出异常
     * @throws AppBuilderServerException 如果发生应用构建服务器异常
     */
    public ChunkDescribeResponse describeChunk(String chunkId)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_DESCRIBE_URL;

        ChunkDescribeRequest request = new ChunkDescribeRequest();
        request.setChunkId(chunkId);
        if (!this.knowledgeBaseId.isEmpty()) {
            request.setKnowledgeBaseId(this.knowledgeBaseId);
        }
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunkDescribeResponse> response = httpClient.execute(postRequest, ChunkDescribeResponse.class);
        ChunkDescribeResponse respBody = response.getBody();
        return respBody;
    }

    /**
     * 描述文档的分块信息
     *
     * @param documentId 文档ID
     * @param marker     分页标记
     * @param maxKeys    返回的最大分块数量
     * @param type       分块类型
     * @return 返回包含文档分块信息的ChunksDescribeResponse对象
     * @throws IOException             如果发生I/O异常
     * @throws AppBuilderServerException 如果发生AppBuilder服务器异常
     */
    public ChunksDescribeResponse describeChunks(String documentId, String marker, Integer maxKeys,
            String type) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNKS_DESCRIBE_URL;

        ChunksDescribeRequest request = new ChunksDescribeRequest(documentId, marker, maxKeys, type);
        if (!this.knowledgeBaseId.isEmpty()) {
            request.setKnowledgeBaseId(this.knowledgeBaseId);
        }
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunksDescribeResponse> response = httpClient.execute(postRequest, ChunksDescribeResponse.class);
        ChunksDescribeResponse respBody = response.getBody();
        return respBody;
    }

    public QueryKnowledgeBaseResponse queryKnowledgeBase(QueryKnowledgeBaseRequest request)
            throws IOException, AppBuilderServerException {
        if (request.rank_score_threshold == null) {
            request.rank_score_threshold = 0.4f;
        }
        String url = AppBuilderConfig.QUERY_KNOWLEDGEBASE_URL;

        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<QueryKnowledgeBaseResponse> response = httpClient.execute(postRequest,
                QueryKnowledgeBaseResponse.class);
        QueryKnowledgeBaseResponse respBody = response.getBody();
        return respBody;
    }
    
    public QueryKnowledgeBaseResponse queryKnowledgeBase(String query, String type, Float rank_score_threshold, Integer top, Integer skip,
            String[] knowledgebaseIDs, QueryKnowledgeBaseRequest.MetadataFilters filters,
            QueryKnowledgeBaseRequest.QueryPipelineConfig pipelineConfig) 
            throws IOException, AppBuilderServerException {
        if (rank_score_threshold == null) {
            rank_score_threshold = 0.4f;
        }

        String url = AppBuilderConfig.QUERY_KNOWLEDGEBASE_URL;
        QueryKnowledgeBaseRequest request = new QueryKnowledgeBaseRequest(query, type, rank_score_threshold,top, skip, knowledgebaseIDs, filters, pipelineConfig);
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<QueryKnowledgeBaseResponse> response = httpClient.execute(postRequest,
                QueryKnowledgeBaseResponse.class);
        QueryKnowledgeBaseResponse respBody = response.getBody();
        return respBody;
    }
}
