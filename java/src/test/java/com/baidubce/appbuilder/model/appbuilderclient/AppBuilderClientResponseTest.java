package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class AppBuilderClientResponseTest {
    private AppBuilderClientResponse response;

    @Before
    public void setUp() {
        response = new AppBuilderClientResponse();
    }

    @Test
    public void testRequestId() {
        response.setRequestId("test_request_id");
        assertEquals("test_request_id", response.getRequestId());
    }

    @Test
    public void testData() {
        response.setData("test_data");
        assertEquals("test_data", response.getData());
    }

    @Test
    public void testAnswer() {
        response.setAnswer("test_answer");
        assertEquals("test_answer", response.getAnswer());
    }

    @Test
    public void testConversationId() {
        response.setConversationId("test_conversation_id");
        assertEquals("test_conversation_id", response.getConversationId());
    }

    @Test
    public void testMessageId() {
        response.setMessageId("test_message_id");
        assertEquals("test_message_id", response.getMessageId());
    }

    @Test
    public void testIsCompletion() {
        response.setCompletion(true);
        assertTrue(response.isCompletion());
    }

    @Test
    public void testContent() {
        EventContent[] contentArray = new EventContent[1];
        response.setContent(contentArray);
        assertArrayEquals(contentArray, response.getContent());
    }

    @Test
    public void testToString() {
        response.setRequestId("test_request_id");
        response.setData("test_data");
        response.setAnswer("test_answer");
        response.setConversationId("test_conversation_id");
        response.setMessageId("test_message_id");
        response.setCompletion(true);
        EventContent[] contentArray = new EventContent[1];
        response.setContent(contentArray);

        String expectedString = "AgentBuilderResponse{" +
                "requestId='test_request_id', data='test_data', answer='test_answer', " +
                "conversationId='test_conversation_id', messageId='test_message_id', " +
                "isCompletion=true, content=[null]}";
        assertEquals(expectedString, response.toString());
    }
}