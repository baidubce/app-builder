package com.baidubce.appbuilder;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.model.agentbuilder.AgentBuilderIterator;

import java.io.IOException;

import com.baidubce.appbuilder.model.agentbuilder.AgentBuilderResult;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

import com.baidubce.appbuilder.console.agentbuilder.AgentBuilder;

public class AgentBuilderTest{
    String appId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", "");
        System.setProperty("APPBUILDER_LOGLEVEL", "INFO");
        appId = "";
    }

    @Test
    public void testAgentBuilder() throws IOException, AppBuilderServerException {
        AgentBuilder builder = new AgentBuilder(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        String fileId = builder.uploadLocalFile(conversationId, "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AgentBuilderIterator itor = builder.run("北京有多少小学生", conversationId, new String[]{fileId}, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AgentBuilderResult result = itor.next();
            System.out.println(result);

        }
    }

    @Test(expected = AppBuilderServerException.class)
    public void testCreateConversation_AppBuilderServerException() throws IOException, AppBuilderServerException {
        AgentBuilder builder = new AgentBuilder("appId");
        builder.createConversation();
    }
}