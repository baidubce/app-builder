package com.baidubce.appbuilder.model.knowledgebase;

import org.junit.Before;
import org.junit.Test;

import java.util.Map;

import static org.junit.Assert.*;

public class DocumentDeleteRequestTest {

    private DocumentDeleteRequest documentDeleteRequest;

    @Before
    public void setUp() {
        // 初始化 DocumentDeleteRequest 对象
        documentDeleteRequest = new DocumentDeleteRequest();
    }

    @Test
    public void testSetAndGetKonwledgeBaseId() {
        // 设置 knowledgeBaseId
        documentDeleteRequest.setKonwledgeBaseId("kb123");

        // 验证是否正确返回设置的 knowledgeBaseId
        assertEquals("kb123", documentDeleteRequest.getKonwledgeBaseId());
    }

    @Test
    public void testSetAndGetDocumentId() {
        // 设置 documentId
        documentDeleteRequest.setDocumentId("doc456");

        // 验证是否正确返回设置的 documentId
        assertEquals("doc456", documentDeleteRequest.getDocumentId());
    }

    @Test
    public void testToMap() {
        // 设置字段
        documentDeleteRequest.setKonwledgeBaseId("kb123");
        documentDeleteRequest.setDocumentId("doc456");

        // 验证 toMap() 方法是否正确返回 map
        Map<String, Object> resultMap = documentDeleteRequest.toMap();
        assertEquals("kb123", resultMap.get("knowledge_base_id"));
        assertEquals("doc456", resultMap.get("document_id"));
    }
}