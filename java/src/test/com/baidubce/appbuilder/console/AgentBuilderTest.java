package com.baidubce.appbuilder.console;

import java.io.IOException;
import java.util.Iterator;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

import com.baidubce.appbuilder.console.agentbuilder.AgentBuilder;
import com.baidubce.appbuilder.model.agentbuilder.AgentBuilderResponse;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;

public class AgentBuilderTest {
    String appId;
    @Before
    public void setUp()  {
        System.setProperty("APPBUILDER_TOKEN", "xxx");
        System.setProperty("GATEWAY_URL", "xxx");
        appId = "xxx";
    }

    @Test
    public void testAgentBuilder() throws IOException, AppBuilderServerException {
        AgentBuilder agentBuilder = new AgentBuilder(appId);
        String conversationId = agentBuilder.createConversation();
        assertNotNull(conversationId);
        String fileId = agentBuilder.uploadLocalFile(conversationId, "java/src/test/com/baidubce/appbuilder/console/files/test.pdf");
        assertNotNull(fileId);
        Iterator<AgentBuilderResponse> itor = agentBuilder.run("北京有多少小学生", conversationId, new String[]{fileId}, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AgentBuilderResponse response = itor.next();
        }
    }

    @Test(expected = AppBuilderServerException.class)
    public void testCreateConversation_AppBuilderServerException() throws IOException, AppBuilderServerException {
        AgentBuilder agentBuilder = new AgentBuilder("appId");
        agentBuilder.createConversation();
    }
}