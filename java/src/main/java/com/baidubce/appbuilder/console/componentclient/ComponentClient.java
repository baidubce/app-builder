package com.baidubce.appbuilder.console.componentclient;

import java.io.IOException;
import java.util.Iterator;
import java.nio.charset.StandardCharsets;

import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.componentclient.ComponentClientIterator;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunRequest;
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
     * 执行应用构建客户端运行请求
     *
     * @param requestBody 请求体，包含运行所需的所有信息
     * @return 返回包含构建客户端响应的迭代器
     * @throws IOException 如果在执行请求时发生I/O错误
     * @throws AppBuilderServerException 如果应用构建服务器返回错误响应
     */
    public ComponentClientIterator run(String component, String version, String action, ComponentClientRunRequest requestBody)
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.COMPONENT_RUN_URL;
        String urlSuffix = String.format("%s/%s", url, component);
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

        String jsonBody = JsonUtils.serialize(requestBody);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(urlSuffix,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<Iterator<ComponentClientRunResponse>> response =
                httpClient.executeSSE(postRequest, ComponentClientRunResponse.class);
        return new ComponentClientIterator(response.getBody());
    }
}
