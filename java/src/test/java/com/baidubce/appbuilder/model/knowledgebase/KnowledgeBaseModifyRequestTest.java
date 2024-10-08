package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class KnowledgeBaseModifyRequestTest {

    private KnowledgeBaseModifyRequest knowledgeBaseModifyRequest;

    @Before
    public void setUp() {
        knowledgeBaseModifyRequest = new KnowledgeBaseModifyRequest();
    }

    @Test
    public void testSetGetKnowledgeBaseId() {
        knowledgeBaseModifyRequest.setKnowledgeBaseId("kb123");
        assertEquals("kb123", knowledgeBaseModifyRequest.getKnowledgeBaseId());
    }

    @Test
    public void testSetGetName() {
        knowledgeBaseModifyRequest.setName("New Knowledge Base");
        assertEquals("New Knowledge Base", knowledgeBaseModifyRequest.getName());
    }

    @Test
    public void testSetGetDescription() {
        knowledgeBaseModifyRequest.setDescription("This is a description for the knowledge base.");
        assertEquals("This is a description for the knowledge base.", knowledgeBaseModifyRequest.getDescription());
    }
}