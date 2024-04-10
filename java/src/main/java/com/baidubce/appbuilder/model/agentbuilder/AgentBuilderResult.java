package com.baidubce.appbuilder.model.agentbuilder;

import java.util.Arrays;

public class AgentBuilderResult {
    private String answer;
    private EventContent[] content;

    public String getAnswer() {
        return answer;
    }

    public AgentBuilderResult setAnswer(String answer) {
        this.answer = answer;
        return this;
    }

    public EventContent[] getContent() {
        return content;
    }

    public AgentBuilderResult setContent(EventContent[] content) {
        this.content = content;
        return this;
    }

    @Override
    public String toString() {
        return "AgentBuilderResult{" +
                "answer='" + answer + '\'' +
                ", content=" + Arrays.toString(content) +
                '}';
    }
}
