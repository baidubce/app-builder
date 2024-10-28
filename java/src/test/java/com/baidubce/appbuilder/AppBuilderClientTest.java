package com.baidubce.appbuilder;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.console.appbuilderclient.AppList;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class AppBuilderClientTest {
    String appId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
        appId = "aa8af334-df27-4855-b3d1-0d249c61fc08";
    }

    @Test
    public void GetAppsTest() throws IOException, AppBuilderServerException {
        AppList builder = new AppList();
        AppListRequest request = new AppListRequest();
        request.setLimit(10);
        assertNotNull(builder.getAppList(request)[0].getId());
    }

    @Test
    public void AppBuilderClientRunTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        String fileId = builder.uploadLocalFile(conversationId,
                "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AppBuilderClientIterator itor =
                builder.run("北京有多少小学生", conversationId, new String[] {fileId}, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }

    @Test(expected = AppBuilderServerException.class)
    public void testCreateConversation_AppBuilderServerException()
            throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient("appId");
        builder.createConversation();
    }

    @Test
    public void AppBuilderClientRunFuncTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "今天北京的天气怎么样?", false);

        String toolJson = new String(Files.readAllBytes(Paths.get("src/test/java/com/baidubce/appbuilder/files/toolcall.json")));
        request.setTools(toolJson);

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        String ToolCallID = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            ToolCallID = result.getEvents()[0].getToolCalls()[0].getId();
            System.out.println(result);
        }

        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest(appId, conversationId);
        request2.setToolOutputs(ToolCallID, "北京今天35度");
        AppBuilderClientIterator itor2 = builder.run(request2);
        assertTrue(itor2.hasNext());
        while (itor2.hasNext()) {
            AppBuilderClientResult result = itor2.next();
            System.out.println(result);
        }
    }
    
    @Test
    public void AppBuilderClientRunToolChoiceTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest(appId, conversationId, "你能干什么", false);
        request.setEndUserId("java_test_user_0");
        Map<String, Object> input = new HashMap<>();
        input.put("city", "北京");
        AppBuilderClientRunRequest.ToolChoice.Function func = new AppBuilderClientRunRequest.ToolChoice.Function(
                "WeatherQuery", input);
        AppBuilderClientRunRequest.ToolChoice choice = new AppBuilderClientRunRequest.ToolChoice("function", func);
        request.setToolChoice(choice);

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }
}
