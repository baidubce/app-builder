package com.baidubce.appbuilder.model.rag;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;

public class RAGIterator {
    private final HttpResponse<StreamIterator<RAGResponse>> resp;
    private final StreamIterator<RAGResponse> iterator;

    public RAGIterator(HttpResponse<StreamIterator<RAGResponse>> resp) {
        this.resp = resp;
        this.iterator = resp.getBody();
    }

    public boolean hasNext() {
        return iterator.hasNext();
    }

    public RAGResponse next() throws AppBuilderServerException {
        RAGResponse ragResponse = iterator.next();
        if (ragResponse.getCode() != 0) {
            throw new AppBuilderServerException(resp.getRequestId(), resp.getCode(), resp.getMessage(),
                    ragResponse.getCode(), ragResponse.getMessage());
        }
        return ragResponse;
    }

    public void close(){
        iterator.close();
    }
}
