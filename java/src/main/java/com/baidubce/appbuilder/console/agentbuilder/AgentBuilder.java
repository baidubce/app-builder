package com.baidubce.appbuilder.console.agentbuilder;


import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.agentbuilder.AgentBuilderResponse;
import com.baidubce.appbuilder.model.agentbuilder.ConversationResponse;
import com.baidubce.appbuilder.model.agentbuilder.FileUploadResponse;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;

import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class AgentBuilder extends Component {
    public String AppID;

    public AgentBuilder(String appID) {
        super();
        this.AppID = appID;
    }

    public AgentBuilder(String appID, String secretKey) {
        super(secretKey);
        this.AppID = appID;
    }

    public AgentBuilder(String appID, String secretKey, String gateway) {
        super(secretKey, gateway);
        this.AppID = appID;
    }

    /**
     * 创建会话
     *
     * @return 返回会话ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String createConversation() throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.CREATE_CONVERSATION_URL;

        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("app_id", this.AppID);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<ConversationResponse> response = httpClient.execute(postRequest, ConversationResponse.class);
        ConversationResponse convResponse = response.getBody();
        if (convResponse.getCode() != 0) {
            throw new AppBuilderServerException(response.getRequestId(), convResponse.getCode(), convResponse.getMessage());
        }
        return convResponse.getResult().getConversationId();
    }

    /**
     * 上传本地文件到指定会话中
     *
     * @param conversationId 会话ID
     * @param filePath       文件路径
     * @return 上传后的文件ID
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public String uploadLocalFile(String conversationId, String filePath) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.UPLOAD_FILE_URL;

        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addBinaryBody("file", new File(filePath));
        builder.addTextBody("app_id", this.AppID);
        builder.addTextBody("conversation_id", conversationId);
        builder.addTextBody("scenario", "assistant");

        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, builder.build());
        HttpResponse<FileUploadResponse> response = httpClient.execute(postRequest, FileUploadResponse.class);

        FileUploadResponse uploadResponse = response.getBody();
        if (uploadResponse.getCode() != 0) {
            throw new AppBuilderServerException(uploadResponse.getRequestId(), uploadResponse.getCode(), uploadResponse.getMessage());
        }
        return uploadResponse.getResult().getFileId();
    }

    /**
     * 运行AgentBuilder，根据输入的问题、会话ID、文件ID数组以及是否以流模式返回结果，返回AgentBuilderResponse的迭代器。
     *
     * @param query          问题
     * @param conversationId 会话ID
     * @param fileIds        文件ID数组
     * @param stream         是否以流模式返回结果
     * @return AgentBuilderResponse的迭代器
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public Iterator<AgentBuilderResponse> run(String query, String conversationId, String[] fileIds, boolean stream) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.AGENTBUILDER_RUN_URL;
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("app_id", this.AppID);
        requestBody.put("query", query);
        requestBody.put("conversation_id", conversationId);
        requestBody.put("file_ids", fileIds);
        requestBody.put("stream", stream);
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<Iterator<AgentBuilderResponse>> response = httpClient.executeSSE(postRequest, AgentBuilderResponse.class);
        if (response.getCode() != 200) {
            throw new AppBuilderServerException(response.getRequestId(), response.getCode(), response.getMessage());
        }
        return response.getBody();
    }
}
