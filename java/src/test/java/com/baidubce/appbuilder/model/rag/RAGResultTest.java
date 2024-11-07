package com.baidubce.appbuilder.model.rag;

import org.junit.Before;
import org.junit.Test;

import java.util.Arrays;  // 导入 java.util.Arrays

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertArrayEquals;

public class RAGResultTest {

    private RAGResult ragResult;

    @Before
    public void setUp() {
        ragResult = new RAGResult();
    }

    @Test
    public void testSetGetAnswer() {
        ragResult.setAnswer("This is an answer.");
        assertEquals("This is an answer.", ragResult.getAnswer());
    }

    @Test
    public void testSetGetConversationId() {
        ragResult.setConversationId("conv123");
        assertEquals("conv123", ragResult.getConversationId());
    }

    @Test
    public void testSetGetMessageId() {
        ragResult.setMessageId("msg456");
        assertEquals("msg456", ragResult.getMessageId());
    }

    @Test
    public void testSetGetIsCompletion() {
        ragResult.setIsCompletion(true);  // 可以是任意对象，通常是Boolean
        assertEquals(true, ragResult.getIsCompletion());
    }

    @Test
    public void testSetGetPrototype() {
        ragResult.setPrototype("prototype data");
        assertEquals("prototype data", ragResult.getPrototype());
    }

    @Test
    public void testSetGetContent() {
        EventContent[] mockContent = new EventContent[2];
        mockContent[0] = new EventContent();
        mockContent[0].setEventCode("event1");
        mockContent[1] = new EventContent();
        mockContent[1].setEventCode("event2");

        ragResult.setContent(mockContent);
        assertArrayEquals(mockContent, ragResult.getContent());
    }

    @Test
    public void testToString() {
        ragResult.setAnswer("This is an answer.");
        ragResult.setConversationId("conv123");
        ragResult.setMessageId("msg456");
        ragResult.setIsCompletion(true);
        ragResult.setPrototype("prototype data");

        EventContent[] mockContent = new EventContent[2];
        mockContent[0] = new EventContent();
        mockContent[0].setEventCode("event1");
        mockContent[1] = new EventContent();
        mockContent[1].setEventCode("event2");
        ragResult.setContent(mockContent);

        String expected = "RAGResult{" +
                "answer='This is an answer.'" +
                ", conversationId='conv123'" +
                ", messageId='msg456'" +
                ", isCompletion=true" +
                ", prototype='prototype data'" +
                ", content=" + Arrays.toString(mockContent) +
                '}';

        assertEquals(expected, ragResult.toString());
    }
}