package com.baidubce.appbuilder.base.utils.http;

import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.NoSuchElementException;

import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.Header;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.io.entity.EntityUtils;

public class HttpClient {
    public String SecretKey;
    public String Gateway;
    private final CloseableHttpClient client;

    public HttpClient(String secretKey, String gateway) {
        this.client = HttpClients.createDefault();
        this.SecretKey = secretKey;
        this.Gateway = gateway;
    }

    public ClassicHttpRequest createPostRequest(String url, HttpEntity entity) {
        String requestURL = Gateway + url;
        HttpPost httpPost = new HttpPost(requestURL);
        httpPost.setHeader("X-Appbuilder-Authorization", this.SecretKey);
        httpPost.setEntity(entity);
        return httpPost;
    }

    public <T> HttpResponse<T> execute(ClassicHttpRequest request, Type bodyType) throws IOException {
        return client.execute(request, resp -> {
            Map<String, String> headers = new LinkedHashMap<>();
            for (Header header : resp.getHeaders()) {
                headers.put(header.getName(), header.getValue());
            }
            String stringBody = EntityUtils.toString(resp.getEntity());
            return new HttpResponse<T>()
                    .setCode(resp.getCode())
                    .setMessage(resp.getReasonPhrase())
                    .setRequestId(headers.get(AppBuilderConfig.APPBUILDER_REQUEST_ID))
                    .setHeaders(headers)
                    .setStringBody(stringBody)
                    .setBody(JsonUtils.deserialize(stringBody, bodyType));
        });
    }

    public <T> HttpResponse<Iterator<T>> executeSSE(ClassicHttpRequest request, Type bodyType) throws IOException {
        CloseableHttpResponse resp = client.execute(request);

        Map<String, String> headers = new LinkedHashMap<>();
        for (Header header : resp.getHeaders()) {
            headers.put(header.getName(), header.getValue());
        }

        return new HttpResponse<Iterator<T>>()
                .setCode(resp.getCode())
                .setMessage(resp.getReasonPhrase())
                .setRequestId(headers.get(AppBuilderConfig.APPBUILDER_REQUEST_ID))
                .setHeaders(headers)
                .setBody(new StreamIterator<>(resp, bodyType));
    }
}

class StreamIterator<T> implements Iterator<T>, AutoCloseable {
    private final CloseableHttpResponse resp;
    private final BufferedReader reader;
    private final Type bodyType;
    private String nextLine;

    public StreamIterator(CloseableHttpResponse resp, Type type) throws IOException {
        this.resp = resp;
        this.reader = new BufferedReader(new InputStreamReader(resp.getEntity().getContent()));
        this.bodyType = type;
    }

    @Override
    public boolean hasNext() {
        if (this.nextLine != null) {
            return true;
        }
        try {
            this.nextLine = this.reader.readLine();
            // 跳过空白行
            this.reader.readLine();
        } catch (IOException e) {
            close();
            return false;
        }
        return this.nextLine != null;
    }

    @Override
    public T next() {
        if (hasNext()) {
            String currentLine = this.nextLine;
            this.nextLine = null;
            String respBody = currentLine.replaceFirst("data: ", "");
            return JsonUtils.deserialize(respBody, this.bodyType);
        } else {
            close();
            throw new NoSuchElementException("No more lines available");
        }
    }

    @Override
    public void close() {
        try {
            if (reader != null) {
                reader.close();
            }
            if (this.resp != null) {
                this.resp.close();
            }
        } catch (Exception ignored) {
            // ignore
        }
    }
}
