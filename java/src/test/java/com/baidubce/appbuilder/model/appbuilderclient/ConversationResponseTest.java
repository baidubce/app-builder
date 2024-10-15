package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class ConversationResponseTest {

    private ConversationResponse conversationResponse;

    @Before
    public void setUp() {
        conversationResponse = new ConversationResponse();
    }

    @Test
    public void testSetGetRequestId() {
        conversationResponse.setRequestId("req123");
        assertEquals("req123", conversationResponse.getRequestId());
    }

    @Test
    public void testSetGetConversationId() {
        conversationResponse.setConversationId("conv456");
        assertEquals("conv456", conversationResponse.getConversationId());
    }

    @Test
    public void testToString() {
        conversationResponse.setRequestId("req123");
        conversationResponse.setConversationId("conv456");

        String expected = "ConversationResponse{" +
                "requestId='req123'" +
                ", conversationId='conv456'" +
                '}';

        assertEquals(expected, conversationResponse.toString());
    }
}