package com.baidubce.appbuilder.model.aisearch;

import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;

public class AISearchIterator {
        private final StreamIterator<AISearchResponse> iterator;

    public AISearchIterator(StreamIterator<AISearchResponse> iterator) {
        this.iterator = iterator;
    }

    public boolean hasNext() {
        return iterator.hasNext();
    }

    public AISearchResponse next() {
        return iterator.next();
    }

    public void close(){
        iterator.close();
    }
}
