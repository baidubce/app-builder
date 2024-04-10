package com.baidubce.appbuilder.model.agentbuilder;

import java.util.Iterator;

public class AgentBuilderIterator {
    private final Iterator<AgentBuilderResponse> iterator;

    public AgentBuilderIterator(Iterator<AgentBuilderResponse> iterator) {
        this.iterator = iterator;
    }

    public boolean hasNext() {
        return iterator.hasNext();
    }

    public AgentBuilderResult next() {
        AgentBuilderResponse response = iterator.next();
        return new AgentBuilderResult()
                .setAnswer(response.getAnswer())
                .setContent(response.getContent());
    }
}
