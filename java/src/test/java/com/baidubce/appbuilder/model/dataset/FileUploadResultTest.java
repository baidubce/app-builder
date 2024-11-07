package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class FileUploadResultTest {
    private FileUploadResult fileUploadResult;

    @Before
    public void setUp() {
        fileUploadResult = new FileUploadResult();
    }

    @Test
    public void testId() {
        fileUploadResult.setId("test_id");
        assertEquals("test_id", fileUploadResult.getId());
    }

    @Test
    public void testName() {
        fileUploadResult.setName("test_name");
        assertEquals("test_name", fileUploadResult.getName());
    }

    @Test
    public void testSize() {
        fileUploadResult.setSize(1024);
        assertEquals(1024, fileUploadResult.getSize());
    }

    @Test
    public void testExtension() {
        fileUploadResult.setExtension(".txt");
        assertEquals(".txt", fileUploadResult.getExtension());
    }

    @Test
    public void testMimeType() {
        fileUploadResult.setMimeType("text/plain");
        assertEquals("text/plain", fileUploadResult.getMimeType());
    }

    @Test
    public void testCreatedBy() {
        fileUploadResult.setCreatedBy("test_user");
        assertEquals("test_user", fileUploadResult.getCreatedBy());
    }

    @Test
    public void testCreatedAt() {
        fileUploadResult.setCreatedAt(123456789L);
        assertEquals(123456789L, fileUploadResult.getCreatedAt());
    }

    @Test
    public void testToString() {
        fileUploadResult.setId("test_id");
        fileUploadResult.setName("test_name");
        fileUploadResult.setSize(1024);
        fileUploadResult.setExtension(".txt");
        fileUploadResult.setMimeType("text/plain");
        fileUploadResult.setCreatedBy("test_user");
        fileUploadResult.setCreatedAt(123456789L);

        String expectedString = "FileUploadResult{" +
                "id='test_id', name='test_name', size=1024, extension='.txt', mimeType='text/plain', " +
                "createdBy='test_user', createdAt=123456789}";

        assertEquals(expectedString, fileUploadResult.toString());
    }
}