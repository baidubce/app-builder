package com.baidubce.appbuilder.model.dataset;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DocumentListResultTest {
    private DocumentListResult documentListResult;

    @Before
    public void setUp() {
        documentListResult = new DocumentListResult();
    }

    @Test
    public void testHasMore() {
        documentListResult.setHasMore(true);
        assertTrue(documentListResult.isHasMore());

        documentListResult.setHasMore(false);
        assertFalse(documentListResult.isHasMore());
    }

    @Test
    public void testLimit() {
        documentListResult.setLimit(10);
        assertEquals(10, documentListResult.getLimit());
    }

    @Test
    public void testPage() {
        documentListResult.setPage(2);
        assertEquals(2, documentListResult.getPage());
    }

    @Test
    public void testTotal() {
        documentListResult.setTotal(100);
        assertEquals(100, documentListResult.getTotal());
    }

    @Test
    public void testData() {
        DocumentListData data1 = new DocumentListData();
        data1.setId("doc1");
        data1.setName("Document 1");

        DocumentListData data2 = new DocumentListData();
        data2.setId("doc2");
        data2.setName("Document 2");

        DocumentListData[] dataArray = {data1, data2};
        documentListResult.setData(dataArray);

        assertEquals(2, documentListResult.getData().length);
        assertEquals("doc1", documentListResult.getData()[0].getId());
        assertEquals("Document 1", documentListResult.getData()[0].getName());
        assertEquals("doc2", documentListResult.getData()[1].getId());
        assertEquals("Document 2", documentListResult.getData()[1].getName());
    }

    @Test
    public void testToString() {
        DocumentListData data1 = new DocumentListData();
        data1.setId("doc1");
        data1.setName("Document 1");

        DocumentListData[] dataArray = {data1};
        documentListResult.setHasMore(true);
        documentListResult.setLimit(5);
        documentListResult.setPage(1);
        documentListResult.setTotal(50);
        documentListResult.setData(dataArray);

        String expectedString = "DocumentListResult{" +
                "hasMore=true, limit=5, page=1, total=50, data=[DocumentListData{id='doc1', name='Document 1', datasetProcessRuleId='null', dataSourceType='null', position=0, dataSourceInfo=null, createdFrom='null', createdBy='null', createdAt=0, indexingStatus='null', error=null, enabled=false, displayStatus='null', wordCount=0, estimatedWaitingMinutes=0, disabledAt=null, disabledBy=null}]}";

        assertEquals(expectedString, documentListResult.toString());
    }
}