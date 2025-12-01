package com.baidubce.appbuilder;

import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import static org.junit.Assert.*;

import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.componentclient.ComponentClient;
import com.baidubce.appbuilder.model.componentclient.ComponentClientIterator;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunRequest;
import com.baidubce.appbuilder.model.componentclient.ComponentClientRunResponse;

public class ComponentClientTest {
    String componentId;

    @Before
    public void setUp() {
        System.setProperty("APPBUILDER_TOKEN", System.getenv("APPBUILDER_TOKEN"));
        System.setProperty("APPBUILDER_LOGLEVEL", "DEBUG");
        componentId = "44205c67-3980-41f7-aad4-37357b577fd0";
    }

    @Test
    public void TestComponentClientRun() throws IOException, AppBuilderServerException {
        ComponentClient client = new ComponentClient();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put(ComponentClientRunRequest.SysOriginQuery, "北京景点推荐");
        ComponentClientIterator iter = client.run(componentId, "latest", "", false, parameters);
        while (iter.hasNext()) {
            ComponentClientRunResponse response = iter.next();
            assertNotNull(response.getContent()[0].getText());
        }
    }

    @Test
    public void TestComponentClientRunStream() throws IOException, AppBuilderServerException {
        ComponentClient client = new ComponentClient();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put(ComponentClientRunRequest.SysOriginQuery, "北京景点推荐");
        ComponentClientIterator iter = client.run(componentId, "latest", "", true, parameters);
        Object text = null;
        while (iter.hasNext()) {
            ComponentClientRunResponse response = iter.next();
            if (response.getContent().length > 0) {
                text = response.getContent()[0].getText();
            }
        }
        assertNotNull(text);
    }

    @Test
    public void TestComponentClientHeaderRun() throws IOException, AppBuilderServerException {
        this.componentId = "c-wf-a39ee06c-808f-4a19-9f5f-544044283749";
        ComponentClient client = new ComponentClient();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put(ComponentClientRunRequest.SysOriginQuery, "梦到巨人");
        ComponentClientIterator iter = client.run(componentId, "latest", "", false, parameters);
        while (iter.hasNext()) {
            ComponentClientRunResponse response = iter.next();
            System.out.println((response.getContent()[0].getText().get("info")));
        }
    }

    @Test
    public void TestComponentClientHeaderRunStream() throws IOException, AppBuilderServerException {
        this.componentId = "c-wf-a39ee06c-808f-4a19-9f5f-544044283749";
        ComponentClient client = new ComponentClient();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put(ComponentClientRunRequest.SysOriginQuery, "梦到巨人");
        ComponentClientIterator iter = client.run(componentId, "latest", "", true, parameters);

        while (iter.hasNext()) {
            ComponentClientRunResponse response = iter.next();
            if (response.getContent().length > 0) {
                System.out.println((response.getContent()[0].getText().get("info")));
            }
        }

    }
}
