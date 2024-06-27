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

public class Knowledgebase extends Component{
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
        String url = AppBuilderConfig.KNOWLEDGEBASE_UPLOAD_FILE_URL;

        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY)
                .setCharset(StandardCharsets.UTF_8);
        builder.addBinaryBody("file", new File(filePath));

        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, builder.build());
        HttpResponse<FileUploadResponse> response = httpClient.execute(postRequest, FileUploadResponse.class);
        FileUploadResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.toString());
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
    public String[] addDocument(DocumentAddRequest req) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_ADD_DOCUMENT_URL;

        String jsonBody = JsonUtils.serialize(req);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentAddResponse> response = httpClient.execute(postRequest, DocumentAddResponse.class);
        DocumentAddResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.toString());
        }
        return respBody.getDocumentIds();
    }

    public  Document[] getDocumentList(DocumentListRequest request) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DOCUMENT_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentListResponse> response = httpClient.execute(getRequest, DocumentListResponse.class);
        DocumentListResponse respBody = response.getBody();
        return respBody.getData();
    }

    public void deleteDocument(DocumentDeleteRequest request) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.KNOWLEDGEBASE_DELETE_DOCUMENT_URL;
        ClassicHttpRequest getRequest = httpClient.createDeleteRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<DocumentDeleteResponse> response = httpClient.execute(getRequest, DocumentDeleteResponse.class);
        DocumentDeleteResponse respBody = response.getBody();
        if (!(respBody.getCode() == null)) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage(),
                    respBody.toString());
        }
    }
}
