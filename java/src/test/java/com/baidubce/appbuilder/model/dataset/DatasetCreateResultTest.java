package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DatasetCreateResultTest {
    private DatasetCreateResult datasetCreateResult;

    @Before
    public void setUp() {
        datasetCreateResult = new DatasetCreateResult();
    }

    @Test
    public void testId() {
        datasetCreateResult.setId("test_id");
        assertEquals("test_id", datasetCreateResult.getId());
    }

    @Test
    public void testName() {
        datasetCreateResult.setName("test_name");
        assertEquals("test_name", datasetCreateResult.getName());
    }

    @Test
    public void testDescription() {
        datasetCreateResult.setDescription("test_description");
        assertEquals("test_description", datasetCreateResult.getDescription());
    }

    @Test
    public void testIndexingTechnique() {
        datasetCreateResult.setIndexingTechnique("test_indexing_technique");
        assertEquals("test_indexing_technique", datasetCreateResult.getIndexingTechnique());
    }

    @Test
    public void testDocumentCount() {
        datasetCreateResult.setDocumentCount(123);
        assertEquals(123, datasetCreateResult.getDocumentCount());
    }

    @Test
    public void testWordCount() {
        datasetCreateResult.setWordCount(456);
        assertEquals(456, datasetCreateResult.getWordCount());
    }

    @Test
    public void testCreatedBy() {
        datasetCreateResult.setCreatedBy("test_created_by");
        assertEquals("test_created_by", datasetCreateResult.getCreatedBy());
    }

    @Test
    public void testCreatedAt() {
        datasetCreateResult.setCreatedAt(123456789L);
        assertEquals(123456789L, datasetCreateResult.getCreatedAt());
    }

    @Test
    public void testUpdatedBy() {
        datasetCreateResult.setUpdatedBy("test_updated_by");
        assertEquals("test_updated_by", datasetCreateResult.getUpdatedBy());
    }

    @Test
    public void testUpdatedAt() {
        datasetCreateResult.setUpdatedAt(987654321L);
        assertEquals(987654321L, datasetCreateResult.getUpdatedAt());
    }

    @Test
    public void testIsPriority() {
        datasetCreateResult.setPriority(true);
        assertTrue(datasetCreateResult.isPriority());

        datasetCreateResult.setPriority(false);
        assertFalse(datasetCreateResult.isPriority());
    }

    @Test
    public void testToString() {
        datasetCreateResult.setId("test_id");
        datasetCreateResult.setName("test_name");
        datasetCreateResult.setDescription("test_description");
        datasetCreateResult.setIndexingTechnique("test_indexing_technique");
        datasetCreateResult.setDocumentCount(123);
        datasetCreateResult.setWordCount(456);
        datasetCreateResult.setCreatedBy("test_created_by");
        datasetCreateResult.setCreatedAt(123456789L);
        datasetCreateResult.setUpdatedBy("test_updated_by");
        datasetCreateResult.setUpdatedAt(987654321L);
        datasetCreateResult.setPriority(true);

        String expectedString = "DatasetCreateResult{" +
                "id='test_id', name='test_name', description='test_description', " +
                "indexingTechnique='test_indexing_technique', documentCount=123, wordCount=456, " +
                "createdBy='test_created_by', createdAt=123456789, updatedBy='test_updated_by', " +
                "updatedAt=987654321, isPriority=true}";

        assertEquals(expectedString, datasetCreateResult.toString());
    }
}