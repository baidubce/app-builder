package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class KnowledgeBaseListResponseTest {
    private KnowledgeBaseListResponse knowledgeBaseListResponse;
    private KnowledgeBaseDetail knowledgeBaseDetail1;
    private KnowledgeBaseDetail knowledgeBaseDetail2;

    @Before
    public void setUp() {
        knowledgeBaseListResponse = new KnowledgeBaseListResponse();
        
        // Initialize KnowledgeBaseDetail objects (assuming KnowledgeBaseDetail has default constructor and setters)
        knowledgeBaseDetail1 = new KnowledgeBaseDetail();
        knowledgeBaseDetail1.setId("kb1");
        knowledgeBaseDetail1.setName("KnowledgeBase 1");

        knowledgeBaseDetail2 = new KnowledgeBaseDetail();
        knowledgeBaseDetail2.setId("kb2");
        knowledgeBaseDetail2.setName("KnowledgeBase 2");

        knowledgeBaseListResponse.setRequestId("testRequestId");
        knowledgeBaseListResponse.setData(new KnowledgeBaseDetail[]{knowledgeBaseDetail1, knowledgeBaseDetail2});
        knowledgeBaseListResponse.setMarker("testMarker");
        knowledgeBaseListResponse.setTruncated(true);
        knowledgeBaseListResponse.setNextMarker("testNextMarker");
        knowledgeBaseListResponse.setMaxKeys(100);
    }

    @Test
    public void testRequestId() {
        assertEquals("testRequestId", knowledgeBaseListResponse.getRequestId());
    }

    @Test
    public void testData() {
        KnowledgeBaseDetail[] data = knowledgeBaseListResponse.getData();
        assertNotNull(data);
        assertEquals(2, data.length);
        assertEquals("kb1", data[0].getId());
        assertEquals("KnowledgeBase 1", data[0].getName());
        assertEquals("kb2", data[1].getId());
        assertEquals("KnowledgeBase 2", data[1].getName());
    }

    @Test
    public void testMarker() {
        assertEquals("testMarker", knowledgeBaseListResponse.getMarker());
    }

    @Test
    public void testIsTruncated() {
        assertTrue(knowledgeBaseListResponse.isTruncated());
    }

    @Test
    public void testNextMarker() {
        assertEquals("testNextMarker", knowledgeBaseListResponse.getNextMarker());
    }

    @Test
    public void testMaxKeys() {
        assertEquals(100, knowledgeBaseListResponse.getMaxKeys());
    }
}