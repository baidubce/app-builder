package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class KnowledgeBaseDetailRequestTest {

    private KnowledgeBaseDetailRequest knowledgeBaseDetailRequest;

    @Before
    public void setUp() {
        knowledgeBaseDetailRequest = new KnowledgeBaseDetailRequest();
    }

    @Test
    public void testGetKnowledgeBaseId() {
        knowledgeBaseDetailRequest.setKnowledgeBaseId("testKnowledgeBaseId");
        assertEquals("testKnowledgeBaseId", knowledgeBaseDetailRequest.getKnowledgeBaseId());
    }

    @Test
    public void testSetKnowledgeBaseId() {
        knowledgeBaseDetailRequest.setKnowledgeBaseId("newKnowledgeBaseId");
        assertEquals("newKnowledgeBaseId", knowledgeBaseDetailRequest.getKnowledgeBaseId());
    }
}