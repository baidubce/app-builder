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
        System.setProperty("APPBUILDER_TOKEN", "");
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
        System.setProperty("APPBUILDER_LOGFILE", "");
        appId = "";
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
        String fileId = builder.uploadLocalFile(conversationId, "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AppBuilderClientIterator itor = builder.run("北京有多少小学生", conversationId, new String[] { fileId }, true);
        assertTrue(itor.hasNext());
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }

    @Test(expected = AppBuilderServerException.class)
    public void testCreateConversation_AppBuilderServerException() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient("appId");
        builder.createConversation();
    }

    @Test
    public void AppBuilderClientRunFuncTest() throws IOException, AppBuilderServerException {
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();
        assertNotNull(conversationId);
        String fileId = builder.uploadLocalFile(conversationId, "src/test/java/com/baidubce/appbuilder/files/test.pdf");
        assertNotNull(fileId);
        AppBuilderClientRunRequest request = new AppBuilderClientRunRequest();
        request.setAppId(appId);
        request.setConversationID(conversationId);
        request.setQuery(
                "今天北京的天气怎么样?");
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
        while (itor.hasNext()) {
            AppBuilderClientResult result = itor.next();
            System.out.println(result);
        }
    }
}