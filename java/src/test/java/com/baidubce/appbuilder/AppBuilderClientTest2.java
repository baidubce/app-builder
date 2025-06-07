package com.baidubce.appbuilder;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;
import java.util.List;
import org.junit.Before;
import org.junit.Test;

import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientIterator;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientResult;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.console.appbuilderclient.AppBuilderClient;
import com.baidubce.appbuilder.console.appbuilderclient.AppList;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeRequest;
import com.baidubce.appbuilder.model.appbuilderclient.Event;
import com.baidubce.appbuilder.model.appbuilderclient.EventContent;
import com.baidubce.appbuilder.model.appbuilderclient.AppBuilderClientRunRequest;


import static org.junit.Assert.*;

public class AppBuilderClientTest {
    public static void main(String[] args) throws IOException, AppBuilderServerException {
        // 设置环境中的TOKEN，以下TOKEN请替换为您的个人TOKEN，个人TOKEN可通过该页面【获取鉴权参数】或控制台页【密钥管理】处获取
        System.setProperty("APPBUILDER_TOKEN", "bce-v3/ALTAK-TnXvQ6z8XCvkZTzP5ShMP/fbd28a8e80f8c3fa1ad9d505db4f843c913858f9");
       	// 从AppBuilder控制台【个人空间】-【应用】网页获取已发布应用的ID
        String appId = "bc78732b-b6a6-474b-b2f8-475f60759426";
        AppBuilderClient builder = new AppBuilderClient(appId);
        String conversationId = builder.createConversation();

        AppBuilderClientIterator itor = builder.run("你好，你能做什么？", conversationId, new String[] {}, false);
        StringBuilder answer = new StringBuilder();
        while (itor.hasNext()) {
            AppBuilderClientResult response = itor.next();
            answer.append(response.getAnswer());
        }
        System.out.println(answer);
    }
}
