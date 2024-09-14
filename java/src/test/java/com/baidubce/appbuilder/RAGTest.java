package com.baidubce.appbuilder;


import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertTrue;

import java.io.IOException;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.rag.RAG;
import com.baidubce.appbuilder.model.rag.RAGResponse;
import com.baidubce.appbuilder.model.rag.RAGIterator;
import com.baidubce.appbuilder.console.agentbuilder.AgentBuilder;

public class RAGTest {
    String appId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", "bce-v3/ALTAK-RPJR9XSOVFl6mb5GxHbfU/072be74731e368d8bbb628a8941ec50aaeba01cd");

        appId = "aa8af334-df27-4855-b3d1-0d249c61fc08";
    }
    /*
    @Test
    public void testRAG() throws IOException, AppBuilderServerException {
        AgentBuilder builder = new AgentBuilder(appId);
        String conversationId = builder.createConversation();
        RAG rag = new RAG(appId);
        RAGIterator itor = rag.run("合同中的甲方是谁？", conversationId, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            RAGResponse response = itor.next();
        }
    }*/
}
