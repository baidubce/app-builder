package com.baidubce.appbuilder.model.agentbuilder;


import java.util.Arrays;

public class AgentBuilderResult {
    private String answer;
    private Event[] events;

    public String getAnswer() {
        return answer;
    }

    public AgentBuilderResult setAnswer(String answer) {
        this.answer = answer;
        return this;
    }

    public Event[] getEvents() {
        return events;
    }

    public AgentBuilderResult setEvents(Event[] events) {
        this.events = events;
        return this;
    }

    @Override
    public String toString() {
        return "AgentBuilderResult{" +
                "answer='" + answer + '\'' +
                ", events=" + Arrays.toString(events) +
                '}';
    }
}
