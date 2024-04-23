package com.baidubce.appbuilder.base.utils.http;

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
    private final CloseableHttpClient client;

    public HttpClient(String secretKey, String gateway) {
        RequestConfig requestConfig = RequestConfig.custom()
                .setResponseTimeout(AppBuilderConfig.HTTP_CLIENT_CONNECTION_TIMEOUT, TimeUnit.SECONDS)
                .build();
        this.client = HttpClients.custom().setDefaultRequestConfig(requestConfig).build();
        this.SecretKey = secretKey;
        this.Gateway = gateway;
    }

    public ClassicHttpRequest createPostRequest(String url, HttpEntity entity) {
        String requestURL = Gateway + url;
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("X-Appbuilder-Authorization", this.SecretKey);
        httpPost.setHeader("X-Appbuilder-Origin", "appbuilder_sdk");
        httpPost.setHeader("X-Appbuilder-Sdk-Config", "{\"appbuilder_sdk_version\":\"0.7.0\",\"appbuilder_sdk_language\":\"java\"}");
        httpPost.setEntity(entity);
        return httpPost;
    }

    public <T> HttpResponse<T> execute(ClassicHttpRequest request, Type bodyType) throws IOException, AppBuilderServerException {
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

    public <T> HttpResponse<Iterator<T>> executeSSE(ClassicHttpRequest request, Type bodyType) throws IOException, AppBuilderServerException {
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
}