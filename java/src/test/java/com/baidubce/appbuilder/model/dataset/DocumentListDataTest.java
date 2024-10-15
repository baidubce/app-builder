package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.HashMap;
import java.util.Map;

public class DocumentListDataTest {
    private DocumentListData documentListData;

    @Before
    public void setUp() {
        documentListData = new DocumentListData();
    }

    @Test
    public void testId() {
        documentListData.setId("test_id");
        assertEquals("test_id", documentListData.getId());
    }

    @Test
    public void testName() {
        documentListData.setName("test_name");
        assertEquals("test_name", documentListData.getName());
    }

    @Test
    public void testDatasetProcessRuleId() {
        documentListData.setDatasetProcessRuleId("test_rule_id");
        assertEquals("test_rule_id", documentListData.getDatasetProcessRuleId());
    }

    @Test
    public void testDataSourceType() {
        documentListData.setDataSourceType("test_source_type");
        assertEquals("test_source_type", documentListData.getDataSourceType());
    }

    @Test
    public void testPosition() {
        documentListData.setPosition(5);
        assertEquals(5, documentListData.getPosition());
    }

    @Test
    public void testDataSourceInfo() {
        Map<String, String> dataSourceInfo = new HashMap<>();
        dataSourceInfo.put("key1", "value1");
        documentListData.setDataSourceInfo(dataSourceInfo);
        assertEquals(dataSourceInfo, documentListData.getDataSourceInfo());
    }

    @Test
    public void testCreatedFrom() {
        documentListData.setCreatedFrom("test_created_from");
        assertEquals("test_created_from", documentListData.getCreatedFrom());
    }

    @Test
    public void testCreatedBy() {
        documentListData.setCreatedBy("test_created_by");
        assertEquals("test_created_by", documentListData.getCreatedBy());
    }

    @Test
    public void testCreatedAt() {
        documentListData.setCreatedAt(123456789L);
        assertEquals(123456789L, documentListData.getCreatedAt());
    }

    @Test
    public void testIndexingStatus() {
        documentListData.setIndexingStatus("indexing");
        assertEquals("indexing", documentListData.getIndexingStatus());
    }

    @Test
    public void testError() {
        Object error = new Object();
        documentListData.setError(error);
        assertEquals(error, documentListData.getError());
    }

    @Test
    public void testEnabled() {
        documentListData.setEnabled(true);
        assertTrue(documentListData.isEnabled());

        documentListData.setEnabled(false);
        assertFalse(documentListData.isEnabled());
    }

    @Test
    public void testDisplayStatus() {
        documentListData.setDisplayStatus("displaying");
        assertEquals("displaying", documentListData.getDisplayStatus());
    }

    @Test
    public void testWordCount() {
        documentListData.setWordCount(1000);
        assertEquals(1000, documentListData.getWordCount());
    }

    @Test
    public void testEstimatedWaitingMinutes() {
        documentListData.setEstimatedWaitingMinutes(30);
        assertEquals(30, documentListData.getEstimatedWaitingMinutes());
    }

    @Test
    public void testDisabledAt() {
        Object disabledAt = new Object();
        documentListData.setDisabledAt(disabledAt);
        assertEquals(disabledAt, documentListData.getDisabledAt());
    }

    @Test
    public void testDisabledBy() {
        Object disabledBy = new Object();
        documentListData.setDisabledBy(disabledBy);
        assertEquals(disabledBy, documentListData.getDisabledBy());
    }

    @Test
    public void testToString() {
        documentListData.setId("test_id");
        documentListData.setName("test_name");
        documentListData.setDatasetProcessRuleId("test_rule_id");
        documentListData.setDataSourceType("test_source_type");
        documentListData.setPosition(5);
        Map<String, String> dataSourceInfo = new HashMap<>();
        dataSourceInfo.put("key1", "value1");
        documentListData.setDataSourceInfo(dataSourceInfo);
        documentListData.setCreatedFrom("test_created_from");
        documentListData.setCreatedBy("test_created_by");
        documentListData.setCreatedAt(123456789L);
        documentListData.setIndexingStatus("indexing");
        documentListData.setError(null);
        documentListData.setEnabled(true);
        documentListData.setDisplayStatus("displaying");
        documentListData.setWordCount(1000);
        documentListData.setEstimatedWaitingMinutes(30);
        documentListData.setDisabledAt(null);
        documentListData.setDisabledBy(null);

        String expectedString = "DocumentListData{" +
                "id='test_id', name='test_name', datasetProcessRuleId='test_rule_id', dataSourceType='test_source_type', " +
                "position=5, dataSourceInfo={key1=value1}, createdFrom='test_created_from', createdBy='test_created_by', " +
                "createdAt=123456789, indexingStatus='indexing', error=null, enabled=true, displayStatus='displaying', " +
                "wordCount=1000, estimatedWaitingMinutes=30, disabledAt=null, disabledBy=null}";
        assertEquals(expectedString, documentListData.toString());
    }
}