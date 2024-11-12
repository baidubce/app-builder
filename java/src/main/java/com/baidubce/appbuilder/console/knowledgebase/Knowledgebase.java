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
    public Knowledgebase() {
        super();
    }

    public Knowledgebase(String SecretKey) {
        super(SecretKey);
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

    public String uploadFile(String filePath, String clientToken) throws IOException, AppBuilderServerException {
        return innerUploadFile(filePath, clientToken);
    }

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

    public String[] addDocument(DocumentAddRequest req, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerAddDocument(req, clientToken);
    }

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

    public Document[] getDocumentList(DocumentListRequest request)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DOCUMENT_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentListResponse> response = httpClient.execute(getRequest, DocumentListResponse.class);
        DocumentListResponse respBody = response.getBody();
        return respBody.getData();
    }

    public void deleteDocument(DocumentDeleteRequest request)
            throws IOException, AppBuilderServerException {
        innerDeleteDocument(request, java.util.UUID.randomUUID().toString());
    }

    public void deleteDocument(DocumentDeleteRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        innerDeleteDocument(request, clientToken);
    }

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

    public KnowledgeBaseDetail createKnowledgeBase(KnowledgeBaseDetail request)
            throws IOException, AppBuilderServerException {
        return innerCreateKnowledgeBase(request, java.util.UUID.randomUUID().toString());
    }

    public KnowledgeBaseDetail createKnowledgeBase(KnowledgeBaseDetail request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateKnowledgeBase(request, clientToken);
    }

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

    public void deleteKnowledgeBase(String knowledgeBaseId)
            throws IOException, AppBuilderServerException {
        innerDeleteKnowledgeBase(knowledgeBaseId, java.util.UUID.randomUUID().toString());
    }

    public void deleteKnowledgeBase(String knowledgeBaseId, String clientToken)
            throws IOException, AppBuilderServerException {
        innerDeleteKnowledgeBase(knowledgeBaseId, clientToken);
    }

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

    public void modifyKnowledgeBase(KnowledgeBaseModifyRequest request)
            throws IOException, AppBuilderServerException {
        modifyKnowledgeBase(request, java.util.UUID.randomUUID().toString());
    }

    public void modifyKnowledgeBase(KnowledgeBaseModifyRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        innerModifyKnowledgeBase(request, clientToken);
    }

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

    public DocumentsCreateResponse createDocuments(DocumentsCreateRequest request)
            throws IOException, AppBuilderServerException {
        return innerCreateDocuments(request, java.util.UUID.randomUUID().toString());
    }

    public DocumentsCreateResponse createDocuments(DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateDocuments(request, clientToken);
    }

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

    public DocumentsUploadResponse uploadDocuments(String filePath, DocumentsCreateRequest request)
            throws IOException, AppBuilderServerException {
        return innerUploadDocuments(filePath, request, java.util.UUID.randomUUID().toString());
    }

    public DocumentsUploadResponse uploadDocuments(String filePath, DocumentsCreateRequest request, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerUploadDocuments(filePath, request, clientToken);
    }

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

    public String createChunk(String documentId, String content)
            throws IOException, AppBuilderServerException {
        return innerCreateChunk(documentId, content, java.util.UUID.randomUUID().toString());
    }

    public String createChunk(String documentId, String content, String clientToken)
            throws IOException, AppBuilderServerException {
        return innerCreateChunk(documentId, content, clientToken);
    }

    private String innerCreateChunk(String documentId, String content, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_CREATE_URL;

        ChunkCreateRequest request = new ChunkCreateRequest(documentId, content);
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunkCreateResponse> response = httpClient.execute(postRequest, ChunkCreateResponse.class);
        ChunkCreateResponse respBody = response.getBody();
        return respBody.getChunkId();
    }

    public void modifyChunk(String chunkId, String content, boolean enable)
            throws IOException, AppBuilderServerException {
        innerModifyChunk(chunkId, content, enable, java.util.UUID.randomUUID().toString());
    }

    public void modifyChunk(String chunkId, String content, boolean enable, String clientToken)
            throws IOException, AppBuilderServerException {
        innerModifyChunk(chunkId, content, enable, clientToken);
    }

    private void innerModifyChunk(String chunkId, String content, boolean enable, String clientToken)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_MODIFY_URL;

        ChunkModifyRequest request = new ChunkModifyRequest(chunkId, content, enable);
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, ChunkCreateResponse.class);
    }

    public void deleteChunk(String chunkId) throws IOException, AppBuilderServerException {
        innderDeleteChunk(chunkId, java.util.UUID.randomUUID().toString());
    }

    public void deleteChunk(String chunkId, String clientToken) throws IOException, AppBuilderServerException {
        innderDeleteChunk(chunkId, clientToken);
    }

    private void innderDeleteChunk(String chunkId, String clientToken) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_DELETE_URL;
        ChunkDeleteRequest request = new ChunkDeleteRequest();
        request.setChunkId(chunkId);
        String jsonBody = JsonUtils.serialize(request);
        url = url + "&clientToken=" + clientToken;
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        httpClient.execute(postRequest, ChunkCreateResponse.class);
    }

    public ChunkDescribeResponse describeChunk(String chunkId)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNK_DESCRIBE_URL;

        ChunkDescribeRequest request = new ChunkDescribeRequest();
        request.setChunkId(chunkId);
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunkDescribeResponse> response = httpClient.execute(postRequest, ChunkDescribeResponse.class);
        ChunkDescribeResponse respBody = response.getBody();
        return respBody;
    }

    public ChunksDescribeResponse describeChunks(String documentId, String marker, Integer maxKeys,
            String type) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CHUNKS_DESCRIBE_URL;

        ChunksDescribeRequest request = new ChunksDescribeRequest(documentId, marker, maxKeys, type);
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ChunksDescribeResponse> response = httpClient.execute(postRequest, ChunksDescribeResponse.class);
        ChunksDescribeResponse respBody = response.getBody();
        return respBody;
    }
}
