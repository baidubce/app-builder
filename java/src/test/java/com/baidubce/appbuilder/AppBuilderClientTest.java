package com.baidubce.appbuilder;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.console.appbuilderclient.AppList;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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
        String fileId = builder.uploadLocalFile(conversationId,
                "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest();
        request.setAppId(appId);
        request.setConversationID(conversationId);
        request.setQuery("今天北京的天气怎么样?");
        request.setStream(false);

        String name = "get_cur_whether";
        String desc = "这是一个获得指定地点天气的工具";
        Map<String, Object> parameters = new HashMap<>();

        Map<String, Object> location = new HashMap<>();
        location.put("type", "string");
        location.put("description", "省，市名，例如：河北省");

        Map<String, Object> unit = new HashMap<>();
        unit.put("type", "string");
        List<String> enumValues = new ArrayList<>();
        enumValues.add("摄氏度");
        enumValues.add("华氏度");
        unit.put("enum", enumValues);

        Map<String, Object> properties = new HashMap<>();
        properties.put("location", location);
        properties.put("unit", unit);

        parameters.put("type", "object");
        parameters.put("properties", properties);
        List<String> required = new ArrayList<>();
        required.add("location");
        parameters.put("required", required);

        AppBuilderClientRunRequest.Tool.Function func = new AppBuilderClientRunRequest.Tool.Function(name, desc,
                parameters);
        AppBuilderClientRunRequest.Tool tool = new AppBuilderClientRunRequest.Tool("function", func);
        request.setTools(new AppBuilderClientRunRequest.Tool[] { tool });

        AppBuilderClientIterator itor = builder.run(request);
        assertTrue(itor.hasNext());
        String ToolCallID = "";
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            ToolCallID = result.getEvents()[0].getToolCalls()[0].getId();
            System.out.println(result);
        }

        AppBuilderClientRunRequest request2 = new AppBuilderClientRunRequest();
        request2.setAppId(appId);
        request2.setConversationID(conversationId);

        AppBuilderClientRunRequest.ToolOutput output = new AppBuilderClientRunRequest.ToolOutput(ToolCallID, "北京今天35度");
        request2.setToolOutputs(new AppBuilderClientRunRequest.ToolOutput[] { output });
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

        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest();
        request.setAppId(appId);
        request.setConversationID(conversationId);
        request.setQuery("你能干什么");
        request.setStream(false);
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
