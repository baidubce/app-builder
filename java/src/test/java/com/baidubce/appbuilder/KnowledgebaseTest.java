package com.baidubce.appbuilder;

import static org.junit.Assert.assertNotNull;

import java.io.IOException;

import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.knowledgebase.Knowledgebase;
import com.baidubce.appbuilder.model.knowledgebase.*;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertNotNull;
import java.util.Arrays;


public class KnowledgebaseTest {
    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN_V3"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
    }

    @Test
    public void testAddDocument() throws IOException, AppBuilderServerException {
        String knowledgeBaseId = System.getenv("DATASET_ID_V3");
        Knowledgebase knowledgebase = new Knowledgebase();

        DocumentListRequest listRequest = new DocumentListRequest();
        listRequest.setKonwledgeBaseId(knowledgeBaseId);
        listRequest.setLimit(10);
        Document[] documents = knowledgebase.getDocumentList(listRequest);
        assertTrue(documents.length > 0);
        assertNotNull(documents[0].getId());

        String fileId = knowledgebase.uploadFile("src/test/java/com/baidubce/appbuilder/files/test.pdf");
        System.out.println(fileId);
        assertNotNull(fileId);

        DocumentAddRequest request = new DocumentAddRequest();
        request.setKnowledgeBaseId(knowledgeBaseId);
        request.setContentType("raw_text");
        request.setFileIds(new String[] {fileId});
        DocumentAddRequest.CustomProcessRule customProcessRule =
                new DocumentAddRequest.CustomProcessRule();
        customProcessRule.setSeparators(new String[] {"。"});
        customProcessRule.setTargetLength(300);
        customProcessRule.setOverlapRate(0.25);
        request.setCustomProcessRule(customProcessRule);

        String[] documentsRes = knowledgebase.addDocument(request);

        // Ensure that documentsRes array is not empty
        assertTrue(documentsRes.length > 0);
        assertNotNull(documentsRes);

        DocumentDeleteRequest deleteRequest = new DocumentDeleteRequest();
        deleteRequest.setKonwledgeBaseId(knowledgeBaseId);
        deleteRequest.setDocumentId(documentsRes[0]);

        knowledgebase.deleteDocument(deleteRequest);
    }

    @Test
    public void testCreateKnowledgebase() throws IOException, AppBuilderServerException {
        Knowledgebase knowledgebase = new Knowledgebase();
        KnowledgeBaseDetail request = new KnowledgeBaseDetail();
        request.setName("test_knowledgebase");
        request.setDescription("test_knowledgebase");

        // 创建知识库
        KnowledgeBaseConfig.Index index = new KnowledgeBaseConfig.Index("public",
                "http://localhost:9200", "elastic", "changeme");
        KnowledgeBaseConfig config = new KnowledgeBaseConfig(index);
        request.setConfig(config);
        KnowledgeBaseDetail response = knowledgebase.createKnowledgeBase(request);
        String knowledgeBaseId = response.getId();
        System.out.println(knowledgeBaseId);
        assertNotNull(response.getId());

        // 获取知识库详情
        KnowledgeBaseDetail detail = knowledgebase.getKnowledgeBaseDetail(knowledgeBaseId);
        System.out.println(detail.getId());
        assertNotNull(detail.getId());

        // 获取知识库列表
        KnowledgeBaseListRequest listRequest =
                new KnowledgeBaseListRequest(knowledgeBaseId, 10, null);
        KnowledgeBaseListResponse knowledgeBases = knowledgebase.getKnowledgeBaseList(listRequest);
        System.out.println(knowledgeBases.getMarker());
        assertNotNull(knowledgeBases.getMarker());

        // 更新知识库
        KnowledgeBaseModifyRequest modifyRequest = new KnowledgeBaseModifyRequest();
        modifyRequest.setKnowledgeBaseId(knowledgeBaseId);
        modifyRequest.setName("test_knowledgebase2");
        modifyRequest.setDescription(knowledgeBaseId);
        knowledgebase.modifyKnowledgeBase(modifyRequest);

        // 导入知识库
        DocumentsCreateRequest.Source source = new DocumentsCreateRequest.Source("web",
                new String[] {"https://baijiahao.baidu.com/s?id=1802527379394162441"}, 1);
        DocumentsCreateRequest.ProcessOption.Parser parser =
                new DocumentsCreateRequest.ProcessOption.Parser(
                        new String[] {"layoutAnalysis", "ocr"});
        DocumentsCreateRequest.ProcessOption.Chunker.Separator separator =
                new DocumentsCreateRequest.ProcessOption.Chunker.Separator(new String[] {"。"}, 300,
                        0.25);
        DocumentsCreateRequest.ProcessOption.Chunker chunker =
                new DocumentsCreateRequest.ProcessOption.Chunker(new String[] {"separator"},
                        separator, null, new String[] {"title", "filename"});
        DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation knowledgeAugmentation =
                new DocumentsCreateRequest.ProcessOption.KnowledgeAugmentation(
                        new String[] {"faq"});
        DocumentsCreateRequest.ProcessOption processOption =
                new DocumentsCreateRequest.ProcessOption("custom", parser, chunker,
                        knowledgeAugmentation);
        DocumentsCreateRequest documentsCreateRequest =
                new DocumentsCreateRequest(knowledgeBaseId, "rawText", source, processOption);
        knowledgebase.createDocuments(documentsCreateRequest);

        // 上传文档
        String filePath = "src/test/java/com/baidubce/appbuilder/files/test.pdf";
        DocumentsCreateRequest.Source source2 =
                new DocumentsCreateRequest.Source("file", null, null);
        DocumentsCreateRequest documentsCreateRequest2 =
                new DocumentsCreateRequest(knowledgeBaseId, "rawText", source2, processOption);
        knowledgebase.uploadDocuments(filePath, documentsCreateRequest2);

        // 删除知识库
        knowledgebase.deleteKnowledgeBase(knowledgeBaseId);
    }
    
    @Test
    public void testCreateChunk() throws IOException, AppBuilderServerException {
        String documentId = System.getenv("DOCUMENT_ID_V3");
        Knowledgebase knowledgebase = new Knowledgebase();
        // 创建切片
        String chunkId = knowledgebase.createChunk(documentId, "test");
        // 修改切片
        knowledgebase.modifyChunk(chunkId, "new test", true);
        // 获取切片详情
        knowledgebase.describeChunk(chunkId);
        // 获取切片列表
        knowledgebase.describeChunks(documentId, chunkId, 10, null);
        try {
            // 延时 
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        // 删除切片
        knowledgebase.deleteChunk(chunkId);
    }
}
