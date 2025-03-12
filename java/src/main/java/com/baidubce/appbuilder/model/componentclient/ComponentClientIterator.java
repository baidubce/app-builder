package com.baidubce.appbuilder.model.componentclient;

import java.util.Iterator;


public class ComponentClientIterator {
    private final Iterator<ComponentClientRunResponse> iterator;

    public ComponentClientIterator(Iterator<ComponentClientRunResponse> iterator) {
        this.iterator = iterator;
    }

    public boolean hasNext() {
        return iterator.hasNext();
    }

    public ComponentClientRunResponse next() {
        return iterator.next();
    }
}
