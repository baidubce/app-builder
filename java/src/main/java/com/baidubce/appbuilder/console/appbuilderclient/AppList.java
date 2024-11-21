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
import com.baidubce.appbuilder.model.appbuilderclient.App;
import com.baidubce.appbuilder.model.appbuilderclient.AppListResponse;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeRequest;
import com.baidubce.appbuilder.model.appbuilderclient.AppsDescribeResponse;
import com.baidubce.appbuilder.model.appbuilderclient.AppListRequest;

public class AppList extends Component {
    public AppList() {
        super();
    }

    /**
     * @deprecated 该方法已被弃用，请改用新方法
     *
     * 根据请求获取应用列表
     *
     * @param request 请求参数
     * @return 应用列表数组
     * @throws IOException 如果发生输入输出异常
     * @throws AppBuilderServerException 如果发生应用构建服务器异常
     */
    @Deprecated
    public App[] getAppList(AppListRequest request) throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APP_LIST_URL;

        ClassicHttpRequest getRequest = httpClient.createGetRequestV2(url, request.toMap());
        getRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppListResponse> response = httpClient.execute(getRequest, AppListResponse.class);
        AppListResponse respBody = response.getBody();
        return respBody.getData();
    }
    
    /**
     * 描述应用程序信息
     *
     * @param request 包含应用程序描述信息的请求对象
     * @return 包含应用程序描述信息的响应对象
     * @throws IOException 如果发生I/O异常
     * @throws AppBuilderServerException 如果发生AppBuilder服务器异常
     */
    public AppsDescribeResponse describeApps(AppsDescribeRequest request) 
            throws IOException, AppBuilderServerException {
        String url = AppBuilderConfig.APPS_DESCRIBE_URL;

        String jsonBody = JsonUtils.serialize(request);
        ClassicHttpRequest postRequest = httpClient.createPostRequestV2(url,
                new StringEntity(jsonBody, StandardCharsets.UTF_8));
        postRequest.setHeader("Content-Type", "application/json");
        HttpResponse<AppsDescribeResponse> response = httpClient.execute(postRequest,
                AppsDescribeResponse.class);
        AppsDescribeResponse respBody = response.getBody();
        return respBody;
    }
}
