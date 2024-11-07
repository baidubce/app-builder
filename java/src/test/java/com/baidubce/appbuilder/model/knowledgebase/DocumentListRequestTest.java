package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class DocumentListRequestTest {

    private DocumentListRequest documentListRequest;

    @Before
    public void setUp() {
        documentListRequest = new DocumentListRequest();
    }

    @Test
    public void testGetSetKonwledgeBaseId() {
        documentListRequest.setKonwledgeBaseId("kb123");
        assertEquals("kb123", documentListRequest.getKonwledgeBaseId());
    }

    @Test
    public void testGetSetLimit() {
        documentListRequest.setLimit(10);
        assertEquals(10, documentListRequest.getLimit());
    }

    @Test
    public void testGetSetAfter() {
        documentListRequest.setAfter("afterToken");
        assertEquals("afterToken", documentListRequest.getAfter());
    }

    @Test
    public void testGetSetBefore() {
        documentListRequest.setBefore("beforeToken");
        assertEquals("beforeToken", documentListRequest.getBefore());
    }

    @Test
    public void testToMapWithAllValues() {
        documentListRequest.setKonwledgeBaseId("kb123");
        documentListRequest.setLimit(10);
        documentListRequest.setAfter("afterToken");
        documentListRequest.setBefore("beforeToken");

        Map<String, Object> resultMap = documentListRequest.toMap();

        assertEquals(4, resultMap.size());
        assertEquals("kb123", resultMap.get("knowledge_base_id"));
        assertEquals(10, resultMap.get("limit"));
        assertEquals("afterToken", resultMap.get("after"));
        assertEquals("beforeToken", resultMap.get("before"));
    }

    @Test
    public void testToMapWithLimitZero() {
        documentListRequest.setKonwledgeBaseId("kb123");
        documentListRequest.setLimit(0); // limit set to 0
        documentListRequest.setAfter("afterToken");
        documentListRequest.setBefore("beforeToken");

        Map<String, Object> resultMap = documentListRequest.toMap();

        assertEquals(3, resultMap.size()); // limit should not be included
        assertEquals("kb123", resultMap.get("knowledge_base_id"));
        assertEquals("afterToken", resultMap.get("after"));
        assertEquals("beforeToken", resultMap.get("before"));
        assertTrue(!resultMap.containsKey("limit")); // Ensure limit is not included when it's 0
    }
}