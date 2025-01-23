package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

import java.beans.Transient;

public class KnowledgeBaseConfigTest {

    private KnowledgeBaseConfig knowledgeBaseConfig;
    private KnowledgeBaseConfig.Index index;

    @Before
    public void setUp() {
        index = new KnowledgeBaseConfig.Index("es", "clusterId", "user", "password", "bj");
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
    public void testIndexClusterId() {
        assertEquals("clusterId", index.getClusterId());
    }

    @Test
    public void testIndexUsername() {
        assertEquals("user", index.getUsername());
    }

    @Test
    public void testIndexPassword() {
        assertEquals("password", index.getPassword());
    }

    @Test
    public void testIndexRegion() {
        assertEquals("bj", index.getRegion());
    }
}