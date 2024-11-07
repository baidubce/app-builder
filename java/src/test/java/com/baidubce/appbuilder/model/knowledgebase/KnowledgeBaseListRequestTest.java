package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class KnowledgeBaseListRequestTest {

    private KnowledgeBaseListRequest knowledgeBaseListRequest;

    @Before
    public void setUp() {
        // 初始化 KnowledgeBaseListRequest 对象
        knowledgeBaseListRequest = new KnowledgeBaseListRequest("marker123", 20, "searchKeyword");
    }

    @Test
    public void testGetMarker() {
        assertEquals("marker123", knowledgeBaseListRequest.getMarker());
    }

    @Test
    public void testGetMaxKeys() {
        assertEquals(20, knowledgeBaseListRequest.getMaxKeys());
    }

    @Test
    public void testGetKeyword() {
        assertEquals("searchKeyword", knowledgeBaseListRequest.getKeyword());
    }
}