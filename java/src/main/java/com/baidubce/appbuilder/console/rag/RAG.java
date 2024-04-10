package com.baidubce.appbuilder.console.rag;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.model.rag.RAGResponse;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

public class RAG extends Component {
    public String AppID;

    public RAG(String appID) {
        super();
        this.AppID = appID;
    }

    public RAG(String appID, String secretKey) {
        super(secretKey);
        this.AppID = appID;
    }

    public RAG(String appID, String secretKey, String gateway) {
        super(secretKey, gateway);
        this.AppID = appID;
    }

    /**
     * 运行RAG模型，根据输入的问题、会话ID以及是否以流模式返回结果，返回RAGResponse的迭代器。
     *
     * @param query          问题
     * @param conversationId 会话ID
     * @param stream         是否以流模式返回结果
     * @return RAGResponse的迭代器
     * @throws IOException               当请求失败时抛出IOException
     * @throws AppBuilderServerException 当服务器返回错误码时抛出AppBuilderServerException
     */
    public Iterator<RAGResponse> run(String query, String conversationId, boolean stream) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.RAG_RUN_URL;
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("app_id", this.AppID);
        requestBody.put("query", query);
        requestBody.put("conversation_id", conversationId);
        requestBody.put("response_mode", stream ? "streaming" : "blocking");
        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequest(url, new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<Iterator<RAGResponse>> response = httpClient.executeSSE(postRequest, RAGResponse.class);
        return response.getBody();
    }
}
