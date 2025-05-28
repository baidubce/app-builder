package com.baidubce.appbuilder.console.appbuilderclient;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.apache.hc.core5.http.ClassicHttpRequest;
import org.apache.hc.core5.http.io.entity.StringEntity;

import com.baidubce.appbuilder.base.component.Component;
import com.baidubce.appbuilder.base.config.AppBuilderConfig;
import com.baidubce.appbuilder.base.exception.AppBuilderServerException;
import com.baidubce.appbuilder.base.utils.http.HttpResponse;
import com.baidubce.appbuilder.base.utils.json.JsonUtils;
import com.baidubce.appbuilder.model.appbuilderclient.AppDescribeRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppDescribeResponse;

public class App extends Component {
    public App() {
        super();
    }
    
    /**
     * 描述应用程序信息
     *
     * @param appId 应用ID
     * @return 包含应用程序描述信息的响应对象
     * @throws IOException 如果发生I/O异常
     * @throws AppBuilderServerException 如果发生AppBuilder服务器异常
     */
    public AppDescribeResponse describeApp(String appId) 
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APP_DESCRIBE_URL;

        AppDescribeRequest request = new AppDescribeRequest();
        request.setId(appId);
        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppDescribeResponse> response = httpClient.execute(postRequest,
                AppDescribeResponse.class);
        AppDescribeResponse respBody = response.getBody();
        return respBody;
    }
}
