package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class FileUploadResponseTest {
    private FileUploadResponse fileUploadResponse;
    private FileUploadResult fileUploadResult;

    @Before
    public void setUp() {
        fileUploadResponse = new FileUploadResponse();
        fileUploadResult = new FileUploadResult();
        fileUploadResult.setId("file123");
        fileUploadResult.setName("testFile.txt");
        fileUploadResult.setSize(1024);
        fileUploadResult.setExtension(".txt");
        fileUploadResult.setMimeType("text/plain");
        fileUploadResult.setCreatedBy("user123");
        fileUploadResult.setCreatedAt(123456789L);
    }

    @Test
    public void testCode() {
        fileUploadResponse.setCode(200);
        assertEquals(200, fileUploadResponse.getCode());
    }

    @Test
    public void testMessage() {
        fileUploadResponse.setMessage("Upload successful");
        assertEquals("Upload successful", fileUploadResponse.getMessage());
    }

    @Test
    public void testResult() {
        fileUploadResponse.setResult(fileUploadResult);
        assertNotNull(fileUploadResponse.getResult());
        assertEquals("file123", fileUploadResponse.getResult().getId());
        assertEquals("testFile.txt", fileUploadResponse.getResult().getName());
        assertEquals(1024, fileUploadResponse.getResult().getSize());
        assertEquals(".txt", fileUploadResponse.getResult().getExtension());
        assertEquals("text/plain", fileUploadResponse.getResult().getMimeType());
        assertEquals("user123", fileUploadResponse.getResult().getCreatedBy());
        assertEquals(123456789L, fileUploadResponse.getResult().getCreatedAt());
    }

    @Test
    public void testToString() {
        fileUploadResponse.setCode(200);
        fileUploadResponse.setMessage("Upload successful");
        fileUploadResponse.setResult(fileUploadResult);

        String expectedString = "FileUploadResponse{" +
                "code=200, message='Upload successful', result=FileUploadResult{id='file123', name='testFile.txt', size=1024, extension='.txt', mimeType='text/plain', createdBy='user123', createdAt=123456789}}";
        
        assertEquals(expectedString, fileUploadResponse.toString());
    }
}