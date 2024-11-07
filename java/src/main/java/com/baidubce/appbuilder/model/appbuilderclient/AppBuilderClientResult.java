package com.baidubce.appbuilder.model.appbuilderclient;


import java.util.Arrays;

public class AppBuilderClientResult {
    private String answer;
    private Event[] events;

    public String getAnswer() {
        return answer;
    }

    public AppBuilderClientResult setAnswer(String answer) {
        this.answer = answer;
        return this;
    }

    public Event[] getEvents() {
        return events;
    }

    public AppBuilderClientResult setEvents(Event[] events) {
        this.events = events;
        return this;
    }

    @Override
    public String toString() {
        return "AppBuilderClientResult{" +
                "answer='" + answer + '\'' +
                ", events=" + Arrays.toString(events) +
                '}';
    }
}
