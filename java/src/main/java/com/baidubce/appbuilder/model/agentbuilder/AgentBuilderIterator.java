package com.baidubce.appbuilder.model.agentbuilder;

import java.util.Iterator;
import java.util.stream.IntStream;

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
        Event[] events = new Event[response.getContent().length];
        EventContent[] contents = response.getContent();
        IntStream.range(0, contents.length).forEach(i -> {
            events[i] = new Event()
                    .setCode(contents[i].getEventCode())
                    .setMessage(contents[i].getEnentMessage())
                    .setStatus(contents[i].getEventStatus())
                    .setEventType(contents[i].getEventType())
                    .setContentType(contents[i].getContentType())
                    .setDetail(contents[i].getOutputs());
        });
        return new AgentBuilderResult()
                .setAnswer(response.getAnswer())
                .setEvents(events);
    }
}
