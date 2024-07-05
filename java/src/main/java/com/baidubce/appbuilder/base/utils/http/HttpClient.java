package com.baidubce.appbuilder.base.utils.http;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;

import java.io.IOException;
import java.lang.reflect.Type;
import java.net.URLEncoder;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.logging.ConsoleHandler;
import java.util.logging.Level;
import java.util.logging.FileHandler;
import java.util.logging.Logger;

import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.classic.methods.HttpDelete;
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
    public String ConsoleOpenAPIVersion;
    public String ConsoleOpenAPIPrefix;

    
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
        } else {
            switch (systemLogLevel.toLowerCase()) {
                case "debug":
                    LOGGER.setLevel(Level.FINE);
                    handler.setLevel(Level.FINE);
                    break;
                case "warning":
                    LOGGER.setLevel(Level.WARNING);
                    handler.setLevel(Level.WARNING);
                    break;
                case "error":
                    LOGGER.setLevel(Level.SEVERE);
                    handler.setLevel(Level.SEVERE);
                    break;
                default:
                    LOGGER.setLevel(Level.INFO);
                    handler.setLevel(Level.INFO);
                    break;
            }
        }
        LOGGER.addHandler(handler);

        String systemLogFile = System.getProperty(AppBuilderConfig.APPBUILDER_LOGFILE);
        if (systemLogFile == null || systemLogFile.isEmpty()) {
            systemLogFile = System.getenv(AppBuilderConfig.APPBUILDER_LOGFILE);
        }

        if (systemLogFile != null && !systemLogFile.isEmpty()) {
            try {
                FileHandler fileHandler = new FileHandler(systemLogFile);
                LOGGER.addHandler(fileHandler);
            } catch (Exception e) {
                throw new RuntimeException("Failed to create log file: " + systemLogFile, e); 
            }
        }
    }

    public ClassicHttpRequest createPostRequest(String url, HttpEntity entity) {
        String requestURL = Gateway + url;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("X-Appbuilder-Authorization", this.SecretKey);
        httpPost.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        String platform = System.getenv("APPBUILDER_SDK_PLATFORM") != null ? System.getenv("APPBUILDER_SDK_PLATFORM")
                : "unknown";
        httpPost.setHeader("X-Appbuilder-Sdk-Config",
                "{\"appbuilder_sdk_version\":\"0.9.0\",\"appbuilder_sdk_language\":\"java\",\"appbuilder_sdk_platform\":\""
                        + platform + "\"}");
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
        String requestURL = GatewayV2 + ConsoleOpenAPIPrefix + ConsoleOpenAPIVersion + url;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("Authorization", this.SecretKey);
        httpPost.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        String platform = System.getenv("APPBUILDER_SDK_PLATFORM") != null ? System.getenv("APPBUILDER_SDK_PLATFORM")
                : "unknown";
        httpPost.setHeader("X-Appbuilder-Sdk-Config",
                "{\"appbuilder_sdk_version\":\"0.9.0\",\"appbuilder_sdk_language\":\"java\",\"appbuilder_sdk_platform\":\"" + platform + "\"}");
        httpPost.setHeader("X-Appbuilder-Request-Id", java.util.UUID.randomUUID().toString());
        httpPost.setEntity(entity);
        String headers = "headers: \n";
        for (Header header : httpPost.getHeaders()) {
            headers += header + "\n";
        }
        LOGGER.log(Level.FINE, "\n" + headers);
        return httpPost;
    }

    public ClassicHttpRequest createGetRequestV2(String url, Map<String, Object> map) {
        String urlParams = toQueryString(map);
        String requestURL = GatewayV2 + ConsoleOpenAPIPrefix + ConsoleOpenAPIVersion + url + "?" + urlParams;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpGet httpGet = new HttpGet(requestURL);
        httpGet.setHeader("Authorization", this.SecretKey);
        httpGet.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        String platform = System.getenv("APPBUILDER_SDK_PLATFORM") != null ? System.getenv("APPBUILDER_SDK_PLATFORM")
                : "unknown";
        httpGet.setHeader("X-Appbuilder-Sdk-Config",
                "{\"appbuilder_sdk_version\":\"0.9.0\",\"appbuilder_sdk_language\":\"java\",\"appbuilder_sdk_platform\":\""
                        + platform + "\"}");
        httpGet.setHeader("X-Appbuilder-Request-Id", java.util.UUID.randomUUID().toString());
        String headers = "headers: \n";
        for (Header header : httpGet.getHeaders()) {
            headers += header + "\n";
        }
        LOGGER.log(Level.FINE, "\n" + headers);
        return httpGet;
    }
    
    public ClassicHttpRequest createDeleteRequestV2(String url, Map<String, Object> map) {
        String urlParams = toQueryString(map);
        String requestURL = GatewayV2 + ConsoleOpenAPIPrefix + ConsoleOpenAPIVersion + url + "?" + urlParams;
        LOGGER.log(Level.FINE, "requestURL: " + requestURL);
        HttpDelete httpDelete = new HttpDelete(requestURL);
        httpDelete.setHeader("Authorization", this.SecretKey);
        httpDelete.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        String platform = System.getenv("APPBUILDER_SDK_PLATFORM") != null ? System.getenv("APPBUILDER_SDK_PLATFORM")
                : "unknown";
        httpDelete.setHeader("X-Appbuilder-Sdk-Config",
                "{\"appbuilder_sdk_version\":\"0.9.0\",\"appbuilder_sdk_language\":\"java\",\"appbuilder_sdk_platform\":\""
                        + platform + "\"}");
        httpDelete.setHeader("X-Appbuilder-Request-Id", java.util.UUID.randomUUID().toString());
        String headers = "headers: \n";
        for (Header header : httpDelete.getHeaders()) {
            headers += header + "\n";
        }
        LOGGER.log(Level.FINE, "\n" + headers);
        return httpDelete;
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

    private String toQueryString(Map<String, Object> map) {
        StringBuilder stringBuilder = new StringBuilder();
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            if (entry.getValue() != null) {
                if (stringBuilder.length() != 0) {
                    stringBuilder.append('&');
                }
                try {
                    stringBuilder.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
                    stringBuilder.append('=');
                    stringBuilder.append(URLEncoder.encode(entry.getValue().toString(), "UTF-8"));
                } catch (Exception e) {
                    // Should never happen.
                }
            }
        }
        return stringBuilder.toString();
    }
    
    private void buildCurlCommand(ClassicHttpRequest request) {
        StringBuilder curlCmd = new StringBuilder("curl");

        // Append method
        curlCmd.append(" -X ").append(request.getMethod());
        curlCmd.append(" -L");
        try {
            curlCmd.append(" ").append("\'").append(request.getUri()).append("\'").append(" \\\n");
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, "Invalid URL: ", e);
        }

        // Append headers
        for (Header header : request.getHeaders()) {
            curlCmd.append("-H \'").append(header.getName()).append(": ").append(header.getValue()).append("\'");
            curlCmd.append(" \\\n");
        }

        
        if ("GET".equals(request.getMethod()) || "DELETE".equals(request.getMethod())) {
            curlCmd = new StringBuilder(curlCmd.toString().replaceAll(" \\\\\n$", ""));
        }

        // Append body
        HttpEntity entity = request.getEntity();
        if (entity != null && entity.isRepeatable()) {
            try {
                String body = EntityUtils.toString(entity);
                curlCmd.append(" -d '").append(body).append("'");
            } catch (ParseException | IOException e) {}
        }

        LOGGER.log(Level.FINE, "Curl Command: \n" + curlCmd.toString() + "\n");
    }
}