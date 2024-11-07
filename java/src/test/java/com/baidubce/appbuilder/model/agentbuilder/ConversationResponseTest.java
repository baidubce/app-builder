package com.baidubce.appbuilder.model.agentbuilder;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ConversationResponseTest {
    private ConversationResponse conversationResponse;

    @Before
    public void setUp() {
        conversationResponse = new ConversationResponse();
        conversationResponse.setRequestId("testRequestId");
        conversationResponse.setConversationId("testConversationId");
    }

    @Test
    public void testRequestId() {
        assertEquals("testRequestId", conversationResponse.getRequestId());
    }

    @Test
    public void testConversationId() {
        assertEquals("testConversationId", conversationResponse.getConversationId());
    }

    @Test
    public void testToString() {
        String expectedString = "ConversationResponse{" +
                "requestId='testRequestId', conversationId='testConversationId'}";
        assertEquals(expectedString, conversationResponse.toString());
    }
}