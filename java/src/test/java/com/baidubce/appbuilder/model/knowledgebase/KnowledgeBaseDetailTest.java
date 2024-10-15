package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class KnowledgeBaseDetailTest {

    private KnowledgeBaseDetail knowledgeBaseDetail;
    private KnowledgeBaseConfig knowledgeBaseConfig;

    @Before
    public void setUp() {
        knowledgeBaseDetail = new KnowledgeBaseDetail();
        knowledgeBaseConfig = new KnowledgeBaseConfig(new KnowledgeBaseConfig.Index("type1", "esUrl", "user", "pass"));
    }

    @Test
    public void testSetGetId() {
        knowledgeBaseDetail.setId("kb123");
        assertEquals("kb123", knowledgeBaseDetail.getId());
    }

    @Test
    public void testSetGetName() {
        knowledgeBaseDetail.setName("Knowledge Base Name");
        assertEquals("Knowledge Base Name", knowledgeBaseDetail.getName());
    }

    @Test
    public void testSetGetDescription() {
        knowledgeBaseDetail.setDescription("This is a knowledge base description.");
        assertEquals("This is a knowledge base description.", knowledgeBaseDetail.getDescription());
    }

    @Test
    public void testSetGetConfig() {
        knowledgeBaseDetail.setConfig(knowledgeBaseConfig);
        assertEquals(knowledgeBaseConfig, knowledgeBaseDetail.getConfig());
    }
}