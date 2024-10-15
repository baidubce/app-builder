package com.baidubce.appbuilder.model.appbuilderclient;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class FileUploadResponseTest {

    private FileUploadResponse fileUploadResponse;

    @Before
    public void setUp() {
        fileUploadResponse = new FileUploadResponse();
    }

    @Test
    public void testSetGetRequestId() {
        fileUploadResponse.setRequestId("request123");
        assertEquals("request123", fileUploadResponse.getRequestId());
    }

    @Test
    public void testSetGetFileId() {
        fileUploadResponse.setFileId("file456");
        assertEquals("file456", fileUploadResponse.getFileId());
    }

    @Test
    public void testSetGetConversationId() {
        fileUploadResponse.setConversationId("conversation789");
        assertEquals("conversation789", fileUploadResponse.getConversationId());
    }

    @Test
    public void testToString() {
        fileUploadResponse.setRequestId("request123");
        fileUploadResponse.setFileId("file456");
        fileUploadResponse.setConversationId("conversation789");

        String expected = "FileUploadResponse{" +
                "requestId='request123'" +
                ", fileId='file456'" +
                ", conversationId='conversation789'" +
                '}';

        assertEquals(expected, fileUploadResponse.toString());
    }
}