package com.baidubce.appbuilder.model.componentclient;

import com.baidubce.appbuilder.base.utils.iterator.StreamIterator;


public class ComponentClientIterator {
    private final StreamIterator<ComponentClientRunResponse> iterator;

    public ComponentClientIterator(StreamIterator<ComponentClientRunResponse> iterator) {
        this.iterator = iterator;
    }

    public boolean hasNext() {
        return iterator.hasNext();
    }

    public ComponentClientRunResponse next() {
        return iterator.next();
    }

    public void close(){
        iterator.close();
    }
}
