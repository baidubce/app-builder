package com.baidubce.appbuilder.console.dataset;


import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;

import com.baidubce.appbuilder.model.dataset.*;
import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import org.apache.hc.client5.http.entity.mime.HttpMultipartMode;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class Dataset extends Component {
    String datasetId;

    @Deprecated
    public Dataset() {
        super();
    }

    @Deprecated
    public Dataset(String secretKey) {
        super(secretKey);
    }

    @Deprecated
    public Dataset(String secretKey, String datasetId) {
        super(secretKey);
        this.datasetId = datasetId;
    }

    /**
     * 创建数据集
     *
     * @param datasetName 数据集名称
     * @return 返回创建成功后的数据集ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String createDataset(String datasetName) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.DATASET_CREATE_URL;

        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("name", datasetName);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DatasetCreateResponse> response = httpClient.execute(postRequest, DatasetCreateResponse.class);
        DatasetCreateResponse respBody = response.getBody();
        if (respBody.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.getCode(), respBody.getMessage());
        }
        this.datasetId = respBody.getResult().getId();
        return this.datasetId;
    }

    /**
     * 上传文档
     *
     * @param filePath 文件路径
     * @return 上传成功后的文档ID
     * @throws IOException               当文件上传失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    private String uploadDocument(String filePath) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.DATASET_UPLOAD_FILE_URL;

        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY)
                .setCharset(StandardCharsets.UTF_8);
        builder.addBinaryBody("file", new File(filePath));

        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, builder.build());
        HttpResponse<FileUploadResponse> response = httpClient.execute(postRequest, FileUploadResponse.class);
        FileUploadResponse respBody = response.getBody();
        if (respBody.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.getCode(), respBody.getMessage());
        }
        return respBody.getResult().getId();
    }

    /**
     * 向数据集中添加文档
     *
     * @param filePaths           要添加的文档文件路径列表
     * @param isCustomProcessRule 是否使用自定义处理规则
     * @param customProcessRule   自定义处理规则，当isCustomProcessRule为true时，该参数不为空
     * @param isEnhanced          是否开启增强模式
     * @throws IOException               当文件上传失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String[] addDocuments(List<String> filePaths, boolean isCustomProcessRule, Map<String,
            Object> customProcessRule, boolean isEnhanced) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.DATASET_ADD_FILE_URL;
        if (this.datasetId == null || this.datasetId.isEmpty()) {
            throw new RuntimeException("Param 'datasetId' is required! Please set param or call createDataset() first");
        }
        ArrayList<String> fileIds = new ArrayList<>(filePaths.size());
        for (String filePath : filePaths) {
            String fileId = uploadDocument(filePath);
            fileIds.add(fileId);
        }
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("dataset_id", this.datasetId);
        requestBody.put("file_ids", fileIds);
        requestBody.put("is_custom_process_rule", isCustomProcessRule);
        requestBody.put("is_enhanced", isEnhanced);
        if (isCustomProcessRule && customProcessRule != null) {
            requestBody.put("custom_process_rule", customProcessRule);
        }
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentAddResponse> response = httpClient.execute(postRequest, DocumentAddResponse.class);
        DocumentAddResponse respBody = response.getBody();
        if (respBody.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.getCode(), respBody.getMessage());
        }
        return respBody.getResult().getDocumentIds();
    }

    /**
     * 获取文档列表
     *
     * @param page    页码
     * @param limit   每页文档数量
     * @param keywork 搜索关键字
     * @return 文档列表
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public DocumentListResponse getDocumentList(int page, int limit, String keywork) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.DATASET_GET_FILE_LIST_URL;
        if (this.datasetId == null || this.datasetId.isEmpty()) {
            throw new RuntimeException("Param 'datasetId' is required! Please set param or call createDataset() first");
        }
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("dataset_id", this.datasetId);
        requestBody.put("page", page);
        requestBody.put("limit", limit);
        requestBody.put("keyword", keywork);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentListResponse> response = httpClient.execute(postRequest, DocumentListResponse.class);
        DocumentListResponse respBody = response.getBody();
        if (respBody.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.getCode(), respBody.getMessage());
        }
        return respBody;
    }

    /**
     * 从数据集中删除文档
     *
     * @param documentId 要删除的文档ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public void deleteDocument(String documentId) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.DATASET_DELETE_FILE_URL;
        if (this.datasetId == null || this.datasetId.isEmpty()) {
            throw new RuntimeException("Param 'datasetId' is required! Please set param or call createDataset() first");
        }
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("dataset_id", this.datasetId);
        requestBody.put("document_id", documentId);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentDeleteResponse> response = httpClient.execute(postRequest, DocumentDeleteResponse.class);
        DocumentDeleteResponse respBody = response.getBody();
        if (respBody.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.getCode(), respBody.getMessage());
        }
    }

    /**
     * 从数据集中批量删除多个文档
     *
     * @param documentIds 要删除的文档ID数组
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public void deleteDocuments(String[] documentIds) throws IOException, AppBuilderServerException {
        for (String documentId : documentIds) {
            deleteDocument(documentId);
        }
    }
}