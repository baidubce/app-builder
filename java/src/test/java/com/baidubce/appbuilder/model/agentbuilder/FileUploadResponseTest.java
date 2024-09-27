package com.baidubce.appbuilder.model.agentbuilder;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class FileUploadResponseTest {
    private FileUploadResponse fileUploadResponse;

    @Before
    public void setUp() {
        fileUploadResponse = new FileUploadResponse();
        fileUploadResponse.setRequestId("testRequestId");
        fileUploadResponse.setFileId("testFileId");
        fileUploadResponse.setConversationId("testConversationId");
    }

    @Test
    public void testGetRequestId() {
        assertEquals("testRequestId", fileUploadResponse.getRequestId());
    }

    @Test
    public void testGetFileId() {
        assertEquals("testFileId", fileUploadResponse.getFileId());
    }

    @Test
    public void testGetConversationId() {
        assertEquals("testConversationId", fileUploadResponse.getConversationId());
    }

    @Test
    public void testToString() {
        String expectedString = "FileUploadResponse{" +
                "requestId='testRequestId'" +
                ", fileId='testFileId'" +
                ", conversationId='testConversationId'" +
                '}';
        assertEquals(expectedString, fileUploadResponse.toString());
    }
}