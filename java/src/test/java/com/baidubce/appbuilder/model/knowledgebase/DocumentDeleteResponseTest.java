package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class DocumentDeleteResponseTest {

    private DocumentDeleteResponse documentDeleteResponse;

    @Before
    public void setUp() {
        documentDeleteResponse = new DocumentDeleteResponse();
    }

    @Test
    public void testGetSetRequestId() {
        documentDeleteResponse.setRequestId("req123");
        assertEquals("req123", documentDeleteResponse.getRequestId());
    }

    @Test
    public void testGetSetCode() {
        documentDeleteResponse.setCode("200");
        assertEquals("200", documentDeleteResponse.getCode());
    }

    @Test
    public void testGetSetMessage() {
        documentDeleteResponse.setMessage("Success");
        assertEquals("Success", documentDeleteResponse.getMessage());
    }

    @Test
    public void testToString() {
        documentDeleteResponse.setRequestId("req123");
        documentDeleteResponse.setCode("200");
        documentDeleteResponse.setMessage("Success");

        String expectedString = "DocumentDeleteResponse{" +
                "request_id=req123" +
                ", code='200'" +
                ", message='Success" +
                '}';

        assertEquals(expectedString, documentDeleteResponse.toString());
    }
}