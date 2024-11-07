package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class KnowledgeBaseConfigTest {

    private KnowledgeBaseConfig knowledgeBaseConfig;
    private KnowledgeBaseConfig.Index index;

    @Before
    public void setUp() {
        index = new KnowledgeBaseConfig.Index("es", "http://localhost:9200", "user", "password");
        knowledgeBaseConfig = new KnowledgeBaseConfig(index);
    }

    @Test
    public void testGetIndex() {
        assertEquals(index, knowledgeBaseConfig.getIndex());
    }

    @Test
    public void testIndexType() {
        assertEquals("es", index.getType());
    }

    @Test
    public void testIndexEsUrl() {
        assertEquals("http://localhost:9200", index.getEsUrl());
    }

    @Test
    public void testIndexUsername() {
        assertEquals("user", index.getUsername());
    }

    @Test
    public void testIndexPassword() {
        assertEquals("password", index.getPassword());
    }
}