package com.baidubce.appbuilder.base.utils.http;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.ConsoleHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.UUID;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.Header;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.ParseException;
import org.apache.hc.core5.http.io.entity.EntityUtils;

public class HttpClient {
    public String SecretKey;
    public String Gateway;
    public String GatewayV2;
    private final CloseableHttpClient client;
    private static final Logger LOGGER = Logger.getLogger(Component.class.getName());

    public HttpClient(String secretKey, String gateway, String gatewayV2) {
        RequestConfig requestConfig = RequestConfig.custom()
                .setResponseTimeout(AppBuilderConfig.HTTP_CLIENT_CONNECTION_TIMEOUT, TimeUnit.SECONDS)
                .build();
        this.client = HttpClients.custom().setDefaultRequestConfig(requestConfig).build();
        this.SecretKey = secretKey;
        this.Gateway = gateway;
        this.GatewayV2 = gatewayV2;

        ConsoleHandler handler = new ConsoleHandler();
        String systemLogLevel = System.getProperty(AppBuilderConfig.APPBUILDER_LOGLEVEL);
        if (systemLogLevel == null || systemLogLevel.isEmpty()){
            systemLogLevel = System.getenv(AppBuilderConfig.APPBUILDER_LOGLEVEL);
        }
        if (systemLogLevel == null || systemLogLevel.isEmpty()) {
            LOGGER.setLevel(Level.INFO);
            handler.setLevel(Level.INFO);
        } else if (systemLogLevel.toLowerCase().equals("debug")) {
            LOGGER.setLevel(Level.FINE);
            handler.setLevel(Level.FINE);
        } else {
            LOGGER.setLevel(Level.INFO);
            handler.setLevel(Level.INFO);
        }
        LOGGER.addHandler(handler);
    }

    public ClassicHttpRequest createPostRequest(String url, HttpEntity entity) {
        String requestURL = Gateway + url;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("X-Appbuilder-Authorization", this.SecretKey);
        httpPost.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        httpPost.setHeader("X-Appbuilder-Sdk-Config",
                "{\"appbuilder_sdk_version\":\"0.8.0\",\"appbuilder_sdk_language\":\"java\"}");
        httpPost.setHeader("X-Appbuilder-Request-Id", java.util.UUID.randomUUID().toString());
        httpPost.setEntity(entity);
        String headers = "headers: \n";
        for (Header header : httpPost.getHeaders()) {
            headers += header + "\n";
        }
        LOGGER.log(Level.FINE, "\n" + headers);
        return httpPost;
    }

    /**
     * 创建一个用于发送 POST 请求的 ClassicHttpRequest 对象
     * 适配OpenAPI，目前仅AgentBuilder使用
     *
     * @param url 请求的 URL
     * @param entity 请求的实体
     * @return 返回创建的 ClassicHttpRequest 对象
     */
    public ClassicHttpRequest createPostRequestV2(String url, HttpEntity entity) {
        String requestURL = GatewayV2 + url;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("Authorization", this.SecretKey);
        httpPost.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        httpPost.setHeader("X-Appbuilder-Sdk-Config", "{\"appbuilder_sdk_version\":\"0.8.0\",\"appbuilder_sdk_language\":\"java\"}");
        httpPost.setHeader("X-Appbuilder-Request-Id", java.util.UUID.randomUUID().toString());
        httpPost.setEntity(entity);
        String headers = "headers: \n";
        for (Header header : httpPost.getHeaders()) {
            headers += header + "\n";
        }
        LOGGER.log(Level.FINE, "\n" + headers);
        return httpPost;
    }

    public <T> HttpResponse<T> execute(ClassicHttpRequest request, Type bodyType)
            throws IOException, AppBuilderServerException {
        if(LOGGER.getLevel() == Level.FINE) {
            buildCurlCommand(request);
        }
        HttpResponse<T> httpResponse = client.execute(request, resp -> {
            Map<String, String> headers = new LinkedHashMap<>();
            for (Header header : resp.getHeaders()) {
                headers.put(header.getName(), header.getValue());
            }
            String requestId = headers.get(AppBuilderConfig.APPBUILDER_REQUEST_ID);
            String stringBody = EntityUtils.toString(resp.getEntity());
            HttpResponse<T> response = new HttpResponse<T>()
                    .setCode(resp.getCode())
                    .setMessage(resp.getReasonPhrase())
                    .setRequestId(requestId)
                    .setHeaders(headers)
                    .setStringBody(stringBody);
            if (resp.getCode() == 200) {
                response.setBody(JsonUtils.deserialize(stringBody, bodyType));
            }
            return response;
        });
        if (httpResponse.getCode() != 200) {
            throw new AppBuilderServerException(httpResponse.getRequestId(),
                    httpResponse.getCode(), httpResponse.getMessage(), httpResponse.getStringBody());
        }
        return httpResponse;
    }

    public <T> HttpResponse<Iterator<T>> executeSSE(ClassicHttpRequest request, Type bodyType)
            throws IOException, AppBuilderServerException {
        if (LOGGER.getLevel() == Level.FINE) {
            buildCurlCommand(request);
        }
        CloseableHttpResponse resp = client.execute(request);
        Map<String, String> headers = new LinkedHashMap<>();
        for (Header header : resp.getHeaders()) {
            headers.put(header.getName(), header.getValue());
        }
        String requestId = headers.get(AppBuilderConfig.APPBUILDER_REQUEST_ID);
        if (resp.getCode() != 200) {
            String stringBody = "";
            try {
                stringBody = EntityUtils.toString(resp.getEntity());
            } catch (ParseException ignored) {
            }
            throw new AppBuilderServerException(requestId, resp.getCode(), resp.getReasonPhrase(), stringBody);
        }
        return new HttpResponse<Iterator<T>>()
                .setCode(resp.getCode())
                .setMessage(resp.getReasonPhrase())
                .setRequestId(requestId)
                .setHeaders(headers)
                .setBody(new StreamIterator<>(resp, bodyType));
    }
    
    private void buildCurlCommand(ClassicHttpRequest request) {
        StringBuilder curlCmd = new StringBuilder("curl -L");
        try {
            curlCmd.append(" ").append(request.getUri()).append(" \\\n");
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Invalid URL: ", e);
        }

        // Append headers
        for (Header header : request.getHeaders()) {
            curlCmd.append(" -H \"").append(header.getName()).append(": ").append(header.getValue()).append("\"");
            curlCmd.append(" \\\n");
        }

        // Append body
        HttpEntity entity = request.getEntity();
        if (entity != null && entity.isRepeatable()) {
            try {
                String body = EntityUtils.toString(entity);
                curlCmd.append(" -d '").append(body).append("'");
            } catch (ParseException | IOException e) {}
        }

        LOGGER.log(Level.FINE, "Crul Command: \n" + curlCmd.toString() + "\n");
    }
}