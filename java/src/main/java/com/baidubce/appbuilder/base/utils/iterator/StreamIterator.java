package com.baidubce.appbuilder.base.utils.iterator;

import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.Iterator;
import java.util.NoSuchElementException;

public class StreamIterator<T> implements Iterator<T>, AutoCloseable {
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
