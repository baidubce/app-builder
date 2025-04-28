package com.baidubce.appbuilder.console.componentclient;

import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.nio.charset.StandardCharsets;

import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.componentclient.ComponentClientIterator;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunResponse;

public class ComponentClient extends Component {
    public ComponentClient() {
        super();
    }

    public ComponentClient(String secretKey) {
        super(secretKey);
    }

    public ComponentClient(String secretKey, String gateway) {
        super(secretKey, gateway);
    }

    /**
     * 运行Component，根据输入的问题、会话ID、文件ID数组以及是否以流模式等信息返回结果，返回ComponentClientIterator迭代器。
     *
     * 
     * @param componentId 组件ID
     * @param version     组件版本
     * @param action      参数动作
     * @param stream      是否以流的形式返回结果
     * @param parameters  参数列表
     * @return ComponentCientIterator 迭代器，包含 ComponentCientIterator 的运行结果
     * @throws IOException               如果在 I/O 操作过程中发生错误
     * @throws AppBuilderServerException 如果 AppBuilder 服务器返回错误
     */
    public ComponentClientIterator run(String componentId, String version, String action, boolean stream,  Map<String, Object> parameters)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.COMPONENT_RUN_URL;
        String urlSuffix = String.format("%s/%s", url, componentId);
        if (!version.isEmpty()) {
            urlSuffix += String.format("/version/%s", version);
        }
        if (!action.isEmpty()) {
            if (urlSuffix.contains("?")) {
                urlSuffix += String.format("&action=%s", action);
            } else {
                urlSuffix += String.format("?action=%s", action);
            }
        }

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("parameters", parameters);
        requestBody.put("stream", stream);
        String jsonBody = JsonUtils.serialize(requestBody);

        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(urlSuffix,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<StreamIterator<ComponentClientRunResponse>> response =
                httpClient.executeSSE(postRequest, ComponentClientRunResponse.class);
        return new ComponentClientIterator(response.getBody());
    }
}
