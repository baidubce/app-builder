package com.baidubce.appbuilder.console.appbuilderclient;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.appbuilderclient.*;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;

import org.apache.hc.client5.http.entity.mime.HttpMultipartMode;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class AppBuilderClient extends Component {
    public String appID;

    public AppBuilderClient(String appID) {
        super();
        this.appID = appID;
    }

    public AppBuilderClient(String appID, String secretKey) {
        super(secretKey);
        this.appID = appID;
    }

    public AppBuilderClient(String appID, String secretKey, String gateway) {
        super(secretKey, gateway);
        this.appID = appID;
    }

    /**
     * 创建会话
     *
     * @return 返回会话ID
     * @throws IOException 当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String createConversation() throws IOException, AppBuilderServerException {
        return innerCreateConversation();
    }

    /**
     * 创建对话
     *
     * @return 对话ID
     * @throws IOException 如果发生I/O错误
     * @throws AppBuilderServerException 如果发生AppBuilder服务器错误
     */
    private String innerCreateConversation() throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CREATE_CONVERSATION_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("app_id", this.appID);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ConversationResponse> response =
                httpClient.execute(postRequest, ConversationResponse.class);
        ConversationResponse respBody = response.getBody();

        return respBody.getConversationId();
    }

    /**
     * 上传本地文件
     *
     * @param conversationId 会话ID
     * @param filePath       文件路径
     * @return 上传结果
     * @throws IOException            文件上传过程中发生的I/O异常
     * @throws AppBuilderServerException 应用构建服务器异常
     */
    public String uploadLocalFile(String conversationId, String filePath)
            throws IOException, AppBuilderServerException {
        return innerUploadLocalFile(conversationId, filePath);
    }

    /**
     * 上传本地文件
     *
     * @param conversationId 会话ID
     * @param filePath       文件路径
     * @return 文件ID
     * @throws IOException              当发生输入输出异常时抛出
     * @throws AppBuilderServerException 当AppBuilder服务器异常时抛出
     */
    private String innerUploadLocalFile(String conversationId, String filePath)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.UPLOAD_FILE_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        MultipartEntityBuilder builder = MultipartEntityBuilder.create()
                .setMode(HttpMultipartMode.LEGACY).setCharset(StandardCharsets.UTF_8);
        builder.addBinaryBody("file", new File(filePath));
        builder.addTextBody("app_id", this.appID);
        builder.addTextBody("conversation_id", conversationId);
        builder.addTextBody("scenario", "assistant");

        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url, builder.build());
        HttpResponse<FileUploadResponse> response =
                httpClient.execute(postRequest, FileUploadResponse.class);

        FileUploadResponse respBody = response.getBody();
        return respBody.getFileId();
    }

    /**
     * 运行AppBuilderClient请求
     *
     * @param query 请求查询字符串
     * @param conversationId 会话ID
     * @param fileIds 文件ID数组
     * @param stream 是否以流的方式传输数据
     * @return AppBuilderClientIterator对象，用于迭代返回的结果
     * @throws IOException 如果发生I/O异常
     * @throws AppBuilderServerException 如果AppBuilder服务发生异常
     */
    public AppBuilderClientIterator run(String query, String conversationId, String[] fileIds,
            boolean stream) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AGENTBUILDER_RUN_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("app_id", this.appID);
        requestBody.put("query", query);
        requestBody.put("conversation_id", conversationId);
        requestBody.put("file_ids", fileIds);
        requestBody.put("stream", stream);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<Iterator<AppBuilderClientResponse>> response =
                httpClient.executeSSE(postRequest, AppBuilderClientResponse.class);
        return new AppBuilderClientIterator(response.getBody());
    }

    /**
     * 运行指定的AppBuilder客户端请求
     *
     * @param requestBody 包含AppBuilder客户端运行请求的请求体
     * @return 返回一个包含AppBuilder客户端响应的迭代器
     * @throws IOException 如果发生I/O错误
     * @throws AppBuilderServerException 如果发生AppBuilder服务器错误
     */
    public AppBuilderClientIterator run(AppBuilderClientRunRequest requestBody)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AGENTBUILDER_RUN_URL;
        if (this.appID == null || this.appID.isEmpty()) {
            throw new RuntimeException("Param 'appID' is required!");
        }

        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<Iterator<AppBuilderClientResponse>> response =
                httpClient.executeSSE(postRequest, AppBuilderClientResponse.class);
        return new AppBuilderClientIterator(response.getBody());
    }
}
