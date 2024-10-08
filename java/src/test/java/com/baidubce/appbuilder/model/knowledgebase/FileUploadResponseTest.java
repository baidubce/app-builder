package com.baidubce.appbuilder.model.knowledgebase;

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
    public void testSetGetId() {
        fileUploadResponse.setId("file123");
        assertEquals("file123", fileUploadResponse.getId());
    }

    @Test
    public void testSetGetCode() {
        fileUploadResponse.setCode("200");
        assertEquals("200", fileUploadResponse.getCode());
    }

    @Test
    public void testSetGetMessage() {
        fileUploadResponse.setMessage("Upload successful");
        assertEquals("Upload successful", fileUploadResponse.getMessage());
    }

    @Test
    public void testToString() {
        fileUploadResponse.setRequestId("request123");
        fileUploadResponse.setId("file123");
        fileUploadResponse.setCode("200");
        fileUploadResponse.setMessage("Upload successful");

        String expected = "FileUploadResponse{" +
                "request_id=request123" +
                ", code='200'" +
                ", message='Upload successful" +
                '}';

        assertEquals(expected, fileUploadResponse.toString());
    }
}